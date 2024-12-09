import json

import nltk
import os
import multiprocessing as mp
from multiprocessing import Manager
from nltk.corpus import words
from collections import Counter

nltk.download('words')
setofwords = set(words.words())


class Solution:
    def __init__(self):
        pass

    def worker_backtrack(self, starting_words, input_freq_counter, num_words, shared_solutions, shared_iterations, lock):
        """
        Worker function that runs backtracking starting with assigned words.
        """
        def backtrack(path, freq_counter, remaining_words):
            with lock:  # Safely increment iteration counter
                shared_iterations.value += 1
                if shared_iterations.value % 1000 == 0:
                    print(f"Iteration {shared_iterations.value}.. Solutions: {len(shared_solutions)}")

            # Base case: If no more words are needed, validate and store the solution
            if remaining_words == 0:
                if all(v == 0 for v in freq_counter.values()):
                    solution = " ".join(path)
                    with lock:
                        shared_solutions.append(solution)
                return

            # Try forming each word using the available letters
            for word in setofwords:
                if len(word) == 1 and word != "a":
                    continue
                word_counter = Counter(word)
                if all(freq_counter[char] >= word_counter[char] for char in word_counter):
                    # Choose the word
                    for char in word_counter:
                        freq_counter[char] -= word_counter[char]
                    path.append(word)

                    # Recur to form the next word
                    backtrack(path, freq_counter, remaining_words - 1)

                    # Undo the choice
                    path.pop()
                    for char in word_counter:
                        freq_counter[char] += word_counter[char]

        # Start backtracking from each starting word assigned to this worker
        for starting_word in starting_words:
            word_counter = Counter(starting_word)
            if all(input_freq_counter[char] >= word_counter[char] for char in word_counter):
                # Initialize path and frequency counter
                freq_counter = input_freq_counter.copy()
                for char in word_counter:
                    freq_counter[char] -= word_counter[char]
                backtrack([starting_word], freq_counter, num_words - 1)

    def solve_anagram_with_spaces(self, input_string, num_words=-1):
        print("Let's a go!")

        # Preprocess the input
        input_string_clean = input_string.replace(" ", "")
        num_words = input_string.count(" ") + 1 if num_words == -1 else num_words
        freq_counter = Counter(input_string_clean)

        final_solutions = list()

        # Use Manager to create shared resources
        with Manager() as manager:
            shared_solutions = manager.list()
            shared_iterations = manager.Value('i', 0)
            lock = mp.Lock()

            # Split the word list into chunks for each worker
            num_workers = mp.cpu_count()
            word_list = list(setofwords)
            chunk_size = len(word_list) // num_workers
            word_chunks = [word_list[i:i + chunk_size] for i in range(0, len(word_list), chunk_size)]

            # Launch worker processes
            processes = []
            for word_chunk in word_chunks:
                p = mp.Process(target=self.worker_backtrack,
                               args=(word_chunk, freq_counter, num_words, shared_solutions, shared_iterations, lock))
                processes.append(p)
                p.start()

            # Wait for all workers to finish
            for p in processes:
                p.join()

            # Return the final unique solutions
            solutions = list(set(shared_solutions))
            solutions.sort()
            final_solutions.append(solutions)

        return final_solutions


# Example usage
if __name__ == "__main__":
    mp.set_start_method("spawn")  # Required for macOS
    solver = Solution()
    input_string = "candis ignite myth"
    solutions = solver.solve_anagram_with_spaces(input_string)

    print(f"{solutions}")

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "anagrams_solutions.txt")
    with open(desktop_path, "w") as file:
        file.write(json.dumps(solutions))  # Write each solution on a new line

    print(f"Solutions saved to: {desktop_path}")

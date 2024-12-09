import nltk
nltk.download('words')

from nltk.corpus import words
setofwords = set(words.words())

from collections import Counter

def is_valid_word(word):
    return word.lower() in setofwords

class Solution:

    def __init__(self):
        self.iterations = 0

    def solve_anagram_with_spaces(self, input_string):
        print("Let's a go!")

        def backtrack(path, freq_counter, remaining_words):
            self.iterations += 1
            if self.iterations % 1000 == 0:
                print(f"Iteration {self.iterations}.. solutions: {solutions}")

            # Base case: If no more words are needed, validate and store the solution
            if remaining_words == 0:
                if all(v == 0 for v in freq_counter.values()):  # All letters used
                    solutions.add(tuple(path))
                return

            # Try forming each word using the available letters
            for word in setofwords:
                word_counter = Counter(word)
                # Check if the word can be formed with the remaining letters
                if all(freq_counter[char] >= word_counter[char] for char in word_counter):
                    # Choose the word
                    for char in word_counter:
                        freq_counter[char] -= word_counter[char]
                    path.append(word)

                    # Recur to form the next word
                    backtrack(path, freq_counter, remaining_words - 1)

                    # Undo the choice (backtrack)
                    path.pop()
                    for char in word_counter:
                        freq_counter[char] += word_counter[char]

        # Preprocess the input
        input_string_clean = input_string.replace(" ", "")  # Remove spaces
        num_words = input_string.count(" ") + 1  # Total words (spaces + 1)
        freq_counter = Counter(input_string_clean)  # Frequency of letters
        solutions = set()

        backtrack([], freq_counter, num_words)
        return solutions

# Example usage:
if __name__ == "__main__":
    solver = Solution()
    input_string = "candis ignite myth"
    solutions = solver.solve_anagram_with_spaces(input_string)
    print("Possible Anagrams:", solutions)

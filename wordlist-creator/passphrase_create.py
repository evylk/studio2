import os
import random

def generate_passphrase(filename="Full_Alphabet_Kids_Vocabulary_Wordlist.csv", num_words=4, max_length=6):
    # Get the path to the current script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)

    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Extract the 3rd value (index 2) from each comma-separated line
    words = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) >= 3:
            word = parts[2]
            if len(word) <= max_length:
                words.append(word)

    # Check we have enough words
    if len(words) < num_words:
        raise ValueError(f"Not enough short words! Found {len(words)}, need {num_words}.")

    # Generate passphrase
    passphrase = ' '.join(random.sample(words, num_words))
    return passphrase

# Example usage
try:
    print("Generated passphrase:", generate_passphrase())
except ValueError as e:
    print("Error:", e)



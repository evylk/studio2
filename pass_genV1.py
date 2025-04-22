import random
import re
from zxcvbn import zxcvbn

def load_wordlist(filepath):
    with open(filepath, 'r') as file:
        words = [line.strip().split('\t')[1] for line in file if '\t' in line]
    return words

def generate_passphrase(words, min_length=15):
    while True:
        selected = random.sample(words, 3)
        passphrase = '-'.join(selected)
        if len(passphrase) >= min_length:
            return passphrase

def display_strength(passphrase):
    result = zxcvbn(passphrase)
    score = result['score']
    feedback = result['feedback']
    
    print(f"\nPassphrase: {passphrase}")
    print(f"Strength Score: {score} / 4")
    
    if feedback['warning']:
        print(f"⚠️  Warning: {feedback['warning']}")
    if feedback['suggestions']:
        for suggestion in feedback['suggestions']:
            print(f"💡 Suggestion: {suggestion}")

def main():
    wordlist_path = 'eff.txt'
    words = load_wordlist(wordlist_path)

    while True:
        passphrase = generate_passphrase(words)
        display_strength(passphrase)

        choice = input("\nGenerate a new passphrase? (y/n): ").strip().lower()
        if choice != 'y':
            print("Passphrase accepted.")
            break

if __name__ == "__main__":
    main()
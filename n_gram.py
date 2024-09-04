import re
import os
import math
from collections import defaultdict

def product(numbers):
    result = 1
    for number in numbers:
        result *= number
    return result

def tokenize(text):
    return re.split(r"[.?!]\s+", text)

def splitToWords(sentence):
    return sentence.split()

def getNGramString(words, n):
    """
    Generate n-grams from a list of words.
    """
    return [' '.join(words[i:i + n]) for i in range(len(words) - n + 1)]

def preprocess_text_data(text_data, n):
    """
    Process the text data into sentences, word counts, and n-gram counts for efficient lookup.
    """
    sentences = tokenize(text_data)
    word_counts = defaultdict(int)
    ngram_counts = defaultdict(int)
    
    for sentence in sentences:
        words = splitToWords(sentence.lower())
        for i, word in enumerate(words):
            word_counts[word] += 1
            if i >= n-1:
                ngram = ' '.join(words[i-n+1:i+1])
                ngram_counts[ngram] += 1
    
    total_words_count = sum(word_counts.values())
    unique_words_count = len(word_counts)
    
    return sentences, word_counts, ngram_counts, total_words_count, unique_words_count

def findCount(word, word_counts):
    return word_counts[word]

def findCountAtStartOfSentence(word, sentences):
    return sum(sentence.lower().startswith(word) for sentence in sentences)

def calculate_sentence_prob(sentence, sentences, word_counts, ngram_counts, total_words_count, n):
    words = splitToWords(sentence.lower())
    
    if len(words) == 0:
        return 0  # Handle the case where the sentence is empty
    
    probabilities = [
        findCountAtStartOfSentence(' '.join(words[:n]), sentences) / total_words_count if total_words_count > 0 else 0
    ]
    
    for i in range(n, len(words)):
        ngram = ' '.join(words[i-n+1:i+1])
        ngram_count = ngram_counts[ngram]
        word_count = word_counts[words[i]]
        probabilities.append(ngram_count / word_count if word_count > 0 else 0)
    
    return product(probabilities)

def smooth_sentence_prob(sentence, sentences, word_counts, ngram_counts, total_words_count, total_unique_words_count, n):
    if total_words_count == 0 or total_unique_words_count == 0:
        raise ValueError("Total words count or total unique words count is zero, which is invalid for probability calculations.")
    
    words = splitToWords(sentence.lower())
    
    if len(words) == 0:
        return 0  # Handle the case where the sentence is empty
    
    probabilities = [
        (findCountAtStartOfSentence(' '.join(words[:n]), sentences) + 1) / (total_words_count + total_unique_words_count)
    ]
    
    for i in range(n, len(words)):
        ngram = ' '.join(words[i-n+1:i+1])
        ngram_count = ngram_counts[ngram] + 1
        word_count = word_counts[words[i]] + total_unique_words_count
        probabilities.append(ngram_count / word_count)
    
    return product(probabilities)

def perplexity(probability, num_words):
    epsilon = 1e-10  # Small value to prevent zero probability
    probability = max(probability, epsilon)  # Ensure probability is not zero
    log_prob = math.log(probability)
    
    try:
        return math.exp(-log_prob * num_words)
    except OverflowError:
        return float('inf')

def input_text_or_file():
    while True:
        choice = input("Do you want to enter text manually or use a text file? (enter 'text' or 'file'): ").strip().lower()
        
        if choice == 'text':
            return input("Enter your text: ").strip()
        
        elif choice == 'file':
            file_path = input("Enter the file path: ").strip()
            if not os.path.isabs(file_path):
                file_path = os.path.abspath(file_path)
            if not os.path.isfile(file_path):
                print("The file does not exist. Please check the file path and try again.")
                continue
            try:
                with open(file_path, 'r') as file:
                    return file.read().lower().strip()
            except Exception as e:
                print(f"Error reading file: {e}")
                retry = input("Do you want to try again? (yes/no): ").strip().lower()
                if retry != 'yes':
                    return None
        else:
            print("Invalid choice. Please enter 'text' or 'file'.")

while True:
    text_data = input_text_or_file()
    if text_data:
        n = int(input("Enter the value of n for n-grams (e.g., 2 for bigrams, 3 for trigrams): ").strip())
        sentences, word_counts, ngram_counts, total_words_count, total_unique_words_count = preprocess_text_data(text_data, n)
        
        print(f"\nProcessing {len(sentences)} sentences...\n")
        
        for sentence in sentences:
            try:
                probability = smooth_sentence_prob(sentence, sentences, word_counts, ngram_counts, total_words_count, total_unique_words_count, n)
                sentence_perplexity = perplexity(probability, len(splitToWords(sentence)))
                
                print(f"Sentence: '{sentence}'")
                print(f"Probability: {probability}")
                print(f"Perplexity: {sentence_perplexity}\n")
            
            except ValueError as e:
                print(f"Error: {e}")
        
    else:
        print("No valid text data provided.")

    retry = input("Do you want to enter another text or file? (yes/no): ").strip().lower()
    if retry != 'yes':
        break

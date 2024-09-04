# N-Gram Language Model

## Overview

This Python script implements an n-gram language model, designed to calculate sentence probabilities and perplexities. It supports n-gram sizes like bigrams, trigrams, etc., and includes smoothing techniques to handle unseen n-grams. The script is versatile, allowing for text input either manually or from a file.

## Features

- **N-Gram Generation**: Supports various n-gram sizes (e.g., bigrams, trigrams).
- **Probability Calculation**:
  - Basic probability estimation based on n-gram frequency.
  - Smoothed probability calculation using additive (Laplace) smoothing.
- **Perplexity Calculation**: Measures how well the model predicts a given sentence, with safeguards to avoid infinite values.
- **User Interaction**: Offers a choice between manual text input or using a text file.

## Getting Started

### Prerequisites

- Python 3.x
- No external libraries are required, as the code uses Python’s standard library.

### Installation

Clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/ngram-language-model.git
cd ngram-language-model
```

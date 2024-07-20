import nltk
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

nltk.download('words')
from nltk.corpus import words

tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2LMHeadModel.from_pretrained('gpt2')

english_words = set(words.words())


def generate_possible_words(letters):
    possible_words = set()
    for word in english_words:
        if len(word) == len(letters):
            possible_words.add(word)
    return possible_words


def score_word(word, letters):
    input_text = " ".join(letters)
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    word_ids = tokenizer.encode(word, return_tensors='pt')

    with torch.no_grad():
        outputs = model(input_ids)
        predictions = outputs[0]

    word_score = 0
    for i, word_id in enumerate(word_ids[0]):
        word_score += torch.nn.functional.softmax(predictions[0, i], dim=-1)[word_id].item()

    return word_score


def find_best_word(letters):
    possible_words = generate_possible_words(letters)
    best_word = None
    best_score = -float('inf')

    for word in possible_words:
        score = score_word(word, letters)
        if score > best_score:
            best_word = word
            best_score = score

    return best_word

scanned_char = ['U','B','T','E','C','H']
best_word = find_best_word(scanned_char)
print(f"Từ có nghía: {best_word}")
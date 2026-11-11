# -*- coding: utf-8 -*-
"""
Hangman v2.0 - Language selection + frequency-based word choice with POS & semantic category (NLTK version)
Original: 2020
Updated: 10/11/2025
Author: Avtomat Agentics
"""

# Ignore warnings to keep console output clean
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# Import necessary libraries
from random import choice
from wordfreq import top_n_list, word_frequency
from textblob import TextBlob
import unicodedata
from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize
import nltk

# Download required NLTK data if missing
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)


# POS tag explanation dictionaries
POS_EXPLAIN = {
    "en": {
        "NN": "Noun",
        "NNS": "Plural noun",
        "VB": "Verb (base form)",
        "VBD": "Verb (past tense)",
        "VBG": "Verb (gerund/present participle)",
        "VBN": "Verb (past participle)",
        "VBP": "Verb (non-3rd person singular present)",
        "VBZ": "Verb (3rd person singular present)",
        "JJ": "Adjective",
        "JJR": "Comparative adjective",
        "JJS": "Superlative adjective",
        "RB": "Adverb",
        "RBR": "Comparative adverb",
        "RBS": "Superlative adverb",
        "IN": "Preposition",
        "DT": "Determiner / Article",
        "PRP": "Pronoun",
        "UH": "Interjection",
    },
    "es": {
        "NN": "Sustantivo",
        "NNS": "Sustantivo plural",
        "VB": "Verbo (forma base)",
        "VBD": "Verbo (pasado)",
        "VBG": "Verbo (gerundio)",
        "VBN": "Verbo (participio)",
        "VBP": "Verbo (presente)",
        "VBZ": "Verbo (presente 3ª persona)",
        "JJ": "Adjetivo",
        "JJR": "Adjetivo comparativo",
        "JJS": "Adjetivo superlativo",
        "RB": "Adverbio",
        "RBR": "Adverbio comparativo",
        "RBS": "Adverbio superlativo",
        "IN": "Preposición",
        "DT": "Determinante / Artículo",
        "PRP": "Pronombre",
        "UH": "Interjección",
    }
}


def get_word(language="en", freq_threshold=1e-6, min_length=5):
    """
    Selects a random word from wordfreq that has a frequency above the threshold.
    If Spanish is chosen, translates the word.
    Returns the word and its frequency.
    """

    english_words = top_n_list("en", 10000)

    while True:
        word = choice(english_words)

        if len(word) >= min_length and word.isalpha():
            freq = word_frequency(word, "en")

            if freq >= freq_threshold:
                if language == "es":
                    try:
                        translated = TextBlob(word).translate(from_lang="en", to="es")
                        translated = ''.join(
                            c for c in unicodedata.normalize('NFD', str(translated))
                            if unicodedata.category(c) != 'Mn'
                        )
                        return translated.lower(), freq, word
                    except Exception:
                        continue
                else:
                    return word.lower(), freq, word


def interpret_frequency(freq):
    """
    Interprets a frequency value into a qualitative label.
    """
    if freq >= 1e-4:
        return "very common"
    elif freq >= 1e-5:
        return "common"
    elif freq >= 1e-6:
        return "medium"
    elif freq >= 1e-7:
        return "uncommon"
    else:
        return "rare"


def get_pos(word, language):
    """
    Returns the syntactic category (POS tag) of a word using NLTK,
    with human-readable explanation in the selected language.
    """
    tokens = word_tokenize(word)
    tagged = pos_tag(tokens)
    tag = tagged[0][1]
    meaning = POS_EXPLAIN.get(language, POS_EXPLAIN["en"]).get(tag, "Unknown")
    return tag, meaning


def get_semantic_category(word, language):
    """
    Returns a general semantic category using WordNet hypernyms.
    Translates the semantic label to Spanish if necessary.
    """
    synsets = wn.synsets(word)
    if not synsets:
        category = "Unknown" if language == "en" else "Desconocido"
        return category

    first_synset = synsets[0]
    hypernyms = first_synset.hypernyms()
    if not hypernyms:
        category = "Generic" if language == "en" else "Genérico"
    else:
        category = hypernyms[0].lemma_names()[0]

    if language == "es":
        try:
            category = TextBlob(category).translate(from_lang="en", to="es")
            category = ''.join(
                c for c in unicodedata.normalize('NFD', str(category))
                if unicodedata.category(c) != 'Mn'
            )
        except Exception:
            pass
    return str(category)


def secret_word(word):
    """
    Converts the selected word into a secret pattern like _ _ _ _ _
    So that len(secret_word) = 2*len(word)
    """
    secret = ""
    for i in word:
        secret += "_ "
    return secret


def game(word, secret):
    """
    The main hangman game loop.
    """
    attempts = 6
    original_word = word
    not_in = []

    word = list(word)
    secret = list(secret)

    while attempts > 0:
        print("\nThis is the secret word:", "".join(secret))
        letter = input("Please, introduce a letter: ").lower()

        if letter in word:
            for idx, char in enumerate(word):
                if char == letter:
                    secret[idx * 2] = letter
                    word[idx] = "/"
            print("-----------------------------------------------------")
        else:
            attempts -= 1
            not_in.append(letter)
            fail(attempts, original_word)

            if attempts != 0 and attempts != 6:
                print("Letters that are not in the word:")
                print(", ".join(not_in))
                print("-----------------------------------------------------")

        if "_" not in secret:
            print("YOU WIN!")
            print("The word was", "'", original_word, "'")
            break


def fail(attempts, word):
    """
    Draws the hangman figure for each failed attempt.
    """
    fails = {
        5: """
    ______
     |    |
     o    |
          |
          |
    ______|       
    """,
        4: """
    ______
     |    |
     o    |
     |    |
          |
    ______|       
    """,
        3: """
    ______
     |    |
     o    |
    /|    |
          |
    ______|       
    """,
        2: """
    ______
     |    |
     o    |
    /|\   |
          |
    ______|       
    """,
        1: """
    ______
     |    |
     o    |
    /|\   |
    /     |
    ______|       
    """,
        0: """
    ______
     |    |
     o    |
    /|\   |
    /\    |
    ______|       
    """
    }

    if attempts in fails:
        print(fails[attempts])
    if attempts == 0:
        print("GAME OVER!")
        print("The word was:", word)


# Main execution block
if __name__ == "__main__":
    print("=====================================")
    print("           HANGMAN v2.1")
    print("=====================================")
    print("Choose language / Elige idioma:")
    print("1. English")
    print("2. Español")
    lang_choice = input("Select 1 or 2: ")

    if lang_choice == "1":
        print("\nLanguage: English")
        language = "en"
    elif lang_choice == "2":
        print("\nIdioma: Español")
        language = "es"
    else:
        print("Invalid option. Defaulting to English.")
        language = "en"

    selected_word, freq, english_word = get_word(language=language, freq_threshold=1e-6, min_length=5)
    hidden_word = secret_word(selected_word)

    # Linguistic info (POS + semantic)
    tag_code, tag_meaning = get_pos(english_word, language)
    semantic_category = get_semantic_category(english_word, language)

    print("\nSelected word details:")
    print(f"POS: {tag_meaning} ({tag_code})")
    print(f"Semantic category: {semantic_category}")
    print(f"Frequency: {freq:.2e} ({interpret_frequency(freq)})")

    game(selected_word, hidden_word)
# -*- coding: utf-8 -*-
"""
Hangman v3.0 — Streamlit Edition
Author: Avtomat Agentics
Updated: 10/11/2025

Description:
------------
A fully interactive Hangman game built with Streamlit. 
This version combines classic word guessing mechanics with natural 
language processing features such as part-of-speech (POS) tagging 
and semantic category extraction using NLTK and WordNet.

Features:
----------
- Interactive web-based Hangman game using Streamlit.
- Automatically fetches random English words and optionally translates them into Spanish.
- Displays POS (part of speech), semantic category, and frequency of the chosen word.
- Supports both English and Spanish interface.
- Tracks guesses, wrong letters, and ASCII hangman progress.
- Includes win/lose detection and a “Play Again” option to restart with a new word.

How to Run:
------------
From a terminal or Anaconda Prompt, execute:
    python -m streamlit run "C:\\path\\to\\ahorcado_v3.py"
"""

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# --- Core Imports ---
import streamlit as st
from random import choice
from wordfreq import top_n_list, word_frequency
from textblob import TextBlob
import unicodedata
from nltk.corpus import wordnet as wn
from nltk import pos_tag, word_tokenize
import nltk

# --- Ensure required NLTK datasets are available ---
nltk.download('punkt', quiet=True)
nltk.download('averaged_perceptron_tagger', quiet=True)
nltk.download('wordnet', quiet=True)

# Preload WordNet to avoid lazy-loading issues
from nltk.corpus import wordnet
_ = wordnet.synsets("test")

# POS tag explanation dictionaries (simplified)
POS_EXPLAIN = {
    "en": {"NN": "Noun", "VB": "Verb", "JJ": "Adjective", "RB": "Adverb"},
    "es": {"NN": "Sustantivo", "VB": "Verbo", "JJ": "Adjetivo", "RB": "Adverbio"},
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_word(language="en", freq_threshold=1e-6, min_length=5):
    """
    Selects a random English word from a frequency-based word list.
    Optionally translates it into Spanish using TextBlob if required.
    Filters out short or low-frequency words.
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
    """Converts numeric word frequency into a human-readable label."""
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
    Identifies the Part-of-Speech (POS) tag of a given word.
    Returns both the tag code (e.g., 'NN') and a readable label.
    """
    tokens = word_tokenize(word)
    tagged = pos_tag(tokens)
    tag = tagged[0][1]
    meaning = POS_EXPLAIN.get(language, POS_EXPLAIN["en"]).get(tag[:2], "Unknown")
    return tag, meaning


def get_semantic_category(word, language):
    """
    Retrieves the semantic category (hypernym) of a given word using WordNet.
    Optionally translates the category into Spanish.
    """
    synsets = wn.synsets(word)
    if not synsets:
        return "Unknown" if language == "en" else "Desconocido"
    hypernyms = synsets[0].hypernyms()
    category = hypernyms[0].lemma_names()[0] if hypernyms else "Generic"
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
    """Generates the masked version of the secret word as underscores."""
    return " ".join(["_"] * len(word))


def reset_game(language):
    """
    Resets the game session and generates a new random word.
    Clears all gameplay-related variables in session state.
    """
    selected_word, freq, english_word = get_word(language=language, freq_threshold=1e-6, min_length=5)
    st.session_state.selected_word = selected_word
    st.session_state.freq = freq
    st.session_state.english_word = english_word
    st.session_state.hidden_word = secret_word(selected_word)
    for key in ["attempts", "word", "secret", "not_in", "original_word", "game_over"]:
        st.session_state.pop(key, None)
    st.session_state.playing = True
    st.rerun()


# ============================================================
# GAME LOGIC
# ============================================================

def game(word, secret):
    """
    Main gameplay function. Handles user input, letter matching,
    hangman drawing, and win/lose state detection.
    """
    # Initialize session variables when the game starts
    if "attempts" not in st.session_state:
        st.session_state.attempts = 6
        st.session_state.word = list(word)
        st.session_state.secret = list(secret)
        st.session_state.not_in = []
        st.session_state.original_word = word
        st.session_state.game_over = False

    attempts = st.session_state.attempts
    word_list = st.session_state.word
    secret_list = st.session_state.secret
    not_in = st.session_state.not_in
    original_word = st.session_state.original_word

    # --- Display hangman state and current progress ---
    st.markdown("### Let's play Hangman!")
    fail(attempts)
    st.markdown(f"#### Word: `{''.join(secret_list)}`")

    # Show letters already guessed incorrectly
    if not_in:
        st.warning("Letters that are not in the word: " + ", ".join(not_in))

    # If the game has already ended, show final results
    if st.session_state.game_over:
        show_end_screen(original_word)
        return

    # --- Input Form for letter guessing ---
    with st.form("guess_form"):
        letter = st.text_input("Enter a letter:", max_chars=1)
        submit = st.form_submit_button("Try letter")

    if not submit or not letter:
        st.stop()

    letter = letter.lower()

    # Prevent repeated guesses
    if letter in not_in or letter in [c for c in original_word if c == "/"]:
        st.warning(f"You already tried '{letter}'.")
        st.stop()

    # --- Process guess result ---
    if letter in word_list:
        for idx, char in enumerate(word_list):
            if char == letter:
                secret_list[idx * 2] = letter
                word_list[idx] = "/"
        st.session_state.secret = secret_list
        st.session_state.word = word_list
        st.success(f"Good guess! '{letter}' is in the word.")
    else:
        not_in.append(letter)
        st.session_state.attempts -= 1
        st.session_state.not_in = not_in
        fail(st.session_state.attempts)
        st.error(f"Nope! '{letter}' is not in the word.")

    # --- Check for win or loss conditions immediately ---
    if "_" not in st.session_state.secret:
        st.session_state.game_over = True
        show_end_screen(original_word)
        return
    elif st.session_state.attempts <= 0:
        st.session_state.game_over = True
        show_end_screen(original_word)
        return

    # Refresh interface with updated state
    st.rerun()


def show_end_screen(word):
    """
    Displays the end-of-game screen, showing either a win or loss message.
    Includes a button to start a new game.
    """
    if "_" not in st.session_state.secret:
        st.balloons()
        st.success(f"🏆 YOU WIN! The word was '{word}'.")
    else:
        st.error(f"💀 GAME OVER! The word was '{word}'.")
        fail(0)
    btn = "🔁 Nueva partida" if st.session_state.language == "es" else "🔁 Play Again"
    if st.button(btn):
        reset_game(st.session_state.language)


def fail(attempts):
    """
    Draws the ASCII art hangman depending on remaining attempts.
    """
    fails = {
        6: r"""
    ______
     |    |
          |
          |
          |
    ______|       
    """,
        5: r"""
    ______
     |    |
     o    |
          |
          |
    ______|       
    """,
        4: r"""
    ______
     |    |
     o    |
     |    |
          |
    ______|       
    """,
        3: r"""
    ______
     |    |
     o    |
    /|    |
          |
    ______|       
    """,
        2: r"""
    ______
     |    |
     o    |
    /|\   |
          |
    ______|       
    """,
        1: r"""
    ______
     |    |
     o    |
    /|\   |
    /     |
    ______|       
    """,
        0: r"""
    ______
     |    |
     o    |
    /|\   |
    /\    |
    ______|       
    """
    }
    if attempts in fails:
        st.code(fails[attempts])


# ============================================================
# STREAMLIT USER INTERFACE
# ============================================================

st.title("Hangman v3.0")
st.write("**By Avtomat Agentics** — 2020 → 2025")

# --- Language selection ---
lang_choice = st.radio("Choose language / Elige idioma:", ["English", "Español"])
language = "en" if lang_choice == "English" else "es"
st.session_state.language = language

# --- Generate a random word only once per session ---
if "selected_word" not in st.session_state:
    selected_word, freq, english_word = get_word(language=language, freq_threshold=1e-6, min_length=5)
    st.session_state.selected_word = selected_word
    st.session_state.freq = freq
    st.session_state.english_word = english_word
    st.session_state.hidden_word = secret_word(selected_word)

# Retrieve stored session data
selected_word = st.session_state.selected_word
freq = st.session_state.freq
english_word = st.session_state.english_word
hidden_word = st.session_state.hidden_word

# --- Linguistic info panel ---
tag_code, tag_meaning = get_pos(english_word, language)
semantic_category = get_semantic_category(english_word, language)

st.markdown("### Word details:")
st.write(f"**POS:** {tag_meaning} ({tag_code})")
st.write(f"**Semantic category:** {semantic_category}")
st.write(f"**Frequency:** {freq:.2e} ({interpret_frequency(freq)})")

# --- Game control buttons ---
if "playing" not in st.session_state:
    st.session_state.playing = False

if st.button("Start Game"):
    st.session_state.playing = True
    st.session_state.game_over = False

# --- Run game ---
if st.session_state.playing:
    game(selected_word, hidden_word)
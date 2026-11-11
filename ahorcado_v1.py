# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 01:27:04 2020

@author: alvar
"""
#import some libraries that we need in more than one function
from random import choice



def list_words():
    
    """
    Create a list of all words in English. Previously, we have imported nltk
    and we have called to nltk.download() and have downloaded the word list.
    """
    
    from nltk.corpus import words
    word_list = words.words()
    # print(len(word_list)) Show how many words there are
    return word_list



def word_list_generator(word_list):
    
    """
    Choose randomly 5 words from the word_list (no more than 10, there's a 
    limit of translations with TextBlob)
    """
    
    short_word_list = []
    for i in range(5): #maximum range(11), range(3) to train
        word = choice(word_list)
        short_word_list.append(word)
    
    word_list = short_word_list
    # print(word_list)
    
    return word_list
    


def clean_list(spanish_list):

    """
    Remove from the list those words who has 4 or less letters.
    Also we should change the letters áéíóú for aeiou
    """

    for i in spanish_list:
        if len(i) < 5:
            spanish_list.remove(i)
    # print(spanish_list)
    return spanish_list



def word_generator(spanish_list):
    
    """
    Generates the word that we will have to guess. Randomly choices from the 
    Spanish word list.
    """
    
    palabra = choice(spanish_list).lower() #all in lower letters
    
    # print(palabra)
    return palabra
    

    
def translator(word_list):
    
    """
    Translate the words of the word_list to Spanish
    """
    
    from textblob import TextBlob
    
    spanish_list = [] #the Spanish words will be here
    
    for i in word_list:
        word = TextBlob(i)
        try:
            word_tran = word.translate(from_lang="en",to="es") #to Spanish
        except:
            word_tran = word #if can't translate word doesn't change
        spanish_list.append(str(word_tran)) #convert to string and append
    # print(spanish_list)
    
    return spanish_list



def secret_word(palabra):

    """
    Converts the word selected in a secret word like _ _ _ _ _
    So that len(secret_word) = 2*len(word)
    """

    secret = ""
    for i in palabra:
        secret += "_ "
    
    # print(secret)
        
    return secret



def game(palabra, secret):
    
    """
    The secret word appears like this _ _ _ _ to the player. Player is asked
    to introduce a letter to see if it is in the word. If it is, the word 
    is showed. If it is not, it calls to fail(). There are 6 attempts.
    As it is easier to work with lists rather than strings, we first convert
    to list, and finally we will come back to string with "".join(list)
    We introduce the letters that are not in a list
    """
    
    attempts = 6 #6 attempts before game over
    original_word = palabra
    not_in = []  #include the letters that are not in the word
    
    #we convert to a list:
    palabra = list(palabra)
    secret = list(secret)
    
    while attempts > 0:
        print("This is the secret word: ", "".join(secret))
        letter = input("Please, introduce a letter: ")
        
        if letter.lower() in palabra:
            #Get index of letter in the word
            while letter.lower() in palabra: #if it is repeated do it again
                index = palabra.index(letter.lower()) #get the first index
                secret[index*2] = letter.lower()  #add to secret word in index*2
                palabra[index] = "/" #we change letter to detect the next in case
                print("-----------------------------------------------------")
                
        else:
            attempts -= 1
            not_in.append(letter.lower())
            fail(attempts, original_word)
            
            if attempts != 0 and attempts != 6:
                print("Letters that are not in the word:")
                for i in not_in:
                    print(i)
                print("-----------------------------------------------------")
                
        if "_" not in secret:
            print("YOU WIN!")
            print("The word was", "'",original_word,"'")
            break
        

    # print("".join(palabra))
    # print("".join(secret))



def fail(attempts, palabra):
    
    """
    If we fail, it will appear the figure representing the man on the gallows 
    """
    
    fails_one = """
    ______
     |    |
     o    |
          |
          |
    ______|       
    """
    
    fails_two = """
    ______
     |    |
     o    |
     |    |
          |
    ______|       
    """
    
    fails_three = """
    ______
     |    |
     o    |
    /|    |
          |
    ______|       
    """
    
    fails_four = """
    ______
     |    |
     o    |
    /|\   |
          |
    ______|       
    """
    
    fails_five = """
    ______
     |    |
     o    |
    /|\   |
    /     |
    ______|       
    """
    
    fails_six = """
    ______
     |    |
     o    |
    /|\   |
    /\    |
    ______|       
    """
    
    if attempts == 5:
        print(fails_one)
    if attempts == 4:
        print(fails_two)
    if attempts == 3:
        print(fails_three)
    if attempts == 2:
        print(fails_four)
    if attempts == 1:
        print(fails_five)
    if attempts == 0:
        print(fails_six)
        print("GAME OVER!")
        print("The word was: ", palabra)



lw1 = list_words()
lw2 = word_list_generator(lw1)
tlw = translator(lw2)
clw = clean_list(tlw)
word = word_generator(clw)
sw = secret_word(word)
game(word, sw)
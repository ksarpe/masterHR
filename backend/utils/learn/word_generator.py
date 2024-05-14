import random
from config.constants import *

# It will grab the random word from the chapter and return it to the user.
# This list will be iterated over in the frontend to display the words to the user.
def get_words(chapter):
  words = []
  with open(CHAPTERS_PATH + f"/{chapter}.txt", "r") as f:
    words = f.readlines()
  
  words = [word.strip() for word in words]
  
  # shuffle the words before returning them
  random.shuffle(words)
  return words

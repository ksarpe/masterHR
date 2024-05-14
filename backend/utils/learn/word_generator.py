# It will grab the random word from the chapter and return it to the user.
# This list will be iterated over in the frontend to display the words to the user.
def get_words(chapter):
  words = []
  with open(f"backend/utils/learn/words/{chapter}.txt", "r") as f:
    words = f.readlines()
  return words

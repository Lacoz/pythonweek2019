def flip(word):
    flipped = []
    for i in range(len(word)):
        letter = word[len(word) - i - 1]
        flipped.append(letter)
    return "".join(flipped)

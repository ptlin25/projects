class Hangman():    
    def __init__(self, word):
        if not word.isalpha():
            raise Exception("Invalid word.")
        self.word = word.lower()
        self.revealed = ["_"] * len(word)
        self.stage = 0
        self.guessed = set()
    
    def guess(self):
        images = [
        """
        +---+
            |
            |
            |
            |
          =====
        """, 
        """
        +---+
        O   |
            |
            |
            |
          =====
        """,
        """
        +---+
        O   |
        |   |
            |
            |
          =====
        """,
        """
        +---+
        O   |
       /|   |
            |
            |
          =====
        """,
        """
        +---+
        O   |
       /|\  |
            |
            |
          =====
        """,
        """
        +---+
        O   |
       /|\  |
       /    |
            |
          =====
        """,
        """
        +---+
        O   |
       /|\  |
       / \  |
            |
          =====
        """
        ]

        letter = input("Guess a letter.\n")
        letter = letter.lower()
        if not letter.isalpha() or len(letter) != 1:
            print("Please guess a letter")
        elif letter in self.guessed:
            print("You have already guessed this letter.")
        else:
            self.guessed.add(letter)
            wrong = True
            for i, char in enumerate(self.word):
                if char == letter:
                    self.revealed[i] = char
                    wrong = False

            if wrong:
                self.stage += 1
        
            print(images[self.stage])
            print(self)
    
    def is_over(self):
        return self.stage == 6 or "".join(self.revealed) == self.word

    def __str__(self):
        return "".join(self.revealed)

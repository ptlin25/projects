from Hangman import Hangman

class HangmanRunner():
    def main():
        word = input("Enter the secret word. \n")
        game = Hangman(word)
        print(game)
         
        while not game.is_over():
            game.guess()

        if game.word == "".join(game.revealed):
            print("YOU WIN!")
        else:
            print("GAME OVER!")

    if __name__ == "__main__":
        main()
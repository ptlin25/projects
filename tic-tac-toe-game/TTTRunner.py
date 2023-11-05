from TicTacToe import TicTacToe

class TTTRunner:
    def main():
        game = TicTacToe()
        turn = 0
        
        while not game.is_full() and game.winner() is None:
            game.player_turn()
        if turn == 9:
            print("Tie")
        else:
            print(game.winner() + " wins!")
        
    if __name__ == "__main__":
        main()
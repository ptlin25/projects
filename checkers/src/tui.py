import click
from colorama import Fore, Back, Style

from checkers import CheckersGame, Board, PieceColor, Piece
from bot import randomBot, smartBot

class TUIPlayer:
    """
    Class that stores information about a TUI player

    The TUI player can either be a human or bot
    """
    def __init__(self, player_num, player, board, color, opponent_color,
    depth = 2):
        """
        Input:
            player_num (int): Player number (1 or 2)
            player (str): "human", "random-bot", or "smart-bot" 
            board (board): Checker's board
            color (PieceColor): player's color 
            opponent_color (PieceColor): opponent's color 
            depth (int): optional parameter that only applies to smart-bot 
            algorithm
        """
        self.color = color
        if player == "human":
            self.name = ("Player " + str(player_num) + 
            " (" + str(self.color) + ")")
            self.bot = None
        if player == "random-bot":
            self.name = ("Random Bot " + str(player_num) + 
            " (" + str(self.color) + ")")
            self.bot = randomBot(board, color)
        elif player == "smart-bot":
            self.name = ("Smart Bot " + str(player_num) + 
            " (" + str(self.color) + ")")
            self.bot = smartBot(board, color, depth)
        
        self.board = board
        self.opponent_color = opponent_color

    def get_movable_pieces(self):
        """
        Prompts the player for coordinates of the piece they want to select.
        If there is a movable piece at the given coordinates, it will print out
        all the valid moves for that piece

        Input: None

        Output: coordinates of the piece that's selected 
        (list[list[(tuple(int, int))])
        """   
        while True:
            user_input = input(self.name + 
            ": Insert coordinates of a piece: ")
            try:
                row = int(user_input.split(",")[0])
                col = int(user_input.split(",")[1])
                coord = (row, col)
                if coord in self.board.player_valid_moves(self.color):
                    moves = []
                for move in self.board.piece_valid_moves(coord):
                    moves.append(move) 
                print("Possible moves: " + str(moves))
                return coord
            except:
                continue
            
            
            
    def get_move(self, coords):
        """
        Prompt the player for the coordinates they want to move a piece to.
        If the coordinates the player wants to move to are valid, will move
        the piece. 

        Input:
            coords (tuple(int, int)): Takes in the starting coordinates of the 
            piece

        Output: None
        """
        while True:
            input_move = input(self.name + 
            ": Insert desired coordinates: ")
            try:
                row = int(input_move.split(",")[0])
                col = int(input_move.split(",")[1])
                final_coord = (row, col)
                if self.board.is_valid_move(self.color, coords, final_coord):
                    return final_coord
            except:
                continue
    

    def get_bot_move(self):
        """
        If the player is a bot, asks the bot to suggest a move, and 
        moves the bot to the suggested place.
        """
        if self.bot is not None:
            start, end = self.bot.suggest_move()
            self.board.move(self.color, start, end)
            print(str(self.name) + " moved \n" + "From:" + str(start) + 
            "\n" + "To:" + str(end))


def print_board(board):
    """
    Prints the board to the screen

    Input: 
        board: board to print

    Returns: None
    """
    grid = board.board_to_str()
    final = []
    string = ""

    #sets row coordinates on the top of the board
    rows = len(grid)
    for i in range(rows):
        if i < 10:
            string += "    " + Fore.WHITE + Style.NORMAL + str(i) + ""
        else:
            string += "   " + Fore.WHITE + Style.NORMAL + str(i) + ""
    final.append(string)
 
    for r, row in enumerate(grid):
        #sets the col coordinates on the left side of the board
        if r < 10:
            string = "" + Fore.WHITE + Style.NORMAL + str(r) + " "
        else:
            string = "" + Fore.WHITE + Style.NORMAL + str(r) + ""
    
        for c, col in enumerate(row):
            if r % 2 == c % 2:
                if col == " ":
                    string += Fore.WHITE + Style.NORMAL + "[   ]"
                elif col == "B":
                    string += (Fore.WHITE + "[ " + Fore.BLACK + Style.BRIGHT + 
                    "♔" + Fore.WHITE + " ]")
                elif col == "b":
                    string += (Fore.WHITE + "[ " + Fore.BLACK + Style.BRIGHT + 
                    "●" + Fore.WHITE + " ]")
                elif col == "R":
                    string += (Fore.WHITE + "[ " + Fore.RED + Style.BRIGHT + 
                    "♔" + Fore.WHITE + " ]")
                elif col == "r":
                    string += (Fore.WHITE + "[ " + Fore.RED + Style.BRIGHT + 
                    "●" + Fore.WHITE + " ]")
            else:
                if col == " ":
                    string += Fore.BLACK + Style.BRIGHT + "[   ]"
                elif col == "B":
                    string += (Fore.BLACK + "[ " + Fore.BLACK + Style.BRIGHT + 
                    "♔" + Fore.BLACK + " ]")
                elif col == "b":
                    string += (Fore.BLACK + "[ " + Fore.BLACK + Style.BRIGHT + 
                    "●" + Fore.BLACK + " ]")
                elif col == "R":
                    string += (Fore.BLACK + "[ " + Fore.RED + Style.BRIGHT + 
                    "♔" + Fore.BLACK + " ]")
                elif col == "r":
                    string += (Fore.BLACK + "[ " + Fore.RED + Style.BRIGHT + 
                    "●" + Fore.BLACK + " ]")
        final.append(string)
    print("\n".join(final))
    return "\n".join(final)


def play_checkers(board, players):
    """
    Plays a game of Checkers on the terminal

    Inputs:
        board (CheckersGame): board to play on
        players (Dict[PieceColor, TUIPlayer]): A dictionary mapping 
        piece colors to TUIPlayer objects

    Output: None
    """
    #starting player is black
    current = players[PieceColor.BLACK]

    #keep playing until there's a winner:
    while board.get_winner() is None:
        #prints the board
        print()
        print_board(board)
        print()
        
        if current.bot is not None:
            current.get_bot_move()
        else:
            coords = current.get_movable_pieces()
            dest = current.get_move(coords)
            board.move(current.color, coords, dest)

        #Update the player
        if not board.turn_incomplete():
            board.end_turn(current.color, "End Turn")
            if current.color == PieceColor.BLACK:
                current = players[PieceColor.RED]
            elif current.color == PieceColor.RED:
                current = players[PieceColor.BLACK]
    
    #prints the board
    print()
    print_board(board)

    #checks if there's a winner
    winner = board.get_winner()
    if winner == PieceColor.DRAW:
        print("It's a tie!")
    elif winner is not None:
        print("The winner is " + str(players[winner].name) + "!")

#
#Command-line interface
#

@click.command(name = "Checkers-tui")
@click.option('--player1',
              type = click.Choice(['human', 'random-bot', 'smart-bot'], 
              case_sensitive=False), default = "human")
@click.option('--player2',
              type=click.Choice(['human', 'random-bot', 'smart-bot'], 
              case_sensitive = False), default = "human")
@click.option('--piece_rows', required = True, prompt = True,
type = click.Choice(["2", "3", "4", "5", "6", "7", "8", "9"]))

def cmd(piece_rows, player1, player2):
    if piece_rows == "2":
        board = CheckersGame(2)
    elif piece_rows == "3":
        board = CheckersGame(3)
    elif piece_rows == "4":
        board = CheckersGame(4)
    elif piece_rows == "5":
        board = CheckersGame(5)
    elif piece_rows == "6":
        board = CheckersGame(6)
    elif piece_rows == "7":
        board = CheckersGame(7)
    elif piece_rows == "8":
        board = CheckersGame(8)
    elif piece_rows == "9":
        board = CheckersGame(9)

    player1 = TUIPlayer(1, player1, board, PieceColor.BLACK, 
    PieceColor.RED)
    player2 = TUIPlayer(2, player2, board, PieceColor.RED, 
    PieceColor.BLACK)

    players = {PieceColor.BLACK: player1, PieceColor.RED: player2}

    play_checkers(board, players)

if __name__ == "__main__":
    cmd()



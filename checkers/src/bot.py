from checkers import CheckersGame, PieceColor
from copy import deepcopy
import random
import click

class randomBot():
    """
    Class for bot that suggests random moves.
    """
    def __init__(self, board, color):
        """
            Constructor

            board (Game obj): board that bot will play on
            color (PieceColor obj): color of the pieces the bot will play with 
        """
        self._board = board
        self._color = color

    def suggest_move(self):
        """
        Randomly selects a piece and randomly selects out of the viable paths
        from the piece can choose to take.

        Parameters:
            None

        Returns:
            tuple(tuple, tuple): first tuple represents starting coordinates of 
            the random piece, second tuple represents end coordinates of the 
            random path
        """
        valid_moves = list(self._board.player_valid_moves(self._color).items())
        rand_piece = random.choice(valid_moves)
        rand_path = random.choice(rand_piece[1])
        start, end = rand_piece[0], rand_path[-1]
        return start, end

class smartBot():
    """
    Class for bot that uses Minimax algorithm to suggest moves.
    """
    def __init__(self, board, color, depth):
        """
            Constructor

            board (Game obj): board that bot will play on
            color (PieceColor obj): color of the pieces the bot will play with 
            depth (int): depth of the Minimax algorithm
        """
        self._board = board
        self._color = color
        self._depth = depth
    
    def suggest_move(self):
        """
        Calls the private method _minimax() to return the coordinates of the 
        piece that should be moved and where it should be moved to.

        Parameters:
            None

        Returns:
            tuple(tuple, tuple): first tuple represents starting coordinates of 
            Minimax chosen piece, second tuple represents end coordinates of 
            Minimax chosen path
        """
        move = self._minimax(self._board, self._depth, self._color)
        start, end = move[0], move[1]
        return start, end

        
    def _minimax(self, board, depth, color):
        """
        Minimax algorithm that traverses a tree of paths given a starting 
        position and bottoms up to the root, returning the next best move for 
        the bot. At each node, depending on the color, the algorithm will
        maximize/minimize the values of the level of nodes below it and obtain
        the move needed to reach that minimal/maximal position. 
        
        I have consulted the following resource to gain a better understanding 
        about the algorithm: https://www.youtube.com/watch?v=l-hh51ncgDI&t=73s,
        https://www.youtube.com/watch?v=STjW3eH0Cik

        Parameters:
            board (Game obj): board that bot will play on
            depth (int): the number of moves that the bot thinks ahead
            color (PieceColor obj): color of the pieces the bot will play with 

        Returns:
            tuple(tuple, tuple, int): first tuple represents starting 
            coordinates of Minimax chosen piece, second tuple represents end 
            coordinates of Minimax chosen path, third tuple represents 
            evaluation of the board
        """
        # Base case --> leaf of tree (depth has been fully explored)
        if depth == 0: 
            return None, None, board.evaluate()
        
        if color == PieceColor.BLACK:
            # Maximize eval value for "BLACK"
            max_val = -float('inf')
            start_coord = None
            best_move = None
            # Consider all paths for a given position
            for start, paths in board.player_valid_moves(color).items():
                for path in paths:
                    end = path[-1]
                    # Use deepycopy so original board is not affected when a 
                    # move is made
                    tmp_board = deepcopy(board)
                    tmp_board.move(color, start, end)
                    # Recurses a level below. "BLACK" will try to maximize the
                    # values of the nodes in this level
                    _, _, val = self._minimax(tmp_board, depth - 1, PieceColor.RED)
                    if val > max_val:
                        max_val = val
                        start_coord = start
                        best_move = end
            return start_coord, best_move, max_val

        if color == PieceColor.RED:
            # Minimize eval value for "RED"
            min_val = float('inf')
            start_coord = None
            best_move = None
            for start, paths in board.player_valid_moves(color).items():
                for path in paths:
                    end = path[-1]
                    tmp_board = deepcopy(board)
                    tmp_board.move(color, start, end)
                    # Recurses a level below. "RED" will try to minimize the
                    # values of the nodes in this level
                    _, _, val = self._minimax(tmp_board, depth - 1, PieceColor.BLACK)
                    if val < min_val:
                        min_val = val
                        start_coord = start
                        best_move = end
            return start_coord, best_move, min_val



# SIMULATION

class BotPlayer:
    """
    Class to store information about a bot player in a simulation.
    """
    def __init__(self, board, color, depth):
        """ 
            Constructor
        
            board (Game obj): board that bot player will play on
            color (PieceColor obj): color of bot player
            depth (int): depth decides identity of bot player (depth = 0 
                signifies bot player is randomBot, depth > 0 signifies bot
                player is smartBot)
        """
        self.depth = depth

        if self.depth == 0:
            self.bot = randomBot(board, color)
        elif self.depth > 0:
            self.bot = smartBot(board, color, depth)
        self.color = color
        self.wins = 0

def simulate(board, n, bots, playout_mode=False):
    """ 
    Simulates multiple games between two bots.

    Parameters:
        board (Game obj): board that bot players will play on
        n (int): number of simulated games
        bots (dict): dictionary that maps PieceColor obj to BotPlayer obj
        playout_mode (bool): 'True' shows live playout of game

    Returns:
        None
    """
    for _ in range(n):
        # Reset the board
        board.setup()
        # i represents ith move of game
        i = 1
    
        # The starting player is Black
        current = bots[PieceColor.BLACK]

        # While the game doesn't recognize a winner, make a move
        while not board.get_winner():
            start, end = current.bot.suggest_move()
            if playout_mode:
                print(f"{i} {start} {end}")
            board.move(current.color, start, end)
            
            # Update the player
            if current.color == PieceColor.BLACK:
                current = bots[PieceColor.RED]
            elif current.color == PieceColor.RED:
                current = bots[PieceColor.BLACK]

            i += 1
            
        winner = board.get_winner()

        if winner is not None:
            if winner == PieceColor.BLACK:
                if playout_mode:
                    print("Black wins")
                    print()
                bots[winner].wins += 1
            if winner == PieceColor.RED:
                if playout_mode:
                    print("Red wins")
                    print()
                bots[winner].wins += 1
            if winner == PieceColor.DRAW:
                if playout_mode:
                    print("Draw")
                    print()
     
@click.command()
@click.option('-n', '--n',  type=click.INT, default=10)
@click.option('-d1', '--depth_1',  type=click.INT, default=0)
@click.option('-d2', '--depth_2',  type=click.INT, default=0)
@click.option('-r', '--row',  type=click.INT, default=3)
@click.option('-p', '--playout_mode', type=click.BOOL, default=False)
def cmd(n, row, depth_1, depth_2, playout_mode):
    """
        Shows win-rate between bot players and if playout_mode is 'True' shows 
        live game.

        Parameters:
            n (int): number of games
            row (int): row of pieces for board
            depth_1 (int): depth for smartBot (depth is 0 --> use randomBot)
            depth_2 (int): depth for smartBot (depth is 0 --> use randomBot)
            playout_mode (bool): 'True' shows live playout of game

        Returns:
            None
    """
    board = CheckersGame(row)

    bot1 = BotPlayer(board, PieceColor.BLACK, depth_1)
    bot2 = BotPlayer(board, PieceColor.RED, depth_2)

    bots = {PieceColor.BLACK: bot1, PieceColor.RED: bot2}

    simulate(board, n, bots, playout_mode)

    bot1_wins = bots[PieceColor.BLACK].wins
    bot2_wins = bots[PieceColor.RED].wins
    ties = n - (bot1_wins + bot2_wins)
    
    print(f"Bot 1 wins (Depth = {depth_1}): {100 * bot1_wins / n:.2f}%")
    print(f"Bot 2 wins (Depth = {depth_2}): {100 * bot2_wins / n:.2f}%")
    print(f"Ties: {100 * ties / n:.2f}%")

if __name__ == "__main__":
    cmd()



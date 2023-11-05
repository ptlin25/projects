"""
Classes for implementing a checkers game with varying board size
(supports 6x6 up to 20x20).

Examples:
    1. Create new Checkers Board

        game = CheckersGame(nrows)

    2. Check whether a given move is legal

        game.is_valid_dest(start, end)

    3. Obtain all valid moves of a piece:

        game.piece_valid_moves(coords)

    4. List of all possible moves a player can make

        game.player_valid_moves(color)

    5. Check whether there's a winner and who

        game.get_winner()
"""
from typing import Optional, List, Tuple, Dict, Set
from enum import Enum
PieceColor = Enum("PieceColor", ["RED", "BLACK", "DRAW"])
"""
Enum type for representing piece colors.
"""

class Piece:
    """
    Class for representing a piece.
    """

    #
    # PRIVATE ATTRIBUTES
    #
        
    # color of the piece        
    _color: PieceColor

    # if the piece is a king
    _king: bool

    #
    # PUBLIC METHODS
    #
    
    def __init__(self, color: PieceColor):
        """
        Constructor
    
        Parameters:
            color (PieceColor): color of the piece
        """
        self._color = color
        self._king = False

    def get_color(self) -> PieceColor:
        """
        Gets the color of the piece.
    
        Parameters:
            None

        Returns:
            PieceColor: color of the given piece
        """
        return self._color

    def is_king(self) -> bool:
        """
        Returns if the piece is a king or not.
    
        Parameters:
            None
    
        Returns:
            bool: returns True if the piece is a king, otherwise, returns False
        """
        return self._king
    
    def promote(self) -> None:
        """
        Promotes the piece to a king.
    
        Parameters:
            None
    
        Returns:
            None
        """
        self._king = True

class Board:
    """
    Class for representing a rectangular board.
    """

    #
    # PRIVATE ATTRIBUTES
    #
        
    # the board itself
    _grid: List[List[Optional[Piece]]]

    # number of rows and columns
    _nrows: int
    _ncols: int
        
    #
    # PUBLIC METHODS
    #

    def __init__(self, nrows: int, ncols: int):
        """
        Constructor

        Parameters:
            nrows (int): number of rows
            ncols (int): number of columns
        """
        self._grid = [[None] * ncols for _ in range(nrows)]
        self._nrows = nrows
        self._ncols = ncols

    def get(self, coord: Tuple[int, int]) -> Optional[Piece]:
        """
        Gets the piece at the given location if there is one.
    
        Parameters:
            coord (tuple(int, int)): location on the board
        
        Raises:
            ValueError: If the given location is not valid
        
        Returns:
            Optional[Piece]: the piece at the location if there is one
        """
        row, col = coord
        if not 0 <= row < self._nrows or not 0 <= col < self._ncols:
            raise ValueError("Invalid coordinates")
        
        return self._grid[row][col]

    def set(self, coord: Tuple[int, int], piece: Optional[Piece]) -> None:
        """
        Sets the location on the board to the given piece.

        Parameters:
            coord (tuple (int, int)): location on the board
            piece (Piece): given piece to be set

        Raises:
            ValueError: If the given location is invalid
    
        Returns:
            None
        """
        row, col = coord
        if not 0 <= row < self._nrows or not 0 <= col < self._ncols:
            raise ValueError("Invalid coordinates")

        self._grid[row][col] = piece
    
    def remove(self, coord: Tuple[int, int]) -> None:
        """
        Removes the piece at the given location.

        Paramters:
            coord (tuple (int, int)): location on the board
    
        Raises:
            ValueError: If the given location is invalid or if there is not a
            piece at the given location
    
        Returns:
            None
        """
        if self.get(coord) is None:
            raise ValueError("No piece to remove at this coordinate")
        
        self.set(coord, None)

    def move(self, start: Tuple[int, int], end: Tuple[int, int]) -> None:
        """
        Moves the pieces at the start location to the end location.
    
        Parameters:
            start (tuple (int, int)): initial location of piece to be moved
            end (tuple (int, int)): final location of the piece

        Raises:
            ValueError: If there is no piece at the starting location or there
            is already a piece at the final location
    
        Returns:
            None
        """
        if self.get(start) is None:
            raise ValueError("No piece at the starting position")
        
        piece = self.get(start)
        self.remove(start)
        self.set(end, piece)

    def board_to_str(self) -> List[List[str]]:
        """
        Returns the board as a list of list of strings.

        Parameters:
            None
        
        Returns:
            list[list[str]]: a list of list of strings with the same dimensions
            as the board. In each row, the values in the list will be " " 
            (no piece), "B" (black king piece), "b" (black non-king piece), "R"
            (red king piece), "r" (red non-king piece).
        """
        str_grid = []
        for row in self._grid:
            new_row = []
            for square in row:
                if square is None:
                    new_row.append(" ")
                elif (square.get_color() == PieceColor.BLACK and
                      square.is_king()):
                    new_row.append("B")
                elif (square.get_color() == PieceColor.BLACK and
                      not square.is_king()):
                    new_row.append("b")
                elif (square.get_color() == PieceColor.RED and
                      square.is_king()):
                    new_row.append("R")
                elif (square.get_color() == PieceColor.RED and
                      not square.is_king()):
                    new_row.append("r")
            str_grid.append(new_row)
        return str_grid

    def get_num_rows(self) -> int:
        """
        Returns the number of rows in the board.

        Parameters:
            None
        
        Returns:
            int: number of rows
        """
        return self._nrows

    def get_num_cols(self) -> int:
        """
        Returns the number of columns in the board.

        Parameters:
            None
        
        Returns:
            int: number of cols
        """
        return self._ncols

class CheckersGame:
    """
    Class for representing a game of checkers.    
    """

    #
    # PRIVATE ATTRIBUTES
    #
    
    # board of the game
    _board: Board

    # number of rows of pieces
    _rows: int

    # list of locations of pieces on the board
    _black_piece_coords: List[Tuple[int, int]]
    _red_piece_coords: List[Tuple[int, int]]

    # location of piece that is in the middle of a jump
    _jumping: Optional[Tuple[int, int]]

    # winner of the game if there is one
    _winner: Optional[PieceColor]

    # True if a draw has been offered, otherwise False
    _draw_offered: bool

    # number of moves since the last capture
    _black_moves_since_capture: int
    _red_moves_since_capture: int

    #
    # PUBLIC METHODS
    #
    
    def __init__(self, nrows: int):
        """
        Constructor

        Parameters:
            nrows (int): number of rows of pieces each player begins the game
            with
        """
        self._board = Board(2 * nrows + 2, 2 * nrows + 2)
        self._rows = nrows
        self._black_piece_coords = []
        self._red_piece_coords = []
        self._jumping = None
        self._winner = None
        self._draw_offered = False
        self._black_moves_since_capture = 0
        self._red_moves_since_capture = 0

        self.setup()

    def __str__(self) -> str:
        """
        Returns a basic string representation of the Game object's board.

        Parameters:
            None

        Returns:
            str: basic string representation fo the Game object's board
        """
        board_string = ""
        for row in self.board_to_str():
            for cell in row:
                board_string += cell
            board_string += "\n"
        return board_string

    def board_to_str(self) -> List[List[str]]:
        """
        Returns the game's board as a list of list of strings.

        Parameters:
            None

        Returns:
            list[list(str)]: A list of lists with the same dimensions as the
            board. In each row, the values in the list will be " " (no piece),
            "B" (black king piece), "b" (black non-king piece), "R" (red kings
            piece), "r" (red non-king piece).
        """
        return self._board.board_to_str()

    def setup(self) -> None:
        """
        Creates the board of the correct size and places the pieces on the
        correct squares of the board. Black pieces will be placed on the first n
        rows of the board and red pieces will be placed on the last n rows of
        the board.

        Parameters:
            None
        
        Returns:
            None
        """
        height = self._board.get_num_rows()
        width = self._board.get_num_cols()

        # reset instance variables
        self._black_piece_coords = []
        self._red_piece_coords = []
        self._winner = None
        self._jumping = None
        self._black_moves_since_capture = 0
        self._red_moves_since_capture = 0

        for r in range(height):
            for c in range(width):
                if r < self._rows and r % 2 != c % 2:
                    self._black_piece_coords.append((r, c))
                    self._board.set((r, c), Piece(PieceColor.BLACK))
                elif r >= height - self._rows and r % 2 != c % 2:
                    self._red_piece_coords.append((r, c))
                    self._board.set((r, c), Piece(PieceColor.RED))
                else:
                    self._board.set((r, c), None)
    
    def move(self, color: PieceColor, start: Tuple[int, int], 
            end: Tuple[int, int]) -> None:
        """
        Player of the given color inputs a position of a piece and a location to
        move the piece to. If the given move is valid, the move will be
        executed. Otherwise, the player wll be prompted to input a different
        move.

        Parameters:
            color (PieceColor): player color
            start: the position of piece to be moved
            end (tuple(int, int)): destination position

        Raises:
            Value if index is not on the board or the selected move is invalid

        Returns:
            None 
        """
        if not self.is_valid_move(color, start, end):
            raise ValueError("Invalid move")
        
        if self._require_jump(color):   # jump move
            for move in self.piece_valid_moves(start):
                if end in move:
                    if end == move[-1]: # complete jump move
                        self._jumping = None
                    else:   # incomplete jump move
                        self._jumping = end
                    
                    current = start
                    for step in move[: move.index(end) + 1]:
                        self._piece_jump_to(color, current, step)
                        current = step
                    break

            # reset moves since last capture counter
            if color == PieceColor.BLACK:
                self._black_moves_since_capture = 0
            elif color == PieceColor.RED:
                self._red_moves_since_capture = 0

        else:   # non-jump move
            self._piece_move_to(color, start, end)
            self._jumping = None

            # increment moves since last capture counter by 1
            if color == PieceColor.BLACK:
                self._black_moves_since_capture += 1
            elif color == PieceColor.RED:
                self._red_moves_since_capture += 1

        # check for promotion
        self._check_promote(color, end)

        # update winner after complete player turn
        if not self.turn_incomplete():
            self._update_winner(color)

    def player_valid_moves(self,
                           color: PieceColor) -> Dict[Optional[Tuple[int, int]],
                                                   List[List[Tuple[int, int]]]]:
        """
        Returns all the complete valid moves (jumps or non-jump moves) for all
        the available specified colored pieces.

        Parameters:
            color (PieceColor): player's color

        Returns:
            dict{tuple(int, int): list[list[tuple(int, int)]]}: dictionary of
            all the complete valid moves the player of the given color can make
            where the keys are the coordinates of a piece that can be moved and
            the values are the list of complete valid moves the player can make
            with each piece.
        """
        moves = {}
        
        if (self.turn_incomplete() and
                self._board.get(self._jumping).get_color() == color):
            moves[self._jumping] = self._get_all_jumps(self._jumping)
            return moves

        piece_coords = []
        if color == PieceColor.BLACK:
            piece_coords = self._black_piece_coords
        elif color == PieceColor.RED:
            piece_coords = self._red_piece_coords

        if self._require_jump(color):
            for coord in piece_coords:
                if self._get_all_jumps(coord):
                    moves[coord] = self._get_all_jumps(coord)

        else:
            for coord in piece_coords:
                if self._get_all_non_jumps(coord):
                    moves[coord] = self._get_all_non_jumps(coord)

        return moves

    def piece_valid_moves(self, coord: Tuple[int, int]) -> List[List
                                                            [Tuple[int, int]]]:
        """
        Returns all the complete valid moves for the given piece.

        Parameters:
            coord (tuple(int, int)): position of the given piece

        Returns:
            list[list[tuple(int, int)]]: list of all the possible moves the
            given piece can move to
        """
        if self._get_all_jumps(coord):
            return self._get_all_jumps(coord)
        else:
            return self._get_all_non_jumps(coord)

    def is_valid_move(self, color: PieceColor, start: Tuple[int, int],
            end: Tuple[int, int]) -> bool:
        """
        Determines if the move is a possible move at the given color's player's
        current turn. 

        Parameters:
            color: color of the player
            start: coordinates of the piece to be moved
            end: coordinates of the destination location of the move

        Returns:
            bool: returns True if the given move is valid, otherwise, returns
            False
        """
        if start not in self.player_valid_moves(color):
            return False
        else:
            for moves in self.piece_valid_moves(start):
                if end in moves:
                    return True
            return False

    def is_valid_dest(self, start: Tuple[int, int],
                      end: Tuple[int, int]) -> bool:
        """
        Given a location of a piece on the board and a location to move the
        piece to, determines if the move is valid or not, regardless of other
        pieces.

        Parameters:
            start (tuple(int, int)): position of the piece
            end (tuple(int, int)): destination position

        Returns:
            bool: returns True if the move is valid, otherwise, returns False
        """
        for moves in self.piece_valid_moves(start):
            if moves[-1] == end:
                return True
        return False

    def turn_incomplete(self) -> bool:
        """
        Boolean value for if the turn is incomplete, meaning the player has not
        completed all possible successive jumps.

        Parameters:
            None

        Returns:
            bool: True if the turn is incomplete, otherwise returns False
        """
        return self._jumping is not None
    
    def is_draw_offered(self) -> bool:
        """
        Returns true if a draw has been offered. Otherwise, returns false/

        Parameters:
            None

        Returns:
            bool: True if a draw has been offered, otherwise returns False
        """
        return self._draw_offered

    def end_turn(self, color: PieceColor, cmd: str) -> None:
        """
        Method for ending a player's turn. The player can choose to resign,
        offer a draw, or simply end their current turn.

        Parameters:
            color (PieceColor): current player's color
            cmd (str): the player's command to end turn, resign, or offer draw

        Returns:
            None
        """
        if cmd == "End Turn":   
            pass
        elif cmd == "Resign":
            if color == PieceColor.BLACK:
                self._winner = PieceColor.RED
            elif color == PieceColor.RED:
                self._winner = PieceColor.BLACK
        elif cmd == "Offer Draw":
            self._draw_offered = True
    
    def accept_draw(self, cmd: str) -> None:
        """
        Method for player to either accept or decline a draw offered by the
        other player.

        Parameters:
            cmd (str): command for accepting or declining a draw
        
        Returns:
            None
        """
        if cmd == "Accept":
            self._winner = PieceColor.DRAW
        else:
            self._draw_offered = False

    def get_winner(self) -> Optional[PieceColor]:
        """
        Find the winner of the game and the color won, if it exists.

        Parameters:
            None

        Returns:
            PieceColor or None: If there is a winner, return the color. If it is
            a tie, returns PieceColor.DRAW. Otherwise, return None.
        """
        return self._winner
    
    def evaluate(self) -> float:
        """
        Evaluates the value of the current position. The more positive the value
        the more favorable the position is for player with the black pieces. The
        more negative the value, the more favorable the position is for player 
        with the red pieces. 

        Parameters:
            None

        Returns:
            value (float): value of current position
        """
        black_king, black_nonking, red_king, red_nonking = self._composition()
        value = ((black_nonking - red_nonking) +
                 (0.5 * black_king - 0.5 * red_king))
        return value

    #
    # PRIVATE METHODS
    #
    
    def _piece_move_to(self, color: PieceColor, start: Tuple[int, int],
                       end: Tuple[int, int]) -> None:
        """
        Moves the piece at the given location and updates the piece's positon on
        the board.

        Parameters:
            color (PieceColor): color of the piece being moved
            start (tuple(int, int)): the location of the piece to be moved
            end(tuple(int, int)): position the peice is moving to

        Returns:
            None
        """
        self._board.move(start, end)
        if color == PieceColor.BLACK:
            self._black_piece_coords.remove(start)
            self._black_piece_coords.append(end)
        elif color == PieceColor.RED:
            self._red_piece_coords.remove(start)
            self._red_piece_coords.append(end)
    
    
    def _piece_jump_to(self, color: PieceColor, start: Tuple[int, int],
                       end: Tuple[int, int]) -> None:
        """
        Jumps with the piece at the given location and updates the piece's
        positon on the board.

        Parameters:
            color (PieceColor): color of the piece being moved
            start (tuple (int, int)): the lcoation of the piece to be moved
            end(tuple(int, int)): position the peice is moving to

        Raises:
            ValueError: Jump is invalid

        Returns:
            None
        """
        start_row, start_col = start
        end_row, end_col = end
        jump_over = (int((start_row + end_row) / 2), 
                int((start_col  + end_col) / 2))
        
        self._board.move(start, end)
        self._board.remove(jump_over)

        if color == PieceColor.BLACK:
            self._black_piece_coords.remove(start)
            self._black_piece_coords.append(end)
            self._red_piece_coords.remove(jump_over)
        elif color == PieceColor.RED:
            self._red_piece_coords.remove(start)
            self._red_piece_coords.append(end)
            self._black_piece_coords.remove(jump_over)

    def _get_all_jumps(self,
                        start: Tuple[int, int]) -> List[List[Tuple[int, int]]]:
        """"
        Given a location on the board, returns a list of all the possible
        complete jumps the piece at that location can make where the coordinates
        of each sqaure the piece jumps to during the path is stored in a list. 

        Parameters:
            start_position: position of the peice

        Raises:
            ValueError: if there is no piece at the given starting position

        Returns:
            list(list(tuple(int, int))): list of moves the piece can make
        """
        piece = self._board.get(start)
        if piece is None:
            raise ValueError("No piece at starting position")
        return self._get_complete_jumps(start, piece.get_color(),
                                        piece.is_king(), set())
    
    def _get_all_non_jumps(self,
                        start: Tuple[int, int]) -> List[List[Tuple[int, int]]]:
        """
        Given a piece on the board, returns a list of positions the piece can
        non-jump move to. This does not include places the piece can move to
        with a jump since that is in the _piece_valid_jump method. It will also
        take into consideration if the piece is a king or not.

        Parameters:
            start (tuple(int, int)): location of the piece

        Raises:
            ValueError: if there is no piece at the given starting position

        Returns:
            list[list[tuple(int, int)]]: all possible places the given piece can
            non-jump move to
        """
        valid_moves = []
        row, col = start
        piece = self._board.get(start)
        if piece is None:
            raise ValueError("No piece at starting position")

        if piece.get_color() == PieceColor.BLACK or piece.is_king():
            try:
                dest = (row + 1, col + 1)
                if self._board.get(dest) is None:
                    valid_moves.append([dest])
            except ValueError:
                pass

            try:
                dest = (row + 1, col - 1)
                if self._board.get(dest) is None:
                    valid_moves.append([dest])
            except ValueError:
                pass

        if piece.get_color() == PieceColor.RED or piece.is_king():
            try:
                dest = (row - 1, col + 1)
                if self._board.get(dest) is None:
                    valid_moves.append([dest])
            except ValueError:
                pass

            try:
                dest = (row - 1, col - 1)
                if self._board.get(dest) is None:
                    valid_moves.append([dest])
            except ValueError:
                pass

        return valid_moves

    def _get_complete_jumps(self, start: Tuple[int, int], color: PieceColor,
            king: bool,
            jumped: Set[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
        """
        Given a position on the board, a color, king status, and a set of
        locations that have already been jumped over, returns a list of all the
        possible complete moves that can be made from the given starting
        position.

        Parameters:
            start (tuple(int, int)): row and column information of the starting
            position on the board
            color (PieceColor): given color
            king (bool): if the piece is a king (can move in both directions)
            jumped (set(tuple(int, int))): set of locations that have already
            been jumped over.

        Returns:
            list[list[tuple(int, int)]]: list of moves a piece with the given
            details can make
        """
        if self._get_single_jumps(start, color, king, jumped) == {}:
            return []
        else:
            paths = []
            for pos, jumped_over in self._get_single_jumps(start, color, king,
                                                           jumped).items():
                sub_paths = self._get_complete_jumps(pos, color, king,
                                                     jumped | {jumped_over})
                if sub_paths == []:
                    paths.append([pos])
                else:
                    for sub_path in sub_paths:
                        paths.append([pos] + sub_path)
            return paths

    def _get_single_jumps(self, start: Tuple[int, int], color: PieceColor,
            king: bool, jumped: Set[Tuple[int, int]]) -> Dict[Tuple[int, int],
                                                              Tuple[int, int]]:
        """
        Given a starting position on the board, a color, king status, and a set
        of locations that have already been jumped over, returns a dictionary of
        the possible single jumps a move with the given details can make. The
        keys of the dictionary are the possible locations that can be jumped to
        and the values of the dictionary are sets of locations that must be
        jumped over to reach each destination.

        Parameters:
            start (tuple(int, int)): starting location on the board
            color (PieceColor): given piece color
            king (bool): king status of the given piece
            jumped (set(tuple(int, int))): set of locations that have already
            been jumped over

        Returns:
            dict{tuple(int, int): tuple(int, int)}: dictionary storing the
            possible end locations and the locations being jumped over
        """
        row, col = start
        valid = {}

        if color == PieceColor.BLACK or king:
            try:
                dest = (row + 2, col + 2)
                jump_over = (row + 1, col + 1)
                if (self._board.get(dest) is None and
                        self._board.get(jump_over) is not None and
                        self._board.get(jump_over).get_color() != color and
                        jump_over not in jumped):
                    valid[dest] = jump_over
            except ValueError:
                pass

            try:
                dest = (row + 2, col - 2)
                jump_over = (row + 1, col - 1)
                if (self._board.get(dest) is None and
                        self._board.get(jump_over) is not None and
                        self._board.get(jump_over).get_color() != color and
                        jump_over not in jumped):
                    valid[dest] = jump_over
            except ValueError:
                pass
            
        if color == PieceColor.RED or king:
            try:
                dest = (row - 2, col + 2)
                jump_over = (row - 1, col + 1)
                if (self._board.get(dest) is None and
                        self._board.get(jump_over) is not None and
                        self._board.get(jump_over).get_color() != color and
                        jump_over not in jumped):
                    valid[dest] = jump_over
            except ValueError:
                pass
                
            try:
                dest = (row - 2, col - 2)
                jump_over = (row - 1, col - 1)
                if (self._board.get(dest) is None and
                        self._board.get(jump_over) is not None and
                        self._board.get(jump_over).get_color() != color and
                        jump_over not in jumped):
                    valid[dest] = jump_over
            except ValueError:
                pass

        return valid

    def _require_jump(self, color: PieceColor) -> bool:
        """
        Given a player color returns a boolean if the player must make a jump
        with his or her turn. 

        Parameters:
            color (PieceColor): player color

        Returns:
            bool: if the player must make a jump with his or her turn
        """
        if (self.turn_incomplete() and
                self._board.get(self._jumping).get_color() == color):
            return True

        if color == PieceColor.BLACK:
            pieces = self._black_piece_coords
        else:
            pieces = self._red_piece_coords

        for coord in pieces:
            if self._get_all_jumps(coord):
                return True
        return False

    def _composition(self) -> Tuple[int, int, int, int]:
        """
        Returns the number of kings and nonking pieces each player currently has
        on the board.

        Parameters:
            None

        Returns:
            tuple (int, int, int, int): tuple of four integers; the first
            integer is the number of black king pieces on the board, the second
            integer is the number of black nonking pieces on the board, the
            third integer is the number of red king pieces on the board, and the
            fourth integer is the number of red nonking pieces on the board. 
        """
        black_king, black_nonking = 0, 0
        red_king, red_nonking = 0, 0

        for row in self._board.board_to_str():
            for piece in row:
                if piece == "B":
                    black_king += 1
                elif piece == "b":
                    black_nonking += 1
                elif piece == "R":
                    red_king += 1
                elif piece == "r":
                    red_nonking +=1 

        return black_king, black_nonking, red_king, red_nonking
    
    def _check_promote(self, color: PieceColor, coord: Tuple[int, int]) -> None:
        """
        Checks if the piece at the given position should be promoted to a king.

        Parameters:
            color (PieceColor): color of the given piece
            coord (Tuple[int, int]): position of the given piece

        Returns:
            None
        """
        row, _ = coord
        if ((color == PieceColor.BLACK and
                row == self._board.get_num_rows() - 1) or
                (color == PieceColor.RED and row == 0)):
            self._board.get(coord).promote()

    def _update_winner(self, color: PieceColor) -> None:
        """
        Checks if the given player has won the game or the game has reached a
        draw.

        Parameters:
            color (PieceColor): player color

        Returns:
            None
        """
        if (color == PieceColor.BLACK and
                self.player_valid_moves(PieceColor.RED) == {}):
            self._winner = PieceColor.BLACK
        elif (color == PieceColor.RED and
                self.player_valid_moves(PieceColor.BLACK)  == {}):
            self._winner = PieceColor.RED
        # check for draw
        elif (self._black_moves_since_capture >= 40 or
                self._red_moves_since_capture >= 40):
            self._winner = PieceColor.DRAW

# Checkers  
This checkers game implementation supports custom board sizes from 6x6 to 20x20

## Setup  
I recommend setting up a virtual environment to install the libraries required
to run the code in this repository. To setup a virtual environment, run the
following from the root of the repository.

    python3 -m venv venv  

To activate your virtual environment, run the following:

    source venv/bin/activate  

To install the required Python libraries run the following:  

    pip3 install -r requirements.txt  

To deactivate the virtual environment, run the following:

    deactivate

## Running the TUI 
To run the TUI, run the following from the root of the repository:

    python3 src/tui.py

The TUI first asks for the number of rows of pieces in order to create the 
correct board size. It then displays the state of the board. Starting with 
black, it asks the player for a piece they want to move. You must specify the
coordinates of the piece in this form: row, col. If the given piece is movable, 
it will ask for the desired coordinates of the piece in this form: row, col. If 
the coordinates are not valid, you will be prompted for a new set of 
coordinates. 

You can also play against a bot like this:

    python3 src/tui.py --player2 {bot}

Where {bot} is either random-bot or smart-bot

You can even have two bots play against each other:

    python3 src/tui.py --player1 {bot} --player2 {bot}

Where {bot} is either random-bot or smart-bot

There is no aftificial delay between each bot's move.  

## Running the GUI  
To run the GUI, run the following from the root of the repository:

    python3 src/gui.py

The GUI will initially ask for the number of rows of pieces in order to create the board size of the accurate dimensions. The GUI will then display the current state of the board. To move a piece, the current and selected piece's valid moves will be highlighted, and the player can select where they want to move (out of the valid moves).

Like the TUI, you can play against a bot, or have two bots play against each other:

    python3 src/gui.py --player2 {bot}

    python3 src/gui.py --player1 {bot} --player2 {bot}

Where {bot} is either random-bot or smart-bot  
The --bot delay {seconds} parameter is also supported.

## Bots  
The ``bots.py`` file includes two classes:

- ``RandomBot``: A bot that will just choose a move at random
- ``SmartBot``: A bot that uses the Minimax algorithm to make a move, which is given a depth that is the number of moves the algorithm will see ahead. The higher the depth, the more informed of a move the bot will make. It is recommended to set the depth to at least 4 to see its dominant effect when playing against a random bot. Keep in mind that a high depth like 4 paired with a high number of simulated games will correspond to a slower runtime.

The two classes are used in the TUI and GUI, but you can also run ``bots.py`` to run simulated games where two bots face each other, and see the percentage of wins and ties. For example:

    $ python3 src/bot.py -n 1000
        Bot 1 wins (Depth = 0): 43.80%
        Bot 2 wins (Depth = 0): 51.30%
        Ties: 4.90%
        
    $ python3 src/bot.py -n 1000 -d1 2
        Bot 1 wins (Depth = 2): 83.70%
        Bot 2 wins (Depth = 0): 1.60%
        Ties: 14.70%

You can control the identity of the bot through the depth value using the ``-d1 <depth value>`` or ``-d2 <depth value>`` parameter. A bot with depth of 0 will use the RandomBot class whereas a bot with depth greater than 0 will use the SmartBot. 

You can also control the number of simulated games using the ``-n <number of games>`` parameter, the board's initial state using the ``-r <number of rows of pieces>`` parameter, and whether you would like to see a live playout of the simulated games using the ``-p <True/False>``.

The default values are d1=0, d2=0, n=10, r=3, p=False.



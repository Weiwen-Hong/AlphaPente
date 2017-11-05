"""
Game rules for Pente
"""

# Constants
EMPTY = 1
PLAYERX = 2
PLAYERO = 3 
DRAW = 4

# Map player constants to letters for printing
STRMAP = {EMPTY: " ",
          PLAYERX: "X",
          PLAYERO: "O"}

class PenteBoard:
    """
    Class to represent a Pente board.
    """

    def __init__(self, dim, reverse = False, board = None):
        self._dim = dim
        self._reverse = reverse
        if board == None:
            # Create empty board
            self._board = [[EMPTY for dummycol in range(dim)] 
                           for dummyrow in range(dim)]
        else:
            # Copy board grid
            self._board = [[board[row][col] for col in range(dim)] 
                           for row in range(dim)]
            
    def __str__(self):
        """
        Human readable representation of the board.
        """
        rep = ""
        for row in range(self._dim):
            for col in range(self._dim):
                rep += STRMAP[self._board[row][col]]
                if col == self._dim - 1:
                    rep += "\n"
                else:
                    rep += " | "
            if row != self._dim - 1:
                rep += "-" * (4 * self._dim - 3)
                rep += "\n"
        return rep

    def get_dim(self):
        """
        Return the dimension of the board.
        """
        return self._dim
    
    def square(self, row, col):
        """
        Return the status (EMPTY, PLAYERX, PLAYERO) of the square at
        position (row, col).
        """
        return self._board[row][col]

    def get_empty_squares(self):
        """
        Return a list of (row, col) tuples for all empty squares
        """
        empty = []
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col] == EMPTY:
                    empty.append((row, col))
        return empty

    def move(self, row, col, player):
        """
        Place player on the board at position (row, col).

        Does nothing if board square is not empty.
        """
        if self._board[row][col] == EMPTY:
            self._board[row][col] = player

    def check_win(self):
        """
        If someone has won, return player.
        If game is a draw, return DRAW.
        If game is in progress, return None.
        """
        board = self._board
        dim = self._dim
        dimrng = range(dim)
        lines = []
        
        # put each column into a list to check whether there are five in a row
        for rowidx in dimrng:
          col = [board[rowidx][colidx] for colidx in dimrng]
          for x in range(dim-5):
            if (col[x]==col[x+1] and col[x]==col[x+2] and col[x]==col[x+3] and
                col[x]==col[x+4]):
                return col[x]
        
        # put each row into a list to check whether there are five in a row
        for colidx in dimrng:
          row = [board[rowidx][colidx] for rowidx in dimrng]
          for x in range(dim-5):
            if (row[x]==row[x+1] and row[x]==row[x+2] and row[x]==row[x+3] and
                row[x]==row[x+4]):
                return row[x]

        diag1 = []
        diag2 = []
        diag3 = []
        diag4 = []

        for idx in dimrng:
          # on row idx
          for col in range(dim-1-idx):
            # i.e. (3,0) (4,1) (5,2)...
            diag1.append(board[idx+col][col]) 
            # i.e. (0,2) (1,3) (2,4)...
            diag2.append(board[col][idx+col])
            if len(diag1) > 4:
              for x in (range(0,len(diag1))):
                if (diag1[x]==diag1[x+1] and diag1[x]==diag1[x+2] and 
                  diag1[x]==diag1[x+3] and diag1[x]==diag1[x+4]):
                  return diag1[x]
                if (diag2[x]==diag2[x+1] and diag2[x]==diag2[x+2] and 
                  diag2[x]==diag2[x+3] and diag2[x]==diag2[x+4]):
                  return diag2[x]

          # on col idx
          for row in range(dim-1-idx):
            # i.e. (0,7) (1,6) (2,5)...
            diag3.append(board[row][idx-row])
            # i.e. (2,8) (3,7) (4,6)
            diag4.append(board[idx+row][dim-1-row])
            if (len(diag1) > 4):
              for x in (range(0,len(diag1))):
                if (diag3[x]==diag3[x+1] and diag3[x]==diag3[x+2] and 
                  diag3[x]==diag3[x+3] and diag3[x]==diag3[x+4]):
                  return diag3[x]
                if (diag4[x]==diag4[x+1] and diag4[x]==diag4[x+2] and 
                  diag4[x]==diag4[x+3] and diag4[x]==diag4[x+4]):
                  return diag4[x]       
          

        # no winner, check for draw
        if len(self.get_empty_squares()) == 0:
            return DRAW

        # game is still in progress
        return None
            
    def clone(self):
        """
        Return a copy of the board.
        """
        return PenteBoard(self._dim, self._reverse, self._board)

def switch_player(player):
    """
    Convenience function to switch players.
    
    Returns other player.
    """
    if player == PLAYERX:
        return PLAYERO
    else:
        return PLAYERX

def play_game(mc_move_function, ntrials, reverse = False):
    """
    Function to play a game with two MC players.
    """
    # Setup game
    board = PenteBoard(3, reverse)
    curplayer = PLAYERX
    winner = None
    
    # Run game
    while winner == None:
        # Move
        row, col = mc_move_function(board, curplayer, ntrials)
        board.move(row, col, curplayer)

        # Update state
        winner = board.check_win
        curplayer = switch_player(curplayer)

        # Display board
        print board
        print
        
    # Print winner
    if winner == PLAYERX:
        print "X wins!"
    elif winner == PLAYERO:
        print "O wins!"
    elif winner == DRAW:
        print "Tie!"
    else:
        print "Error: unknown winner"

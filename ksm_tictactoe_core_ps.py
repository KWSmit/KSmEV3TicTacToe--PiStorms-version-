''' Core functionality for ksm_tictactoe_ps.'''
import cv2
import numpy as np


class Board:
    ''' Tic tac toe board.'''
    def __init__(self):
        # Field indexes
        self.index = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        # Field boundaries
        self.x0 = 72  # 90
        self.y0 = 60  # 90
        self.x1 = 150  # 180
        self.y1 = 135  # 180
        # Define symbols for human player and computer
        self.HU_PLAYER = 'O'
        self.AI_PLAYER = 'X'

    def reset(self):
        ''' Reset board for new game: empty all indexes.'''
        self.index = [0, 1, 2, 3, 4, 5, 6, 7, 8]

    def empty_indexes(self):
        ''' Return all empty indexs.'''
        empty_index = []
        for i in range(0, 9):
            if str(self.index[i]) != 'X' and str(self.index[i]) != 'O':
                empty_index.append(i)
        return empty_index

    def check_for_winner(self, player):
        ''' Check if player is a winner.'''
        if (self.index[0] == player and self.index[1] == player and self.index[2] == player) or \
           (self.index[3] == player and self.index[4] == player and self.index[5] == player) or \
           (self.index[6] == player and self.index[7] == player and self.index[8] == player) or \
           (self.index[0] == player and self.index[3] == player and self.index[6] == player) or \
           (self.index[1] == player and self.index[4] == player and self.index[7] == player) or \
           (self.index[2] == player and self.index[5] == player and self.index[8] == player) or \
           (self.index[0] == player and self.index[4] == player and self.index[8] == player) or \
           (self.index[2] == player and self.index[4] == player and self.index[6] == player):
            return True
        else:
            return False

    def add_human_move_to_board(self, x, y):
        ''' Determine index of human move. '''
        if x < self.x0:
            if y < self.y0:
                self.index[0] = 'O'
            elif y > self.y0 and y < self.y1:
                self.index[3] = 'O'
            elif y > self.y1:
                self.index[6] = 'O'
        elif x > self.x0 and x < self.x1:
            if y < self.y0:
                self.index[1] = 'O'
            elif y > self.y0 and y < self.y1:
                self.index[4] = 'O'
            elif y > self.y1:
                self.index[7] = 'O'
        elif x > self.x1:
            if y < self.y0:
                self.index[2] = 'O'
            elif y > self.y0 and y < self.y1:
                self.index[5] = 'O'
            elif y > self.y1:
                self.index[8] = 'O'


def minimax(new_board, player):
    ''' Implementation of the minimax algorithm.'''

    # Array to store al move objects
    moves = []

    # Object to store index and score of each available spot
    move = {}
    best_move = {}
    result = {}

    # Determine all available spots on the board
    spots = new_board.empty_indexes()

    # Check for terminal states, such as win, lose and tie and
    # return value accordingly
    if new_board.check_for_winner(new_board.HU_PLAYER):
        move['score'] = -10
        return move
    elif new_board.check_for_winner(new_board.AI_PLAYER):
        move['score'] = 10
        return move
    elif len(spots) == 0:
        move['score'] = 0
        return move

    # Loop through available spots
    for spot in spots:
        move['index'] = new_board.index[spot]

        # Set the empty spot to the current player
        new_board.index[spot] = player

        # Collect the score resulted from calling minimax
        # on the opponent of the current player
        if player == new_board.AI_PLAYER:
            result = minimax(new_board, new_board.HU_PLAYER)
            move['score'] = result['score']
        else:
            result = minimax(new_board, new_board.AI_PLAYER)
            move['score'] = result['score']

        # Reset the spot to empty again
        new_board.index[spot] = move['index']

        # Append a copy of move to array moves
        moves.append(move.copy())

    # Determine the best move
    if player == new_board.AI_PLAYER:
        # If it's the computers turn, loop over the moves
        # and choose the move with the highest score
        best_score = -1000
        for m in moves:
            if m['score'] > best_score:
                best_score = m['score']
                best_move = m
    else:
        # If it's the computers turn, loop over the moves
        # and choose the move with the highest score
        best_score = 1000
        for m in moves:
            if m['score'] < best_score:
                best_score = m['score']
                best_move = m

    # Return the best move
    return best_move


def human_moves_from_image(camera, board):
    '''Detect alle human moves (circles) in picture. '''
    nr_circles = 0
    font = cv2.FONT_HERSHEY_SIMPLEX

    # capture image and save to file
    camera.capture('ttt.jpg')

    # Read image and preprocess for circle detection
    img = cv2.imread('ttt.jpg')

    # Resize image to region of interest (tic tac toe board only)
    img = img[150: 350, 410: 630]

    # Convert to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Adaptive Guassian Threshold is to detect sharp edges in the Image.
    gray_img = cv2.adaptiveThreshold(gray_img, 255,
                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 11, 3.5)

    # apply GuassianBlur to reduce noise. medianBlur is also added for
    # smoothening, reducing noise.
    gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0)
    gray_img = cv2.medianBlur(gray_img, 5)

    # Circle detection (= moves of human player)
    circles = cv2.HoughCircles(gray_img, cv2.HOUGH_GRADIENT, 1.2, 50,
                               param1=200, param2=50,
                               minRadius=10, maxRadius=50)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for (x, y, r) in circles[0, :]:
            nr_circles += 1
            # Draw the outer circle
            cv2.circle(img, (x, y), r, (0, 255, 0), 2)
            # Draw the center if the circle
            cv2.circle(img, (x, y), 2, (0, 0, 255), 3)
            # Put number of circle at center
            cv2.putText(img, str(nr_circles), (x, y), font, 2, 255)
            # Add human move to board
            board.add_human_move_to_board(x, y)
        cv2.imwrite('ttt_circles.jpg', img)
        return nr_circles, board
    else:
        return nr_circles, board

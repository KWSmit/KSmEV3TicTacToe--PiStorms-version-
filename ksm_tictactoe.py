#!/usr/bin/env python3
#
# Game of Tic Tac Toe with PiStorms v2, LEGO Mindstorms,
# Raspberry Pi 3B and picamera.
# Build with ev3dev.
#
# Author:  Kees Smit, 2018
# Website: ksmev3.wordpress.com
#
# Hardware:
# - PiStorms v2 / Raspberry Pi3B
# - PiCamera
# - LEGO LargeMotor connected to port BAM1
# - LEGO LargeMotor connected to port BBM1
# - LEGO LargeMotor connected to port BBM2
# - LEGO MediumMotor connected to port BAM2
# - LEGO TouchSensor connected to port BAS1
# - LEGO TouchSensor connected to port BAS2
# - LEGO TouchSensor connected to port BBS2
#

from os import environ
from time import sleep

from picamera import PiCamera

from ksm_tictactoe_core_ps import Board, minimax, human_moves_from_image
from ksm_tictactoe_userinterface import show_start_screen, show_start_menu, \
     show_end_screen, show_message
from ksm_tictactoe_lego_devices import Tic_tac_toe_machine

# Picamera
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()

# Tic tac toe board
board = Board()

# Tic tac toe machine
m = Tic_tac_toe_machine()

#
# Gameplay
#

# Show start screen
show_start_screen()

# Start game
while True:

    # Show start menu and ask which player will start the game
    start_player = show_start_menu()
    if start_player == 'STOP_PROGRAM':
        show_end_screen()
        break
    elif start_player == 'AI_PLAYER':
        show_message('The computer will start...', 2)
        computer = True

    else:
        show_message('Human player will start...', 2)
        computer = False

    # Reset board
    board.reset()

    # Each game has 9 moves to play
    for move in range(0, 9):

        if computer:
            # It's computer's turn
            show_message('Wait for the computer\nto make its move...', 0)

            if move < 1:
                # Computer plays first, place X on index 0
                board.index[0] = board.AI_PLAYER
                computer = False
                # Draw computer move
                m.draw_computer_move(0)
                show_message('Computer move: 0', 0)
            else:
                result = minimax(board, board.AI_PLAYER)
                board.index[result['index']] = board.AI_PLAYER
                computer = False

                # TODO: implement drawing computer move
                m.draw_computer_move(result['index'])
                show_message('Computer move:' + str(result['index']), 0)

        else:
            # It's the human's turn
            show_message('It is your turn.\nMake a move and press TouchSensor', 0)

            # Wait for human player to make his move and press TouchSenor
            m.ts_play.wait_for_bump(timeout_ms=None)

            # Detect human move by using PiCamera
            nr_circles, board = human_moves_from_image(camera, board)
            show_message('Aantal: {}'.format(nr_circles), 2)
            computer = True

        # Debug: show board
        show_message('{}-{}-{}\n{}-{}-{}\n{}-{}-{}'.format(board.index[0],
                                                           board.index[1],
                                                           board.index[2],
                                                           board.index[3],
                                                           board.index[4],
                                                           board.index[5],
                                                           board.index[6],
                                                           board.index[7],
                                                           board.index[8]), 5)
        # Check for a winner
        if board.check_for_winner(board.HU_PLAYER):
            show_message('Congratulations, you won!!', 4)
            break
        elif board.check_for_winner(board.AI_PLAYER):
            show_message('The computer has won!!', 4)
            break

        # If move = 8 and there is no winner, it's a tie
        if move == 8:
            show_message('It is a tie!!', 4)

    start_player = ''

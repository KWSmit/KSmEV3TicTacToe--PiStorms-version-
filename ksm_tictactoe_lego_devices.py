#!/usr/bin/env python3
#
# Game of Tic Tac Toe with PiStorms v2, LEGO Mindstorms,
# Raspberry Pi 3B and picamera.
# Build with ev3dev.
#
# Author:  Kees Smit, 2018
# Website: kwsmit.github.io
#
# Hardware:
# - PiStorms v2 / Raspberry Pi3B
# - PiCamera
# - LEGO LargeMotor connected to port BAM1
# - LEGO LargeMotor connected to port BBM1
# - LEGO LargeMotor connected to port BBM2
# - LEGO MediumMotor connected to port BAM2
# - LEGO TouchSensor connected to port BAS2
# - LEGO TouchSensor connected to port BBS2
#
from time import sleep

from ev3dev2.port import LegoPort
from ev3dev2.motor import Motor, LargeMotor, OUTPUT_D
from ev3dev2.sensor.lego import TouchSensor

# Configure ports for sensors
port_BAS2 = LegoPort('pistorms:BAS2')
port_BAS2.mode = 'ev3-analog'
port_BBS2 = LegoPort('pistorms:BBS2')
port_BBS2.mode = 'ev3-analog'
sleep(2)


class ExceededRetries(Exception):
    ''' Custom exception for exceeding retries at Remote I/O error.'''
    pass


def try_except(func):
    ''' Retry function when Remote I/O error occurs.'''
    def wrapper(*args, **kwargs):
        for i in range(10):
            try:
                result = func(*args, **kwargs)
                return result
            except OSError:
                with open('logfile.txt', 'a') as f:
                    f.write('OSError\n')
        raise ExceededRetries('ExceededRetries in function ' + func.__name__)
    return wrapper


class Tic_tac_toe_machine:
    def __init__(self):
        self.turntable = Turntable('pistorms:BAM1', 'pistorms:BAM2')
        self.pen = Pen('pistorms:BBM2', 'pistorms:BBM1')
        self.ts_play = TouchSensor('pistorms:BAS2')

    @try_except
    def draw_computer_move(self, field_index):
        ''' Draw the move (cross) of computer.'''
        # Move pen to given field
        self._move_to_field(field_index)
        # Draw cross
        self._draw_cross()
        # Goto start position
        self.turntable.goto_start_pos()

    @try_except
    def _move_to_field(self, field_index):
        ''' Move turntable and pen to given field (private method).'''
        #        turntable   pen
        # field  turn  move  move
        # 0      1     5     3
        # 1      1     4     2
        # 2      1     3     1
        # 3      1     4     4
        # 4      1     3     3
        # 5      1     2     2
        # 6      1     3     5
        # 7      1     2     4
        # 8      1     1     3
        field = ((1, 5, 3),
                 (1, 4, 2),
                 (1, 3, 1),
                 (1, 4, 4),
                 (1, 3, 3),
                 (1, 2, 2),
                 (1, 3, 5),
                 (1, 2, 4),
                 (1, 1, 3))

        # move to field
        self.turntable.turn_to_abs_pos(field[field_index][0])
        self.turntable.move_to_abs_pos(field[field_index][1])
        self.pen.move_to_abs_pos(field[field_index][2])
        wait_while_motors_running(self.turntable.motor_move,
                                  self.turntable.motor_turn,
                                  self.pen.motor_move)

    @try_except
    def _draw_cross(self):
        ''' Draw a cross at given field_index).'''
        # Bring pen down to paper
        self.pen.pen_down()
        # Draw first line of cross
        self.turntable.motor_move.run_to_rel_pos(position_sp=200)
        wait_while_motors_running(self.turntable.motor_move)
        # Move pen up
        self.pen.pen_up()
        # Goto startpoint of second line of the cross
        self.turntable.motor_move.run_to_rel_pos(position_sp=-100)
        self.pen.motor_move.run_to_rel_pos(position_sp=-75)
        wait_while_motors_running(self.turntable.motor_move,
                                  self.pen.motor_move)
        # Bring pen down to paper
        self.pen.pen_down()
        # Draw second ling of the cross
        self.pen.motor_move.run_to_rel_pos(position_sp=175)
        wait_while_motors_running(self.pen.motor_move)
        # Move pen up
        self.pen.pen_up()


class Turntable:
    def __init__(self, port_motor_move, port_motor_turn):
        # Motor for moving turntable forwards and backwards
        self.motor_move = Motor(port_motor_move)
        self.motor_move.speed_sp = 400
        self.motor_move.stop_action = 'brake'
        self.motor_move_positions = (0, -740, -890, -1030, -1175, -1380)

        # Motor for rotating turntable
        self.motor_turn = Motor(port_motor_turn)
        self.motor_turn.speed_sp = 400
        self.motor_turn.stop_action = 'brake'
        self.motor_turn_positions = (0, -345, 345)

    @try_except
    def move_to_abs_pos(self, pos):
        ''' Move the turntable to given absolute position [0,..,5].'''
        self.motor_move.run_to_abs_pos(
                        position_sp=self.motor_move_positions[pos])

    @try_except
    def move_to_rel_pos(self, rel_pos):
        ''' Move the turntable over a given distance.'''
        self.motor_move.run_to_rel_pos(position_sp=rel_pos)  # rel_pos=150
        wait_while_motors_running(self.motor_move)

    @try_except
    def turn_to_abs_pos(self, pos):
        ''' Turn the turntable to a given absolute position [0,..,2].'''
        self.motor_turn.run_to_abs_pos(
                        position_sp=self.motor_turn_positions[pos])

    @try_except
    def goto_start_pos(self):
        ''' Move and turn the turntable to its start position.'''
        self.move_to_abs_pos(0)
        self.turn_to_abs_pos(0)


class Pen:
    def __init__(self, port_motor_move, port_motor_pen):
        # Motor to move pen sideways
        self.motor_move = LargeMotor(port_motor_move)
        self.motor_move.reset()
        self.motor_move.speed_sp = 400
        self.motor_move.stop_action = 'brake'
        self.motor_move_positions = (0, -60, -210, -350, -500, -640)
        # Motor te move pen up or down
        self.motor_pen = LargeMotor(port_motor_pen)
        self.motor_pen.stop_action = 'hold'
        # TouchSensor to indicate pen is up
        self.ts_pen = TouchSensor('pistorms:BBS2')
        # Move pen up
        self.motor_pen.run_forever(speed_sp=-200)
        self.ts_pen.wait_for_pressed()
        self.motor_pen.stop()

    @try_except
    def pen_up(self):
        ''' Move pen up.'''
        self.motor_pen.run_to_abs_pos(speed_sp=400, position_sp=-20)
        wait_while_motors_running(self.motor_pen)

    @try_except
    def pen_down(self):
        ''' Move pen down.'''
        self.motor_pen.run_to_abs_pos(speed_sp=400, position_sp=20)
        wait_while_motors_running(self.motor_pen)

    @try_except
    def move_to_abs_pos(self, pos):
        ''' Move pen sidways to absolute position [0,..,5].'''
        self.motor_move.run_to_abs_pos(
                        position_sp=self.motor_move_positions[pos])


@try_except
def wait_while_motors_running(*args):
    ''' Hold program when given motors are still running.'''
    for motor in args:
        pos = motor.position
        while True:
            sleep(0.3)
            current_pos = motor.position
            if pos == current_pos:
                break
            else:
                pos = current_pos

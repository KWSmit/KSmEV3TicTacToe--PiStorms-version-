''' All things related to userinterface on the screen of the PiStorms.'''

from os import environ
from time import sleep

from PIL import Image
from evdev import InputDevice
from ev3dev2.display import Display

# workaround for ev3dev-lang-python bug (issue #469)
environ['FRAMEBUFFER'] = '/dev/fb1'

display = Display()


def show_start_screen():
    ''' Show start screen.'''

    # Show start screen
    display.clear()
    logo = Image.open('images/start_screen.png')
    display.image.paste(logo, (0, 0))
    display.update()
    sleep(2)


def show_end_screen():
    ''' Show end screen.'''

    # Show end screen
    display.clear()
    logo = Image.open('images/end_screen.png')
    display.image.paste(logo, (0, 0))
    display.update()
    sleep(2)


def show_start_menu():
    ''' Show start menu.'''

    # Set input device to pistorms TouchScreen
    device = InputDevice('/dev/input/event2')

    # Initilize variables for x and y of screentouch
    abs_x = 0
    abs_y = 0
    start = None

    # Clear screen
    display.clear()
    display.update()

    # Menu text
    display.draw.rectangle((0, 10, 320, 50), fill='blue', outline='blue')
    display.text_pixels('Choose which player starts', clear_screen=False,
                        x=15, y=20, text_color='white', font='lutBS18')

    # Computer button
    display.draw.rectangle((15, 100, 150, 150), fill='white', outline='black')
    display.text_pixels('Computer', clear_screen=False, x=40, y=113,
                        text_color='black', font='lutBS18')

    # Human button
    display.draw.rectangle((170, 100, 305, 150), fill='white', outline='black')
    display.text_pixels('Human', clear_screen=False, x=215, y=113,
                        text_color='black', font='lutBS18')

    # Stop button
    display.draw.rectangle((85, 170, 220, 220), fill='white', outline='black')
    display.text_pixels('Stop', clear_screen=False, x=125, y=185,
                        text_color='black', font='lutBS18')

    # Update screen to show menu
    display.update()

    # Detect user input (touch on screen)
    abs_x_valid = False
    abs_y_valid = False
    valid_input = False

    for event in device.read_loop():
        if event.type == 3 and event.code == 0:
            # ABS_X event
            abs_x = event.value
            abs_x_valid = True
        elif event.type == 3 and event.code == 1:
            # ABS_Y event
            abs_y = event.value
            abs_y_valid = True
        elif event.code == 28:
            # PiStorms' GO-button pressed, stop program
            start = 'STOP_PROGRAM'
            break

        # Check which button is pressed and act accordingly
        if abs_x_valid and abs_y_valid:
            if abs_y > 100 and abs_y < 150:
                if abs_x > 15 and abs_x < 150:
                    display.draw.rectangle((15, 100, 150, 150),
                                           fill='black',
                                           outline='black')
                    display.text_pixels('Computer', clear_screen=False,
                                        x=40, y=113,
                                        text_color='white', font='lutBS18')
                    display.update()
                    start = 'AI_PLAYER'
                    valid_input = True
                elif abs_x > 180 and abs_x < 315:
                    display.draw.rectangle((170, 100, 305, 150),
                                           fill='black',
                                           outline='black')
                    display.text_pixels('Human', clear_screen=False,
                                        x=215, y=113,
                                        text_color='white', font='lutBS18')
                    display.update()
                    start = 'HU_PLAYER'
                    valid_input = True
            elif abs_y > 170 and abs_y < 220:
                if abs_x > 85 and abs_x < 220:
                    display.draw.rectangle((85, 170, 220, 220),
                                           fill='black',
                                           outline='black')
                    display.text_pixels('Stop', clear_screen=False,
                                        x=125, y=185,
                                        text_color='white', font='lutBS18')
                    display.update()
                    start = 'STOP_PROGRAM'
                    valid_input = True
            if valid_input:
                break

    return start


def show_message(msg, sec):
    ''' Display a message on PiStorms screen.'''

    display.text_pixels(msg, clear_screen=True, x=15, y=100,
                        text_color='black', font='lutBS18')
    display.update()
    sleep(sec)

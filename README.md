# Tic Tac Toe game for LEGO Minstorms with PiStorms v2

## Hardware
- Mindsensors.com PiStorms v2
- Raspberry Pi 3B
- Picamera
- LEGO Mindstorms

LEGO Mindstorms:
- LEGO LargeMotor connected to port BAM1
- LEGO LargeMotor connected to port BBM1
- LEGO LargeMotor connected to port BBM2
- LEGO MediumMotor connected to port BAM2
- LEGO TouchSensor connected to port BAS2
- LEGO TouchSensor connected to port BBS2

## Software
- ev3dev operating system
- OpenCV

The program is written in Python on the ev3dev operating system. 
For calculating the computer’s moves I used the Minimax algorithm. 
This way the computer will always win or the game ends in a draw. 
Of course, this way it’s no fun to play with, but if you like 
you can change the algorithm in such way that the computer does 
not always pick the best move out of all possibilities. You’ll 
find many suggestions for this on the internet.

Of course the computer knows where it puts its own moves. To 
determine the moves of the human player I use a picamera. 
This camera takes a picture when the human player presses 
the touchsensor. Then the program uses OpenCV to detect the 
circles the human player drawed. Now it can use the Minimax 
algorithm to calculate the best move.

See my [website](https://kwsmit.github.io) for pictures and video.

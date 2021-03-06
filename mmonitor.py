import subprocess
from enum import Enum
import time
import threading
from MenuDisplay import MenuDisplay

from gpiozero import RGBLED
from gpiozero import Button

class State(Enum):
    NOT_STARTED = 0
    STOPPED = 1
    STARTING = 2
    RUNNING = 3
    STOPPING = 4


SERVER_STATE = State.NOT_STARTED
SERVER_PROCESS = None
LED = None
BUTTON = None
menu = MenuDisplay()


def ledloop():
    global SERVER_STATE
    global State
    global LED
    LED.color = (0, 0, 0)
    while True:
        ## Turn off - Server Stopped
        if SERVER_STATE == State.STOPPED:
            LED.off
            return
        ## Flash Yellow - Server Starting
        elif SERVER_STATE == State.STARTING:
            #LED.blink(on_time=1, off_time=1, on_color=(0,1,1))
            LED.color = (0, 1, 0)
            time.sleep(0.5)
            LED.color = (0, 0, 0)
            time.sleep(0.5)
        ## Green - Server Running
        elif SERVER_STATE == State.RUNNING:
            LED.color = (0, 1, 0)
            time.sleep(0.5)
        ## Red - Server Sopping
        elif SERVER_STATE == State.STOPPING:
            LED.color = (1, 0, 0)
            time.sleep(0.5)
            LED.color = (0, 0, 0)
            time.sleep(0.5)


def interaction():
    global SERVER_STATE
    global SERVER_PROCESS
    global State
    print("__starting interaction thread....")
    while True:
        if SERVER_STATE == State.STOPPED or SERVER_STATE == State.STOPPING:
            print("__stopping")
            return
        elif SERVER_STATE != State.RUNNING:
            print("__nope, sleeping")
            time.sleep(2)
        else:
            print("__yay!")
            #userinput = input("Please enter your server command: ")
            print("__waiting for button...")
            BUTTON.wait_for_press()
            SERVER_PROCESS.stdin.write(bytearray('stop\n', 'utf-8'))
            SERVER_PROCESS.stdin.flush()
            time.sleep(1)  # wait for 1 second for command to be run

LED = RGBLED(red=9, green=10, blue=11)
BUTTON = Button(21)
UP_BUTTON = Button(5)
DOWN_BUTTON = Button(6)

UP_BUTTON.when_pressed = menu.up_action
DOWN_BUTTON.when_pressed = menu.down_action

level_selected = menu.level_name()

while True:
    menu.enable()
    SERVER_STATE = State.NOT_STARTED
    print("Waiting for button...")

    # let menu selection continue until button is pressed
    while (not BUTTON.is_pressed):
        if (menu.y_movement != 0):
            menu.animate()
            level_selected = menu.level_name()
            print("Selected Level: %s %s" % (menu.selected_level, level_selected))


    #BUTTON.wait_for_press()
    print("Starting server with level: %s" % level_selected)

    interactionThread = threading.Thread(target=interaction)
    interactionThread.start()

    ledThread = threading.Thread(target=ledloop)
    ledThread.start()

    
    menu.disable()
    minecraft = subprocess.Popen(["cd /home/pi/spigot; /usr/bin/bash /home/pi/spigot/start.sh %s" % level_selected],
                                shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    #minecraft = subprocess.Popen(["sh sample.sh"], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    SERVER_STATE = State.STARTING
    SERVER_PROCESS = minecraft


    while True:
        output = minecraft.stdout.readline()
        line = output.decode('utf-8').rstrip()

        if line == '' and minecraft.poll() is not None:
            break
        if line:
            print("Read: %s" % line)
            if "Done" in line:
                print("MM: Ready to interact.")
                SERVER_STATE = State.RUNNING
            if "Stopping the server" in line:
                print("MM: Detected stopping.")
                SERVER_STATE = State.STOPPING

        rc = minecraft.poll


    SERVER_STATE = State.STOPPED
    interactionThread.join()
    ledThread.join()

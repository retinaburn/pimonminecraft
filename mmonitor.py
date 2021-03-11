import subprocess
from enum import Enum
import time
import threading

from gpiozero import RGBLED

class State(Enum):
    NOT_STARTED = 0
    STOPPED = 1
    STARTING = 2
    RUNNING = 3
    STOPPING = 4


SERVER_STATE = State.NOT_STARTED
SERVER_PROCESS = None
LED = None

def ledloop():
    global SERVER_STATE
    global State
    global LED
    LED.color = (0, 0, 0)
    while True:
        if SERVER_STATE == State.STOPPED:
            LED.off
            return
        ## Flash Yellow
        elif SERVER_STATE == State.STARTING:
            #LED.blink(on_time=1, off_time=1, on_color=(0,1,1))
            LED.color = (0, 1, 1)
            time.sleep(0.5)
            LED.color = (0, 0, 0)

            time.sleep(0.5)
        elif SERVER_STATE == State.RUNNING:
            LED.color = (0, 1, 0)
            time.sleep(0.5)
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
            userinput = input("Please enter your server command: ")

            SERVER_PROCESS.stdin.write(bytearray(userinput+'\n', 'utf-8'))
            SERVER_PROCESS.stdin.flush()
            time.sleep(1)  # wait for 1 second for command to be run



interactionThread = threading.Thread(target=interaction)
interactionThread.start()
LED = RGBLED(red=9, green=10, blue=11)
ledThread = threading.Thread(target=ledloop)
ledThread.start()

SERVER_STATE = State.NOT_STARTED
#minecraft = subprocess.Popen(["cd /home/cmoynes/Minecraft; /usr/bin/sh /home/cmoynes/Minecraft/start.sh"],
#                                shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
minecraft = subprocess.Popen(["sh sample.sh"], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
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
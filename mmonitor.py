import subprocess
from enum import Enum
import time
import threading

class State(Enum):
    STOPPED = 1
    STARTING = 2
    RUNNING = 3
    STOPPING = 4
  
global SERVER_STATE
global SERVER_PROCESS

def interaction():
    global SERVER_STATE
    global SERVER_PROCESS
    global State
    print("__starting interaction thread....")
    while True:
        if SERVER_STATE != State.RUNNING:
            print("__nope, sleeping")
            time.sleep(2)            
        else:
            print("__yay!")
            userinput = input("Please enter your server command: ")
            SERVER_PROCESS.stdin.write(bytearray(userinput+'\n','utf-8'))
            SERVER_PROCESS.stdin.flush()
            return


interactionThread = threading.Thread(target=interaction)
interactionThread.start()

SERVER_STATE = State.STOPPED
#minecraft = subprocess.Popen(["cd /home/cmoynes/Minecraft; /usr/bin/sh /home/cmoynes/Minecraft/start.sh"], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)

minecraft = subprocess.Popen(["cd /home/cmoynes/pyplay; sh sample.sh"], shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
SERVER_STATE = State.STARTING
SERVER_PROCESS = minecraft


while True:
    output = minecraft.stdout.readline()
    line = output.decode('utf-8')
    if line == '' and minecraft.poll() is not None:
        break
    if line:
        print("Read: %s" % line)
        if "Done" in line:
            print("MM: Ready to interact.")
            SERVER_STATE = State.RUNNING
                    
    rc = minecraft.poll

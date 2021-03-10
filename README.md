# pimonminecraft
Python Monitor for Minecraft to allow start/stop via a button and status via an LED


## Description

mmonitor.py is my feeble attempt to learn Python, and Raspberry Pi to create a simple interface for my kids to start the Minecraft server.

1. An LED will be RED/OFF if the server is not running
2. A button will launch the minecraft server, the LED will flash YELLOW during 'STARTING'
3. Once the server has started (looking for 'Done'), the LED will turn GREEN
4. If the server has started we are in 'Interaction Mode'
5. In Interation Mode
    1. If the button is pressed, the LED will flash RED and `/stop` will be sent to the minecraft server
    2. Once the process has terminated the LED will turn off
    

    
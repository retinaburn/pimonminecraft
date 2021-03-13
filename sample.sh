echo "Starting...sleeping 2 seconds"
sleep 3s
echo "Slept 2 seconds, going back to sleep"
sleep 3s
echo "2 seconds slept"
echo "Done. OK I have started. I am going to prompt"
read -p "PROMPT>" MYINPUT
echo "Sample Script Read: ${MYINPUT}"
echo "Stopping the server..."
sleep 2s
echo "....."
sleep 2s
echo "Stopped"
exit 0
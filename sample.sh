echo "Starting...sleeping 2 seconds"
sleep 2s
echo "Slept 2 seconds, going back to sleep"
sleep 2s
echo "2 seconds slept"
echo "Done. OK I have started. I am going to prompt"
read -p "PROMPT>" MYINPUT
echo "Sample Script Read: ${MYINPUT}"
exit 0
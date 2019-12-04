SERVICE="dumserver.py"
if pgrep -f "$SERVICE" >/dev/null
then
    echo "*** found a running instance of dumserver, killing it... ***"
	sudo kill $(pgrep -f "dumserver.py")
	echo "*** restarting dumserver... ***"
else
    echo "*** dumserver will now boot ***"
fi
python3 -u dumserver.py &
sleep 2
cd webclient
./run.sh
echo "*** startup sequence completed ***"
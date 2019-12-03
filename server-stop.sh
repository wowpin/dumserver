echo "*** stopping dumserver***"
SERVICE="dumserver.py"
if pgrep -f "$SERVICE" >/dev/null
then
    echo "*** found a running instance of dumserver, killing it... ***"
	kill $(pgrep -f "dumserver.py")
else
    echo "*** no running instances of dumserver were found ***"
fi

SERVICE="client-app.js"
if pgrep -f "$SERVICE" >/dev/null
then
    echo "*** found a running instance of dumserver webclient, killing it... ***"
	kill $(ps aux | grep [c]lient-app.js | awk '{print $2}')
else
    echo "*** no running instances of dumserver webclient were found ***"
fi



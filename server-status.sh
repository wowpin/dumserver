if [ ! -e ./setup.completed ] ; then
    echo '[error] dumserver requires configuration before it can be launched'
    echo '[info] please run the setup.py configuration script'
    exit
fi

SERVICE="dumserver.py"
if pgrep -f "$SERVICE" >/dev/null
then
    echo "*** Dumserver: \e[42mRUNNING\e[0m ***"
else
    echo "*** Dumserver: \e[41mNOT RUNNING\e[0m ***"
fi

SERVICE="client-app.js"
if pgrep -f "$SERVICE" >/dev/null
then
    echo "*** Webclient: \e[42mRUNNING\e[0m ***"
else
    echo "*** Webclient: \e[41mNOT RUNNING\e[0m ***"
fi


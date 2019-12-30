
import os
from requests import get

def yes_or_no(question):
    reply = " "
    while reply[0] is not 'y' or reply[0] is not 'n':
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[0] == 'y':
            return True
        if reply[0] == 'n':
            return False
        else:
            return yes_or_no("Uhhhh... please enter ")
        
print('\n\n\n')

ip = get('https://api.ipify.org').text
print('Following Public IP address has been detected:', ip)
if yes_or_no('Would you like to use it for DUM Webclient configuration?'):
    pass
else:
    ip = str(input("Please input Public IP:")).strip()
    
# Read in the webclient config file
with open('webclient/config/default.js', 'r') as file :
  filedata = file.read()

# Update the config file
filedata = filedata.replace('PUBLIC_IP', str(ip))
# Write the file out again

with open('webclient/config/default.js', 'w') as file:
  file.write(filedata)
if not os.path.exists('setup.completed'):
    os.mknod('setup.completed')

print('\ndumserver configuration has been completed. You can start using the sever with the help of following commands:')
print('./server-start.sh    -    Boot up an instance of dumserver. Once up and running, server can be accessed on http://<Your public IP>')
print('./server-status.sh   -    Check the status of dumserver components')
print('./server-stop.sh     -    Stop all dumserver components')
print('\n')
print('Note: if dumserver is listening for clients on port 80 (which it is configured to do by default!), it needs to run as root. As such, above scripts need to be invoked with a "sudo" prefix.')

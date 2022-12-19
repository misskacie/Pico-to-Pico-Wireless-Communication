import network
import socket
import time
from machine import Pin, ADC
from secret import ssid,password

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)
       
# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

buttonPin = 16
button = Pin(buttonPin, Pin.IN, Pin.PULL_UP)

def buttonvalue():
    return button.value()

# Listen for connections
while True:
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)
        val = buttonvalue()
        response = str(val)
        print(response)       
        cl.send(response)
        cl.close()
        time.sleep(0.2)
    except OSError as e:
        cl.close()
        print('connection closed')
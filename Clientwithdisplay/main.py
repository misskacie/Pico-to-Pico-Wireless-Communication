from secret import ssid,password
from drivers import LCD_1inch8
import network
import socket
import time
import machine
from machine import Pin
   
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
 



LCD = LCD_1inch8()
LCD.fill(LCD.BLUE)
LCD.show()
# Listen for connections
while True:
    try:
        ai = socket.getaddrinfo("192.168.1.11", 80) # Address of Web Server
        addr = ai[0][-1]

        # Create a socket and make a HTTP request
        s = socket.socket() # Open socket
        s.connect(addr)
        s.send(b"GET Data") # Send request
        ss=str(s.recv(512)) # Store reply
        # Print what we received
        print(ss)
        
        if ss[2:-1] == '0':
            LCD.fill(LCD.GREEN)
            LCD.write_text('DOOR',x=50,y=40,size=2,color=LCD.BLACK)
            LCD.write_text('CLOSED',x=34,y=70,size=2,color=LCD.BLACK)
            LCD.show()

        if ss[2:-1] == '1' :
            LCD.fill(LCD.RED)
            LCD.write_text('DOOR',x=50,y=40,size=2,color=LCD.BLACK)
            LCD.write_text('OPEN',x=50,y=70,size=2,color=LCD.BLACK)
            LCD.show()
            
        s.close()          # Close socket
        time.sleep(0.2)    # wait
     
 
    except OSError as e:
        cl.close()
        print('connection closed')
    except KeyboardInterrupt:
        cl.close()

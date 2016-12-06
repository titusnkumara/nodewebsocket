import websocket
import RPi.GPIO as IO
import time
import ast

IO.setwarnings(False)
IO.setmode (IO.BCM)

leftForwardPIN = 19
leftBackwordPIN = 26

rightForwardPIN = 20
rightBackwordPIN = 21

IO.setup(leftForwardPIN,IO.OUT)
IO.setup(leftBackwordPIN,IO.OUT)
IO.setup(rightForwardPIN,IO.OUT)
IO.setup(rightBackwordPIN,IO.OUT)

leftForward = IO.PWM(leftForwardPIN,1000)
leftBackword = IO.PWM(leftBackwordPIN,1000)
rightForward = IO.PWM(rightForwardPIN,1000)
rightBackword = IO.PWM(rightBackwordPIN,1000)


leftForward.start(0)
leftBackword.start(0)
rightForward.start(0)
rightBackword.start(0)

def handleData(data):
    #data is a dictionary
    leftSpeed = int(data.get("l"))
    rightSpeed = int(data.get("r"))
    direction = data.get("d")
    if(direction=="f"):
        leftForward.ChangeDutyCycle(leftSpeed)
        leftBackword.ChangeDutyCycle(0)
        rightForward.ChangeDutyCycle(rightSpeed)
        rightBackword.ChangeDutyCycle(0)
    elif(direction=="b"):
        leftForward.ChangeDutyCycle(0)
        leftBackword.ChangeDutyCycle(leftSpeed)
        rightForward.ChangeDutyCycle(0)
        rightBackword.ChangeDutyCycle(rightSpeed)        

def on_message(ws, message):
    print message
    data = ast.literal_eval(message)
    handleData(data)

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    #for i in range(10):
    #    ws.send(str(i))
    #result =  ws.recv()
    #ws.close()
    print 'Connection open'


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8081",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

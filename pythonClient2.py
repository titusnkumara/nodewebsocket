import websocket
import RPi.GPIO as IO
import time
import ast

IO.setwarnings(False)
IO.setmode (IO.BCM)
IO.setup(19,IO.OUT)
p = IO.PWM(19,1000)
p.start(0)


def on_message(ws, message):
    print message
    data = ast.literal_eval(message)
    p.ChangeDutyCycle(int(data.get("l")))

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

import websocket
import RPi.GPIO as IO
import time
import ast
import thread
import sys

ADDRESS = "ws://tesla.ce.pdn.ac.lk:8081"

IO.setwarnings(False)
IO.setmode (IO.BCM)

leftForwardPIN = 19
leftBackwordPIN = 26

rightForwardPIN = 16
rightBackwordPIN = 21

IO.setup(leftForwardPIN,IO.OUT)
IO.setup(leftBackwordPIN,IO.OUT)
IO.setup(rightForwardPIN,IO.OUT)
IO.setup(rightBackwordPIN,IO.OUT)

leftForward = IO.PWM(leftForwardPIN,100)
leftBackword = IO.PWM(leftBackwordPIN,100)
rightForward = IO.PWM(rightForwardPIN,100)
rightBackword = IO.PWM(rightBackwordPIN,100)


leftForward.start(0)
leftBackword.start(0)
rightForward.start(0)
rightBackword.start(0)

dataObj = {"37":0,"38":0,"39":0,"40":0,"65":0,"90":0}
speedObj = {'l':0,'r':0,'d':'f'}
MAXVAL = 100
MINVAL = 0
ACCELERATION = 2.0

def handleSpeed():
    global speedObj
    #38-up,37-left,39-right,40-back
    while 1:
        #when only forward(38) is enabled
        #all I need is to increase the speed in both
        if(dataObj['38'] and (not dataObj['37']) and (not dataObj['39'])and (not dataObj['40']) ):
            speedObj['l'] = speedObj['l']+ACCELERATION
            speedObj['r'] = speedObj['r']+ACCELERATION
            #cap these to MAXVAL
            if(speedObj['l']>MAXVAL):
                speedObj['l'] = MAXVAL
            if(speedObj['r']>MAXVAL):
                speedObj['r'] = MAXVAL

        #when only backword(40) is enabled
        #this should act as a brake
        elif((not dataObj['38']) and (not dataObj['37']) and (not dataObj['39'])and dataObj['40'] ):
            speedObj['l'] = speedObj['l']-(ACCELERATION*2)
            speedObj['r'] = speedObj['r']-(ACCELERATION*2)
            #cap these to MINVAL
            if(speedObj['l']<MINVAL):
                speedObj['l'] = MINVAL
            if(speedObj['r']<MINVAL):
                speedObj['r'] = MINVAL   
        #when only left(37) and forward (38) is pressed
        elif(dataObj['38'] and dataObj['37'] and (not dataObj['39'])and (not dataObj['40']) ):
            #left should not exceed MAXVAL
            if(speedObj['l']>(MAXVAL/2)):
                speedObj['l'] = speedObj['l']-(ACCELERATION/2)
            else:
                speedObj['l'] = speedObj['l']+(ACCELERATION/2)
            speedObj['r'] = speedObj['r']+ACCELERATION
            if(speedObj['r']>MAXVAL):
                speedObj['r']=MAXVAL
        #when only right(39) and forward (38) is pressed
        elif(dataObj['38'] and (not dataObj['37']) and  dataObj['39'] and (not dataObj['40']) ):
            #right should not exceed MAXVAL
            if(speedObj['r']>(MAXVAL/2)):
                speedObj['r'] = speedObj['r']-(ACCELERATION/2)
            else:
                speedObj['r'] = speedObj['r']+(ACCELERATION/2)
            speedObj['l'] = speedObj['l']+ACCELERATION
            if(speedObj['l']>MAXVAL):
                speedObj['l']=MAXVAL

        #if nothing pressed, just reduce the speed until zero
        elif((not dataObj['38']) and (not dataObj['37']) and  (not dataObj['39']) and (not dataObj['40']) ):
            speedObj['r'] = speedObj['r']-(ACCELERATION/2)
            speedObj['l'] = speedObj['l']-(ACCELERATION/2)
            if(speedObj['r']<MINVAL):
                speedObj['r'] = MINVAL
            if(speedObj['l']<MINVAL):
                speedObj['l'] = MINVAL
        else:
            #any other key combination, just reduce the speed
            speedObj['r'] = speedObj['r']-(ACCELERATION/2)
            speedObj['l'] = speedObj['l']-(ACCELERATION/2)
            if(speedObj['r']<MINVAL):
                speedObj['r'] = MINVAL
            if(speedObj['l']<MINVAL):
                speedObj['l'] = MINVAL

        if(dataObj['65']):
            #gear change allow only if in smaller speeds
            if(int(speedObj.get("l")) <10 and int(speedObj.get("r"))<10):
                speedObj['d']='f'
        if(dataObj['90']):
            #gear change allow only if in smaller speeds
            if(int(speedObj.get("l")) <10 and int(speedObj.get("r"))<10):
                speedObj['d']='b'
        #print speedObj

        #now assign speeds
        global leftForward
        global leftBackword
        global rightForward
        global rightBackword
        leftSpeed = int(speedObj.get("l"))
        rightSpeed = int(speedObj.get("r"))
        direction = speedObj.get("d")
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
            
        time.sleep(0.03)
    
def handleData(data):
    #data is a dictionary
    #edit the global data
    global dataObj
    '''
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
    '''
    #print data
    dataObj = data;

def on_message(ws, message):
    print message
    try:
        data = ast.literal_eval(message)
        handleData(data)
    except:
        pass

def on_error(ws, error):
    print error
    sys.exit(0)

def on_close(ws):
    print "### closed ###"
    sys.exit(0)

def on_open(ws):
    #for i in range(10):
    #    ws.send(str(i))
    #result =  ws.recv()
    #ws.close()
    print 'Connection open'


if __name__ == "__main__":
    #create thread to handle speed
    try:
        thread.start_new_thread( handleSpeed, () )
        
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(ADDRESS,
                                  on_message = on_message,
                                  on_error = on_error,
                                  on_close = on_close)
        ws.on_open = on_open
        ws.run_forever()
    except:
        sys.exit(0)

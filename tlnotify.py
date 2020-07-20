#!/home/epics/miniconda3/envs/telegram/bin/python
import telegram
import os
import json
import time
import epics
import queue

## Get credentials
TLpath = os.environ['HOME']+"/.credentials/bot.json"
TL = json.load(open(TLpath, "r"))

## bot setup
bot = telegram.Bot(TL['token'])

## queue
msgqueue = queue.Queue()

## PV callback
def onChange(pvname=None, value=None, char_value=None, **kw):
    global msgqueue
    msg = time.asctime() + ":[" + pvname +"]:"+str(value)
    msgqueue.put(msg)

def onConnectionChange(pvname=None, conn= None, **kws):
    global msgqueue
    msg = time.asctime() + ":[" + pvname +"]:Connection:"+str(conn)
    msgqueue.put(msg)

## EPICS PVs
PVList = [
    "PINK:WLD:state",
    "PINK:WLD:value",
    "PINK:AUX:Valves_RBV",
    "PINK:AUX:Shutters_RBV",
    "PINK:SCNALM:scanDone",
    ]

PVs = []
for pv in PVList:
    PVs.append(epics.PV(pv, auto_monitor=True, callback=onChange, connection_callback=onConnectionChange))

while(1):
    if msgqueue.qsize():
        msg = msgqueue.get()
        print(msg)
        bot.sendMessage(TL['chatid'], msg)
    time.sleep(5)

print("OK")

# Tell the script where to find the Portal to log the data
PORTAL_ADDR = '\x00\x00\x01'

# Pin the switch is connected to
BUTTON_PIN = 9

@setHook(HOOK_STARTUP)
def startupEvent():
    # Set SM200 Pin F1 to be an input pin
    setPinDir(BUTTON_PIN, False)
    #setPinPullup(BUTTON_PIN, False)
    monitorPin(BUTTON_PIN, True)
    rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " has been turned on")
    
@setHook(HOOK_GPIN)
def button_pressed(pinNum, isSet):
   if pinNum == BUTTON_PIN:
        rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " is killing LTAs")
        mcastRpc(0x0002, 3, 'kill_LTA')
        
@setHook(HOOK_1S)
def status_check():
    rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " checking in...")

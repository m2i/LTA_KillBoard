# Tell the script where to find the Portal to log the data
PORTAL_ADDR = '\x00\x00\x01'

# The output pin for the LED on the SM200
LED_PIN = 9

@setHook(HOOK_STARTUP)
def startupEvent():
    # Set SM200 Pin F3 to be an output pin
    setPinDir(LED_PIN, True)
    rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " has been turned on")
    mcastRpc(0x0002, 3, 'kill_LTA')
    writePin(LED_PIN, True)
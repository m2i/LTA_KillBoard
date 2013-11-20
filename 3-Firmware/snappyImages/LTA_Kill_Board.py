# Define the pin which controls the latch
LATCH_CTRL_PIN = 28
BATTERY_PIN = 5

# Tell the script where to find the Portal to log the data
PORTAL_ADDR = '\x00\x00\x01'

# Status Codes
LTA_BOARD_OFF = 0
LTA_BOARD_ON = 1
LTA_BOARD_KILLED = 2
LTA_BOARD_RESURRECTED = 3
LTA_BOARD_LOW_BATT = 4

# Is the LTA Alive?
LTA_Alive = 0

# Have we heard from portal?
Portal_Response = 0

@setHook(HOOK_STARTUP)
def startupEvent():
    global LTA_Alive
    # Set the LTA Board to respond to multicast group 2 and forward it on
    saveNvParam(5, 0x0002)
    saveNvParam(6, 0x0002)
    
    # Set RF266 Pin 20 to be an output pin
    setPinDir(LATCH_CTRL_PIN, True)
    
    # Set the RF266 ADC pin 5 to be an input
    setPinDir(29, False)
    
    # Toggle the pin to 3.3V
    writePin(LATCH_CTRL_PIN, True)

    adc = readAdc(BATTERY_PIN)
    rpc(PORTAL_ADDR, "ping")

    if adc >= 832:
        writePin(LATCH_CTRL_PIN, False)
        rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " has been turned on")
        LTA_Alive = LTA_BOARD_ON
        rpc(PORTAL_ADDR, "LTA_Add_Board", loadNvParam(8), LTA_Alive, adc)
    else:
        rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " Low Battery - Not turning on")
        rpc(PORTAL_ADDR, "LTA_Add_Board", loadNvParam(8), LTA_BOARD_LOW_BATT, adc)
        LTA_Alive = LTA_BOARD_LOW_BATT

def Response():
    global Portal_Response
    Portal_Response = 1

#TODO Update
# Kill the LTA by setting the latch control pin high
def kill_LTA():
    global LTA_Alive
    global Portal_Response
    writePin(LATCH_CTRL_PIN, True)
    LTA_Alive = LTA_BOARD_KILLED
    if Portal_Response == 1:
        rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " has been killed")

#TODO Update
# Enable the motors and received by setting the latch control pin low
def restart_LTA():
    global LTA_Alive
    global Portal_Response
    writePin(LATCH_CTRL_PIN, False)
    LTA_Alive = LTA_BOARD_RESURRECTED
    if Portal_Response == 1:
        rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " has been resurrected")

# Return the current battery voltage as a number between 0-1023 every second
@setHook(HOOK_1S)
def status_check():
    global Portal_Response
    global LTA_Alive
    adc = readAdc(BATTERY_PIN)
    if Portal_Response == 0:
        rpc(PORTAL_ADDR, "ping")
        rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " was already active")
        rpc(PORTAL_ADDR, "LTA_Add_Board", loadNvParam(8), LTA_Alive, adc)

    # Kill the LTA if the battery voltage is below 5.8V
    if (adc <= 742) and (LTA_Alive == 1 or LTA_Alive == 3):
        kill_LTA()

def update_info():
    global LTA_Alive
    adc = readAdc(BATTERY_PIN)
    return str(loadNvParam(8) + "_" + str(adc) + "_" + str(LTA_Alive))

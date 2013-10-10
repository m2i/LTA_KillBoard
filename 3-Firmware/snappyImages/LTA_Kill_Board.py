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
    # Don't turn on the LTAs unless it is above 6.5
    if adc >= 832:
        # Toggle the pin to 0V again
        writePin(LATCH_CTRL_PIN, False)
        rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " has been turned on")
        rpc(PORTAL_ADDR, "LTA_Status", loadNvParam(8), LTA_BOARD_ON)
        LTA_Alive = LTA_BOARD_ON
    else:
        rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " Low Battery - Not turning on")
        rpc(PORTAL_ADDR, "LTA_Status", loadNvParam(8), LTA_BOARD_LOW_BATT)
        LTA_Alive = LTA_BOARD_LOW_BATT


# Kill the LTA by setting the latch control pin high
def kill_LTA():
    global LTA_Alive
    writePin(LATCH_CTRL_PIN, True)
    rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " has been killed")
    rpc(PORTAL_ADDR, "LTA_Status", loadNvParam(8), LTA_BOARD_KILLED)
    LTA_Alive = LTA_BOARD_KILLED

# Enable the motors and received by setting the latch control pin low
def restart_LTA():
    global LTA_Alive
    writePin(LATCH_CTRL_PIN, False)
    rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " has been resurrected")
    rpc(PORTAL_ADDR, "LTA_Status", loadNvParam(8), LTA_BOARD_RESURRECTED)
    LTA_Alive = LTA_BOARD_RESURRECTED

# Return the current battery voltage as a number between 0-1023 every second
@setHook(HOOK_1S)
def status_check():
    adc_value = readAdc(BATTERY_PIN)
    # Kill the LTA if the battery voltage is below 5.8V
    if (adc_value <= 742) & (LTA_Alive == 0):
        kill_LTA()
        rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + " Low Battery")
        rpc(PORTAL_ADDR, "LTA_Status", LTA_BOARD_LOW_BATT)
    else:
        rpc(PORTAL_ADDR, "LTA_Status", LTA_Alive)
        
    rpc(PORTAL_ADDR, "LTA_Battery", adc_value)
    return(adc_value)
    

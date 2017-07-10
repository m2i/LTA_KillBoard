# Define the pin which controls the latch
LATCH_CTRL_PIN = 28
BATTERY_PIN = 5

# Define the battery tolerances
BATTERY_LOW_TURNON = 680		# Corresponds to 6.5V
BATTERY_LOW_FLIGHT = 606		# Corresponds to 5.8V

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
    global BOARD_ADDR
    
    #Configure Serial
    stdinMode(0, 1)
    
    # Set the LTA Board to respond to multicast group 2 and forward it on
    saveNvParam(5, 0x0002)
    saveNvParam(6, 0x0002)
    
    BOARD_ADDR = str(byteToHex(ord(localAddr()[0]))) + ":" + str(byteToHex(ord(localAddr()[1]))) + ":" + str(byteToHex(ord(localAddr()[2])))
    
    # Set RF266 Pin 20 to be an output pin
    setPinDir(LATCH_CTRL_PIN, True)
    
    # Set the RF266 ADC pin 5 to be an input
    setPinDir(29, False)

    rpc(PORTAL_ADDR, "ping")
    rpc(PORTAL_ADDR, "logEvent", loadNvParam(8) + "Gateway Online.")
    print 'Gateway online'
    
def hexNibble(nibble):
    '''Convert a numeric nibble 0x0-0xF to its ASCII string representation "0"-"F"'''
    hexStr = "0123456789ABCDEF"
    return hexStr[nibble & 0xF]

def printHex(byte):
    '''print a byte in hex - input is an integer, not a string'''
    print hexNibble(byte >> 4),
    print hexNibble(byte),         # no trailing CR/LF
    
def byteToHex(byte):
    '''print a byte in hex - input is an integer, not a string'''
    upper = hexNibble(byte >> 4)
    lower = hexNibble(byte)
    return upper + lower


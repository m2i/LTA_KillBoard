import wx
import decimal
import threading

ltas = []

# LTA Status Codes
LTA_BOARD_OFF = 0
LTA_BOARD_ON = 1
LTA_BOARD_KILLED = 2
LTA_BOARD_RESURRECTED = 3
LTA_BOARD_LOW_BATT = 4

# Number of total LTAs
LTA_NUMBER = 6


# Maximum Battery Voltage
max_volt = 8.3

def LTA_Status(status):
    # Determine the node number
	node_number = int(remoteNode.name.split('_')[2])

	# Search for the LTA in the 
	global ltas
	found_lta = 0
	for i in range(0, len(ltas)):
		if ltas[i][1] == node_number:
			ltas[i][0].updateStatus(status)
			ltas[i][2] = 0
			found_lta = 1
	if found_lta == 0:
		ltas.append([MainFrame(root, node_number), node_number, 0])

def LTA_Battery(adc_value):
    # Determine the battery voltage
	batt_voltage = max_volt*adc_value/1024
    
    # Determine the node number
	node_number = int(remoteNode.name.split('_')[2])
	
	global ltas
	found_lta = 0
	for i in range(0, len(ltas)):
		if ltas[i][1] == node_number:
			ltas[i][0].updateBattery(batt_voltage)
			ltas[i][2] = 0
			found_lta = 1
	if found_lta == 0:
		ltas.append([MainFrame(root, node_number), node_number, 0])
		
def LTA_Check():
	global ltas
	for i in range(0, len(ltas)):
		ltas[i][0].checkLTA()

class MainFrame(wx.Frame):
	"""Main window frame"""
	def __init__(self, parent, lta_number):
		wx.Frame.__init__(self, parent, -1, "LTA " + str(lta_number) + " Status", style = wx.DEFAULT_FRAME_STYLE)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.number = lta_number
		self.panel = MainPanel(self, lta_number)
		self.Show(True)

	def onClose(self, event):
		self.Destroy()

	def updateBattery(self, battReading):
        # Display the new battery reading on the gauge and in the textbox
		self.panel.ltaWindow.voltText.SetLabel('%1.2fV' % battReading)
		self.panel.ltaWindow.gauge.SetValue(battReading)
		self.Refresh()
	
	def updateStatus(self, statusCode):
		# Iterate over the status code returned and update the text
		if statusCode == LTA_BOARD_OFF:
			self.panel.ltaWindow.statusText.SetLabel('Off')
		elif statusCode == LTA_BOARD_ON:
			self.panel.ltaWindow.statusText.SetLabel('On')
		elif statusCode == LTA_BOARD_KILLED:
			self.panel.ltaWindow.statusText.SetLabel('Killed')
		elif statusCode == LTA_BOARD_RESURRECTED:
			self.panel.ltaWindow.statusText.SetLabel('Resurrected')
		elif statusCode == LTA_BOARD_LOW_BATT:
			self.panel.ltaWindow.statusText.SetLabel('Low Battery')
		else:
			self.panel.ltaWindow.statusText.SetLabel('Unknown')
		
		self.Refresh()
        
	def checkLTA(self):
		global ltas
		for i in range(0, len(ltas)):
			if ltas[i][1] == self.number:
				ltas[i][2] = ltas[i][2] + 1
				if ltas[i][2] >= 5:
					self.updateStatus(LTA_BOARD_OFF)
        
class MainPanel(wx.Panel):
    """Main Panel"""
    def __init__(self, parent, lta_number):
		wx.Panel.__init__(self, parent, -1)
		self.MainFrame = parent
		mainGrid = wx.BoxSizer(wx.HORIZONTAL)
		column1 = wx.BoxSizer(wx.VERTICAL)
		self.ltaWindow = LTA_Panel(self, lta_number)
		mainGrid.Add(self.ltaWindow, 1 , wx.CENTER)

		self.SetSizerAndFit(mainGrid)

		
class LTA_Panel(wx.Panel):
	def __init__(self, parent, lta_number):
		wx.Panel.__init__(self, parent, -1)
		self.subGrid = wx.BoxSizer(wx.VERTICAL)
		self.voltGrid = wx.BoxSizer(wx.HORIZONTAL)

		self.ltaLabel = wx.StaticText(self, -1, "0", (30, 40))
		font = wx.Font(40, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, "Arial")
		self.ltaLabel.SetFont(font)
		self.ltaLabel.SetLabel('LTA Board ' + str(lta_number) + ':')
		self.subGrid.Add(self.ltaLabel, 0, wx.CENTER)
        
		self.gauge = wx.Gauge(self, 0, 8.5, (10, 75), (300, 25))
		self.gauge.SetValue(0)
		self.voltGrid.Add(self.gauge, 0, wx.EXPAND)

		self.voltText = wx.StaticText(self, -1, "0", (30, 40))
		font1 = wx.Font(24, wx.DEFAULT, wx.NORMAL, wx.BOLD, False, "Arial")
		self.voltText.SetFont(font1)
		self.voltGrid.Add(self.voltText, 1, wx.EXPAND)
		
		self.statusGrid = wx.BoxSizer(wx.HORIZONTAL)
		self.statusLabel = wx.StaticText(self, -1, "Status:", (30,40))
		self.statusLabel.SetFont(font1)
		self.statusGrid.Add(self.statusLabel, 0, wx.LEFT)
		
		self.statusText = wx.StaticText(self, -1, "Off", (30, 40))
		self.statusText.SetFont(font1)
		self.statusGrid.Add(self.statusText, 1, wx.LEFT)
		
		self.subGrid.Add(self.voltGrid, 1, wx.LEFT)
		self.subGrid.Add(self.statusGrid, 2, wx.LEFT)
		self.SetSizerAndFit(self.subGrid)

if __name__ == '__main__':
    """This code is needed to run as a stand alone program""" 
    class MyApp(wx.App):
        def OnInit(self):
            self.frame = MainFrame(None, 1)
            self.SetTopWindow(self.frame)
            return True


    app = MyApp(0)
    app.MainLoop()
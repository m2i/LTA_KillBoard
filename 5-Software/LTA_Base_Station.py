import wx
import threading
import time

#[0] = number, [1] = adc, [2] = status, [3] = timeout, [4] = address
boards = []

# LTA Status Codes
LTA_BOARD_OFF = 0
LTA_BOARD_ON = 1
LTA_BOARD_KILLED = 2
LTA_BOARD_RESURRECTED = 3
LTA_BOARD_LOW_BATT = 4

#Lower limit for colors
GREEN_VOLTAGE = 7.5
YELLOW_VOLTAGE = 6.5

# Maximum Voltage able to be sensed
max_volt = 9.80

def ping():
        rpc(remoteAddr, "Response")

def LTA_Check_In():
        global boards
        #global timer
        #Called every second, updates each board
        #timer.cancel()
        #timer = threading.Timer(1, LTA_Check_In)
        #timer.start()
        if (len(boards) == 0):
                return
        for board in boards:
                if board[3] == 4:
                        board[2] = LTA_BOARD_OFF
                        frame.Update_Board_Info(board)
                else:
                        board[3] = board[3] + 1
                rpc(board[4], "callback", "LTA_Update_Info", "update_info")

def LTA_Update_Info(info):
        global boards
        global frame
        caller = remoteAddr
        splitInfo = info.split('_')
        for board in boards:
                if board[4] == caller:
                        board[3] = 0
                        board[1] = splitInfo[3]
                        board[2] = splitInfo[4]
                        frame.Update_Board_Info(board)
                        return

def LTA_Add_Board(name, status, batt):
        global boards
        global frame
        number = name.split('_')[2]
        caller = remoteAddr
        index = 0
        if (len(boards) == 0) or (boards[len(boards)-1][0] < number):
                boards.append([number, batt, status, 0, caller])
                frame.Update_Board_Info(boards[len(boards)-1])
                return
        for i in range(len(boards)):
                if boards[i][0] == number:
                        return
                if boards[i][0] < number:
                        continue
                index = i
                break
        boards.insert(index, [number, batt, status, 0, caller])
        frame.Update_Board_Info(boards[index])

class MainFrame(wx.Frame):
        """Main window frame"""
        def __init__(self, parent):
                wx.Frame.__init__(self, parent, -1, "LTA Data", style = wx.DEFAULT_FRAME_STYLE, size = (800, 600))
                self.Bind(wx.EVT_CLOSE, self.onClose)
                self.column1 = wx.BoxSizer(wx.VERTICAL)
                self.column2 = wx.BoxSizer(wx.VERTICAL)
                self.MainSizer = wx.BoxSizer(wx.HORIZONTAL)
                self.boardList = []
                self.MainSizer.Add(self.column1)
                self.MainSizer.Add(self.column2)
                self.SetSizer(self.MainSizer)
                self.SetAutoLayout(True)
                self.Layout()
                self.Show(True)

        def onClose(self, event):
                self.Destroy()

        def Update_Board_Info(self, board):
                for i in range(len(self.boardList)):
                        if board[0] == self.boardList[i][0]:
                                if i < 25:
                                        children = self.boardList[i][1].GetChildren()
                                        for child in children:
                                                if child.IsSizer() and (child.GetSizer() !=  None):
                                                        child.GetSizer().Destroy()
                                                elif child.IsWindow and (child.GetWindow() != None):
                                                        child.GetWindow().Destroy()
                                        self.column1.Remove(self.boardList[i][1])
                                        self.boardList[i][1] = self.NewBoxSizer(board)
                                        self.column1.Insert(i, self.boardList[i][1], 1, wx.ALIGN_TOP | wx.EXPAND)
                                        self.boardList[i][1].Layout()
                                        self.column1.Layout()
                                        self.MainSizer.Layout()
                                        self.Layout()
                                        return
                                else:
                                        children = self.boardList[i][1].GetChildren()
                                        for child in children:
                                                if child.IsSizer() and (child.GetSizer() !=  None):
                                                        child.GetSizer().Destroy()
                                                elif child.IsWindow and (child.GetWindow() != None):
                                                        child.GetWindow().Destroy()
                                        self.column2.Remove(self.boardList[i][1])
                                        self.boardList[i][1] = self.NewBoxSizer(board)
                                        self.column2.Insert(i - 25, self.boardList[i][1], 1, wx.ALIGN_TOP | wx.EXPAND)
                                        self.boardList[i][1].Layout()
                                        self.column2.Layout()
                                        self.MainSizer.Layout()
                                        self.Layout()
                                        return
                        if (board[0] > self.boardList[i][0]):
                                continue
                        self.boardList.insert(i, [board[0], self.NewBoxSizer(board)])
                        if i < 25:
                                self.column1.Insert(i, self.boardList[i][1], 1, wx.ALIGN_TOP | wx.EXPAND)
                                if len(self.column1.GetChildren()) > 25:
                                        self.column1.Detach(self.boardList[25][1])
                                        self.column2.Insert(0, self.boardList[25][1], 1, wx.ALIGN_TOP | wx.EXPAND)
                                        self.column2.Layout()
                                self.column1.Layout()
                                self.MainSizer.Layout()
                                self.Layout()
                                return
                        else:
                                self.column2.Insert(i - 25, self.boardList[i][1], 1, wx.ALIGN_TOP | wx.EXPAND)
                                self.column2.Layout()
                                self.MainSizer.Layout()
                                self.Layout()
                                return
                self.boardList.append([board[0], self.NewBoxSizer(board)])
                if len(self.boardList) < 25:
                        self.column1.Add(self.boardList[len(self.boardList)-1][1], 1, wx.ALIGN_TOP | wx.EXPAND)
                        self.column1.Layout()
                else:
                        self.column2.Add(self.boardList[len(self.boardList)-1][1], 1, wx.ALIGN_TOP | wx.EXPAND)
                        self.column2.Layout()
                self.MainSizer.Layout()
                self.Layout()

        def NewBoxSizer(self, board):
                global nextID
                sizer = wx.BoxSizer(wx.HORIZONTAL)
                sizer.Add(wx.StaticText(self, -1, "LTA_Board " + board[0]), 0, wx.ALIGN_LEFT)
                sizer.AddStretchSpacer()
                gauge = wx.Gauge(self, nextID, 1024, size = (100, 15))
                nextID = nextID + 1
                gauge.SetValue(int(board[1]))
                sizer.Add(gauge, 0, wx.ALIGN_RIGHT)
                text = wx.StaticText(self, -1, str("%.2f" % (max_volt * int(board[1]) / 1024)))
                if (int(board[1]) * max_volt / 1024) > GREEN_VOLTAGE:
                        text.SetForegroundColour("Green")
                elif int(board[1]) > YELLOW_VOLTAGE:
                        text.SetForegroundColour("Yellow")
                else:
                        text.SetForegroundColour("Red")
                sizer.Add(text, 0, wx.EXPAND | wx.ALIGN_LEFT)
                #sizer.Add(vSizer, 0, wx.ALIGN_TOP)
                sizer.AddStretchSpacer()
                sizer.Add(wx.StaticText(self, -1, self.statusText(board[2])), 1, wx.ALIGN_LEFT)

                return sizer

        def statusText(self, status):
                if int(status) == LTA_BOARD_OFF:
			return "Status: Off"
		elif int (status) == LTA_BOARD_ON:
			return "Status: On"
		elif int(status) == LTA_BOARD_KILLED:
			return "Status: Killed"
		elif int(status) == LTA_BOARD_RESURRECTED:
			return "Status: Resurrected"
		elif int(status) == LTA_BOARD_LOW_BATT:
			return "Status: Low Battery"
		else:
			return "Status: Unknown"

global frame
global nextID
nextID = 0
#global timer
frame = MainFrame(None)
#timer = threading.Timer(1, LTA_Check_In)
#timer.start()

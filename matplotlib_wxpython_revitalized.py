
"""
M Goldberg at EnerSys
Help from Mr. Venus 
"""
 
#this imports wx python 
import wx

#import matplotlib stuff 
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt    

#to get/ send data through command line
import subprocess

from collections import deque

global isPaused
isPaused = True

#interval between adding points
global timerInterval
timerInterval = 2500

#a deque of the x coordinates for the data
global xLocations
xLocations = deque([])

#a deque of the daq data
global data
data = deque([])

#number of points per line before start removing oldest ones
global maxPoints
maxPoints = 100

#the number of points per line currently
global numPoints
numPoints=0

#number of DAQ
global numDaq
numDaq = 0

#number of channels per DAQ
global numChannel
numChannel = 8

#number of tabs on the window
global numTab
numTab = 1


#main frame of program (whole interface including graph) 
class frame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(650,600), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

	#makes two panels, one for interface and one for graph
        self.sp = wx.SplitterWindow(self)
        self.graph = graph(self.sp)
        self.gui = wx.Panel(self.sp)
         
        self.sp.SplitHorizontally(self.graph,self.gui,470)


        #when timer goes off add points
        self.timer=wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.addPoint)

        #notebook holds the tabs
        self.notebook=myNotebook(self.gui)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        self.gui.SetSizer(sizer)

         
    #when timer goes off
    def addPoint(self, event):
	#print "timer off"
        global xLocations
        global data
        global numPoints
        global maxPoints
        global numDaq

        #put the x coordinate of the next point on the deque.
        xLocations.append(numPoints)

        commandString = 'cd ~/Linux_Drivers-master/USB/mcc-libusb ; ./test-usb1608FS ' + str(int(numDaq)-1)
        #print commandString

        #call for daq data
        proc = subprocess.Popen(commandString, shell = True, stdout=subprocess.PIPE)

        #puts data in data deque (also removes if too many)
        try:
            currentChannel = 0

            if(numPoints > maxPoints):
                xLocations.popleft() 
                for line in proc.stdout:
                    data[currentChannel].append(line)
                    data[currentChannel].popleft()
                    currentChannel +=1

            else:
                for line in proc.stdout:
                    data[currentChannel].append(line)
                    currentChannel +=1

        except:
            print "Error getting data"
	       

        numPoints += 1

        frame.graph.plot()

        #update tab images
        self.notebook.OnTimerImg()


#collection of tabs
class myNotebook(wx.Notebook):
    def __init__(self,parent):
        wx.Notebook.__init__(self,parent)

        #adds initial tab
        tab1 = myTab(self)
        self.AddPage(tab1, "Tab 1")

        #makes list of images
        imgList = wx.ImageList(16,16)
        #adds a random picture of a red square from the internet (change to better pic once have one)
        self.img0 = imgList.Add(wx.Bitmap('/home/pi/Desktop/FF0000.png', wx.BITMAP_TYPE_PNG))
        self.AssignImageList(imgList)

        #if the user switches the tab, OnPageChanging() will run
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

    #saves current data and sets graph to data on new tab
    def OnPageChanging(self, event):

        try:
            #the tab being changed to
            newTab = event.EventObject.GetChildren()[event.Selection]
            #the tab comming from
            oldTab = event.EventObject.GetChildren()[event.OldSelection]
            
            global data
            global xLocations
            global numPoints
            global numDaq
            global isPaused

            #saves current graph in the old tab's data
            oldTab.tabData = data
            oldTab.tabXLocations = xLocations
            oldTab.tabNumPoints = numPoints
            oldTab.tabNumDaq = numDaq

            #tells graph what data it should currently have
            data = newTab.tabData
            xLocations = newTab.tabXLocations
            numPoints = newTab.tabNumPoints
            numDaq = newTab.tabNumDaq

            #stops timer
            frame.timer.Stop()
            isPaused = True
            print "stop"

            #updates graph
            frame.graph.plot()

            #updates gui
            event.Skip()

        except:
            print "Error or the prgram quit"
            #when the user closes out of the program an error occurs becuase it think tab is changing to -1 (I think)

    #checks to see if tab images need to be updated
    def OnTimerImg(self):
        self.SetPageImage(0, self.img0)
        


#each tab panel
class myTab(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent=parent, id=wx.ID_ANY)

        #a deque of the x coordinates for the data collected for the tab
        self.tabXLocations = deque([])

        #a deque of the daq data collected for the tab
        self.tabData = deque([])

        #the number of points per line currently on that tab
        self.tabNumPoints=0

        #number of DAQ desired for the tab
        self.tabNumDaq = 0

        #text box to enter the number of DAQ attached
        self.txtDaqNum = wx.TextCtrl(self, -1, pos=(265,10), size=(70,40))
	
	#submits number of daq's in the txtDaqNum
        self.btnSubmit = wx.Button(self,-1,"Submit Nuber of DAQ", size=(160,40),pos=(100,10))
        self.btnSubmit.Bind(wx.EVT_BUTTON,self.submit)

	#random button for testing
        #self.btnHi = wx.Button(self,-1,"Hi", size=(40,40),pos=(300,10))
        #self.btnHi.Bind(wx.EVT_BUTTON,self.hi)

	#text box for user to insert what to set digipot to
        self.txtDigipot = wx.TextCtrl(self, size =(100,40), pos = (515,10))

        #button to submit data in txtDigipot to digipot
        self.btnDigipot = wx.Button(self, label = "Send to Digipot", size = (110,40), pos = (400, 10))
        self.btnDigipot.Bind(wx.EVT_BUTTON, lambda event: self.toDigipot(wx.EVT_BUTTON, self.txtDigipot.GetValue()), self.btnDigipot)

	#a button to tell the notebook to add a new tab
        self.btnNewTab = wx.Button(self,-1,"New Tab", size=(80,40),pos=(10,10))
        self.btnNewTab.Bind(wx.EVT_BUTTON,self.newTab)
         
    #random test method
    def hi(self,event):
        print "Hi"

    #adds new tab
    def newTab(self, event):
        global numTab
        
        numTab += 1
        frame.notebook.AddPage(myTab(frame.notebook), "Tab " + str(numTab))
        
    
    #submits number of DAQ
    def submit(self,event):
        global numDaq
        global numChannel
        
        numDaq = self.txtDaqNum.GetValue()
        
        #makes a deque for each of the channels (each daq I'm using has 8)
        try:
            
            for i in range(0, (int(numDaq))*numChannel):
                data.append(deque([]))

            #removes button and disable changing the txtbox to keep the user from trying to re-submit
            self.btnSubmit.Destroy()
            self.txtDaqNum.SetEditable(False)

            #starts or stops timer (timer goes off when add point)
            self.btnStart = wx.Button(self,-1,"Start/Stop", size=(80,40),pos=(160,10))
            self.btnStart.Bind(wx.EVT_BUTTON,self.startStop)

        except ValueError:
            print "Plese only input numbers" 
        
       

    #writes to digipot and then reads to make sure changed.  result printed
    def toDigipot(self, event, valToWrite):

        #writes to digipot and prints out what it was set to
        try:
            int(valToWrite)
            proc = subprocess.Popen("./i2cDigipot2 %s"%valToWrite, shell = True, stdout=subprocess.PIPE)

            for line in proc.stdout:
               print line

        except ValueError:
            print "Plese only input numbers"          

    #starts or stops the timer
    def startStop(self,event):
        global isPaused
        global timerInterval

        if(isPaused):
        	frame.timer.Start(timerInterval)
        	isPaused = False
        	print "start"
        else:
                frame.timer.Stop()
                isPaused = True
                print "stop"


#the graph for DAQ data 
class graph(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.figure = plt.figure()
         
        self.canvas = FigureCanvas(self,-1, self.figure)

    #makes subplot and grpahs data 
    def plot(self):

        global xLocations

        #make ax global and move into _init_?
        ax = self.figure.add_subplot(111)

        ax.set_xlabel('Time')
        ax.set_ylabel('Volts')

        ax.set_title('USB-1608FS DAQ Data')

	#removes whitespace along x axis
        plt.autoscale(enable=True, axis='x', tight=True)

	#print xLocations

        #makes lines based on the deques
        try:
            for i in range(0, (int(numDaq))*8):
                lines = ax.plot(xLocations, data[i], '*-', label=str(i+1))
            
        except:
            print "error graphing data"

        try:
            #makes key for graph
            plt.legend(bbox_to_anchor=(1,1), loc=2, borderaxespad=0., fontsize = 10, title="Data")
        except:
            print "Can't make key right now"
        
            
        self.canvas.draw()

        #clears lines in axis so still see old lines below new ones
        ax.cla()

        '''myLines=lines.pop(0)
	#myLines.remove()
	#del myLines'''    
   

#controlling code
app = wx.App(redirect=False)
frame = frame(None,"USB-1608FS DAQ Data Chart")
frame.Show()
app.MainLoop()

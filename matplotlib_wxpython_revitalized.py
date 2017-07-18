
"""
M Goldberg at EnerSys
Help from Mr. Venus
 
"""
 
 
#import wx python 
import wx
import random

#import matplotlib stuff 
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as NavigationToolbar
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

#the number of points per line currently
global numPoints
numPoints=0

#a deque of the daq data
global data
data = deque([])

#number of DAQ
global numDaq
numDaq = 0

#number of points per line before start removing oldest ones
global maxPoints
maxPoints = 10

#main frame of program (whole interface including graph) 
class frame(wx.Frame):
    def __init__(self,parent,title):
        wx.Frame.__init__(self,parent,title=title,size=(650,600), style=wx.MINIMIZE_BOX|wx.SYSTEM_MENU|
                  wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)

	#makes two panels, one for interface and one for graph
        self.sp = wx.SplitterWindow(self)
        self.graph = graph(self.sp)
        self.gui = wx.Panel(self.sp,style=wx.SUNKEN_BORDER)
         
        self.sp.SplitHorizontally(self.graph,self.gui,470)
         
	#starts or stops timer (timer goes off when add point)
        self.btnStart = wx.Button(self.gui,-1,"Start/Stop", size=(80,40),pos=(50,10))
        self.btnStart.Bind(wx.EVT_BUTTON,self.startStop)
         
	#text box to enter the number of DAQ attached
	self.txtDaqNum = wx.TextCtrl(self.gui, -1, pos=(160,10), size=(70,40))
	
	#submits number of daq's in the txtDaqNum
        self.btnSubmit = wx.Button(self.gui,-1,"Submit", size=(80,40),pos=(240,10))
        self.btnSubmit.Bind(wx.EVT_BUTTON,self.submit)
        
	#random button for testing
        self.btnHi = wx.Button(self.gui,-1,"Hi", size=(40,40),pos=(500,10))
        self.btnHi.Bind(wx.EVT_BUTTON,self.hi)

	#when timer goes off add points
	self.timer=wx.Timer(self)
	self.Bind(wx.EVT_TIMER, self.addPoint)
         
    #random test method
    def hi(self,event):
        print "Hi"
    
    #submits number of DAQ (or will when I add that)
    def submit(self,event):
        global numDaq
        numDaq = self.txtDaqNum.GetValue()
        for i in range(0, (int(numDaq))*8):
            data.append(deque([]))
            #print "deque added"
 
    #plots graph
    def plot(self,event):
        self.graph.plot()  

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
        #try:
	if True:
            currentChannel = 0
        
            for line in proc.stdout:
                #print line
                #print xLocations[0]+currentChannel
                data[currentChannel].append(line)

                if(numPoints > maxPoints):
            	    data[currentChannel].popleft()
                #print line
                #print data[currentChannel]
                #print "boing"
                currentChannel +=1

        #except:
            #print "error: somethihng or other"

        #print data[0]

        #removes x coordinate if too many
        if(numPoints > maxPoints):
	    xLocations.popleft()    


	numPoints += 1

	

	self.graph.plot()


    #starts or stops the timer
    def startStop(self,event):
	global isPaused
	global timerInterval

	if(isPaused):
        	self.timer.Start(timerInterval)
		isPaused = False
		print "start"   
	else:
		self.timer.Stop() 
		isPaused = True
		print "stop"



#the graph for DAQ data 
class graph(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.figure = plt.figure()
         
        self.canvas = FigureCanvas(self,-1, self.figure)
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Hide()
     
    def plot(self):

        global xLocations
        
        ax = self.figure.add_subplot(111)

	ax.set_xlabel('Time')
	ax.set_ylabel('Volts')

	ax.set_title('DAQ Data')
	plt.autoscale(enable=True, axis='x', tight=True)

	#print xLocations

        #print xLocations

        #makes lines based on the deques
        for i in range(0, (int(numDaq))*8):
            lines = ax.plot(xLocations, data[i], '*-', label='line')

        plt.legend()
            
        self.canvas.draw()

        #clears lines in axis so still see old lines below new ones
        ax.cla()

        #lines.pop(0).remove()
        #del lines

	#myLines=lines.pop(0)
	#myLines.remove()
	#del myLines    
   

#controlling code
app = wx.App(redirect=False)
frame = frame(None,"DAQ Data Chart")
frame.Show()
app.MainLoop()

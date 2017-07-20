
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

#number of points per line before start removing oldest ones
global maxPoints
maxPoints = 100

#number of channels per DAQ
global numChannel
numChannel = 8

#number of tabs on the window
global numTab
numTab = 1

#what tab the user is currently looking at
global activeTab


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
        global maxPoints
        global numTab

        #loop through tabs
        for loopTab in range(0,numTab):
            #print "timering"
            currentTab = self.notebook.GetPage(loopTab)

            try:
                #get data from DAQ
                commandString = 'cd ~/Linux_Drivers-master/USB/mcc-libusb ; ./test-usb1608FS ' + str(int(currentTab.tabNumDaq)-1)

                #call for daq data
                proc = subprocess.Popen(commandString, shell = True, stdout=subprocess.PIPE)

                #if tab is ready to recive data (it's not when brand new)
                if currentTab.isCollectingData:

                    #adds point to list of x values
                    currentTab.tabXLocations.append(currentTab.tabNumPoints)

                    currentChannel = 0

                    #if more points than want to handle
                    if(currentTab.tabNumPoints > maxPoints):

                        #drop oldest x value
                        currentTab.tabXLocations.popleft()

                        #loop though output (each output is the output of one channel)
                        for line in proc.stdout:
                            currentTab.tabData[currentChannel].append(line)
                            currentTab.tabData[currentChannel].popleft()
                            currentChannel +=1

                    #if have aceptable amount of points
                    else:
                        for line in proc.stdout:
                            currentTab.tabData[currentChannel].append(line)
                            currentChannel +=1

                    #print str(loopTab) + str(currentTab.tabXLocations)

            except:
                print "Error getting data"
	       
            #number of points on that tab increased, keep track
            currentTab.tabNumPoints += 1

        #tells grpah to plot data of active tab
        frame.graph.plot(activeTab.tabXLocations, activeTab.tabData, activeTab.tabNumDaq)

        #update tab images
        self.notebook.OnTimerImg()


#collection of tabs
class myNotebook(wx.Notebook):
    def __init__(self,parent):
        wx.Notebook.__init__(self,parent)

        global activeTab

        #adds initial tab
        tab1 = myTab(self)
        self.AddPage(tab1, "Tab 1")

        #sets inital value of activeTab
        activeTab = tab1

        #makes list of images
        imgList = wx.ImageList(16,16)
        #adds a random picture of a red square from the internet (change to better pic once have one)
        self.img0 = imgList.Add(wx.Bitmap('/home/pi/Desktop/FF0000.png', wx.BITMAP_TYPE_PNG))
        self.AssignImageList(imgList)

        #if the user switches the tab, OnPageChanging() will run
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)

    #saves current data and sets graph to data on new tab
    def OnPageChanging(self, event):

        global isPaused
        global activeTab

        try:
            #the tab being changed to
            newTab = event.EventObject.GetChildren()[event.Selection]

            #bookkeeping to know what tab the user is on
            activeTab = newTab

            #updates graph
            frame.graph.plot(newTab.tabXLocations, newTab.tabData, newTab.tabNumDaq)

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

        #list of DAQ tab is keeping track of
        self.daqList = deque([])

        #whether the tab is ready to collect data
        self.isCollectingData = False
                

        #text box to enter the number of DAQ attached
        self.txtDaqNum = wx.TextCtrl(self, -1, pos=(290,10), size=(70,40))
	
	#submits number of daq's in the txtDaqNum
        self.btnSubmit = wx.Button(self,-1,"Submit the number of DAQ", size=(190,40),pos=(95,10))
        self.btnSubmit.Bind(wx.EVT_BUTTON,self.submit)

	#text box for user to insert what to set digipot to
        self.txtDigipot = wx.TextCtrl(self, size =(100,40), pos = (515,10))

        #button to submit data in txtDigipot to digipot
        self.btnDigipot = wx.Button(self, label = "Send to Digipot", size = (110,40), pos = (400, 10))
        self.btnDigipot.Bind(wx.EVT_BUTTON, lambda event: self.toDigipot(wx.EVT_BUTTON, self.txtDigipot.GetValue()), self.btnDigipot)

	#a button to tell the notebook to add a new tab
        self.btnNewTab = wx.Button(self,-1,"New Tab", size=(80,40),pos=(5,10))
        self.btnNewTab.Bind(wx.EVT_BUTTON,self.newTab)
        

    #adds new tab
    def newTab(self, event):
        global numTab
        
        numTab += 1
        frame.notebook.AddPage(myTab(frame.notebook), "Tab " + str(numTab))
        
    #submits number of DAQ
    def submit(self,event):
        global numChannel

        #puts user input from text box into var
        self.tabNumDaq = self.txtDaqNum.GetValue()
        
        try:

            #makes a deque for each of the channels
            for i in range(0, (int(self.tabNumDaq))*numChannel):
                self.tabData.append(deque([]))

            #removes button and disable changing the txtbox to keep the user from trying to re-submit
            self.btnSubmit.Destroy()
            self.txtDaqNum.SetEditable(False)

            #starts or stops timer (timer goes off when add point)
            self.btnStart = wx.Button(self,-1,"Start/Stop Timer", size=(120,40),pos=(165,10))
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

        #if tab is ready to recieve data (it's not if brand new)

        if(isPaused):
            #re-starts timer
            frame.timer.Start(timerInterval)
            isPaused = False
            print "start"
        elif(self.isCollectingData):
            #stops timer and pauses program
            frame.timer.Stop()
            isPaused = True
            print "stop"

        #is corolating button is visable and clicked tab should be collecting data
        self.isCollectingData = True


#the graph for DAQ data 
class graph(wx.Panel):

    def __init__(self,parent):
        wx.Panel.__init__(self, parent)
        self.figure = plt.figure()
         
        self.canvas = FigureCanvas(self,-1, self.figure)

    #makes subplot and grpahs data 
    def plot(self, xLocations, data,numDaq):

        #make ax global and move into _init_?
        ax = self.figure.add_subplot(111)

        ax.set_xlabel('Time')
        ax.set_ylabel('Volts')

        ax.set_title('USB-1608FS DAQ Data')

	#removes whitespace along x axis
        plt.autoscale(enable=True, axis='x', tight=True)
	

        #makes lines based on the deques
        try:
            for i in range(0, (int(numDaq))*8):
                lines = ax.plot(xLocations, data[i], '*-', label=str(i+1))
            
        except:
            print "error graphing data"

        try:
            #makes key for graph
            plt.legend(bbox_to_anchor=(1,1), loc=2, borderaxespad=0., fontsize = 10, title="Channels")
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




'''Old and unused code

#a deque of the x coordinates for the data
#global xLocations
#xLocations = deque([])

#a deque of the daq data
#global data
#data = deque([])
#the number of points per line currently
#global numPoints
#numPoints=0

#number of DAQ
#global numDaq
#numDaq = 0


#says if should be graphing at the moment
#global isGraphing
#isGraphing = False


        ''commandString = 'cd ~/Linux_Drivers-master/USB/mcc-libusb ; ./test-usb1608FS ' + str(int(numDaq)-1)
        #print commandString

        #call for daq data
        proc = subprocess.Popen(commandString, shell = True, stdout=subprocess.PIPE)

        if isGraphing:

            #put the x coordinate of the next point on the deque.
            xLocations.append(numPoints)
            
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

    
            frame.graph.plot()''


            #saves current graph in the old tab's data
            ''oldTab.tabData = data
            oldTab.tabXLocations = xLocations
            oldTab.tabNumPoints = numPoints
            oldTab.tabNumDaq = numDaq

            #tells graph what data it should currently have
            data = newTab.tabData
            xLocations = newTab.tabXLocations
            numPoints = newTab.tabNumPoints
            numDaq = newTab.tabNumDaq''

                            #stops timer
                #frame.timer.Stop()
                #isPaused = True
                #print "stop"

    #random test method
    def hi(self,event):
        print "Hi"


if newTab.tabXLocations:
                print newTab.tabXLocations
                print "data there"
                if isPaused == False:
                    print "dsfa"
                    #isGraphing = True
            else:
                print "grr"
                #isGraphing = False
                
	#random button for testing
        #self.btnHi = wx.Button(self,-1,"Hi", size=(40,40),pos=(300,10))
        #self.btnHi.Bind(wx.EVT_BUTTON,self.hi)

                    #print "adding 0's"
            #xLocations.append(0)
            #for channel in data:
                #channel.append(0)


                        if True: #if(self.isCollectingData):

                        #if the corrolating button is hit on new tab, tab is ready to collect data
        ''else:

            if(isPaused):
                frame.timer.Start(timerInterval)
                isPaused = False
                print "start"''

'''                

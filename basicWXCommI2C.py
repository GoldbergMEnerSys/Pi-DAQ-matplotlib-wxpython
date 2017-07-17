import wx
import sys
import subprocess

app = wx.App()
window = wx.Frame(None, title = "Frame", size = (500,500))
panel = wx.Panel(window)
label = wx.StaticText(panel, label = "Hello World", pos = (100,50))


proc = subprocess.Popen("./i2cDigipot2 0x4", shell = True, stdout=subprocess.PIPE)

print "hi"


for line in proc.stdout:
    print line
    print "Check"


print "done"


window.Show(True)
app.MainLoop()

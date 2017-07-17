import wx
import sys
import subprocess

app = wx.App()
window = wx.Frame(None, title = "Frame", size = (500,500))
panel = wx.Panel(window)
label = wx.StaticText(panel, label = "Hello World", pos = (100,50))

var = 66

proc = subprocess.Popen("./i2cDigipot2 %i"%var, shell = True, stdout=subprocess.PIPE)


for line in proc.stdout:
    print line


print "done"


window.Show(True)
app.MainLoop()

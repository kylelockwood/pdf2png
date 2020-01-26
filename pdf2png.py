#! python3

import os
import subprocess
import sys
from glob import glob
import wx

# Poppler is required for this type of file conversion
POPPATH = r'C:\Program Files (x86)\Poppler\poppler-0.68.0\bin\pdftoppm.exe'
DESKTOPPATH = 'C:' + os.environ["HOMEPATH"] + '\\Desktop\\'


# Define File Drop Target class
class FileDropTarget(wx.FileDropTarget):

    def __init__(self, obj):
        # Initialize the wxFileDropTarget Object
        wx.FileDropTarget.__init__(self)
        self.obj = obj

    def on_drop_files(self, x, y, filenames):
        for file in filenames:
            # Create outFile name
            outFile = os.path.basename(file)
            outFile = outFile.split('.pdf')[0]

            # Check if valid file type
            if not file.endswith('.pdf'):
                wx.MessageBox(f'\'{outFile}\' is not a PDF', 'Invalid FIle Type', wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP)
                continue            
            # Check if outFile already exists
            if glob(DESKTOPPATH + outFile + '*'):
                choice = wx.MessageBox(f'\'{outFile}\' already exists.  Would you like to overwrite?', 'Info', wx.YES|wx.NO | wx.ICON_QUESTION | wx.STAY_ON_TOP)
                if choice == wx.NO:
                    continue
            # Write file name in box
            self.obj.WriteText(file + '\n')

            # Create image file
            print(f'Converting \'{outFile}\' to png... ', end='', flush=True)
            # TODO Dynamic output path, default=DESKTOPPATH
            subprocess.Popen(f'\"{POPPATH}\" -png \"{file}\" \"{DESKTOPPATH}{outFile}\"')
            print('Done')
        return True

class MainWindow(wx.Frame):
    
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(287,280), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.SetBackgroundColour(wx.Colour(240,255,255))
        
        # Text box to receive Dropped Files
        wx.StaticText(self, -1, 'Drag and drop PDF(s) here', (10, 10))
        self.textBox = wx.TextCtrl(self, -1, "", pos=(10,30), size=(250,150), style=wx.TE_MULTILINE) #, |wx.HSCROLL|wx.TE_READONLY
        dt = FileDropTarget(self.textBox)
        # Link the Drop Target Object to the Text Control
        self.textBox.SetDropTarget(dt)

        # Text box for output file path
        wx.StaticText(self, -1, 'Output file path:', (10, 188))
        self.textBox2 = wx.TextCtrl(self, -1, "", pos=(10,208), size=(250,22)) #, |wx.HSCROLL|wx.TE_READONLY
        self.textBox2.WriteText(DESKTOPPATH)

        # TODO Store user default path, preferences file

        # Display the Window
        self.Show(True)
 
    def close_window(self):
        self.Close()
 
class MyApp(wx.App):
    def OnInit(self):
        # Declare the Main Application Window
        frame = MainWindow(None, -1, "PDF to PNG")
        self.SetTopWindow(frame)
        return True
 

 
# Declare the Application and start the Main Loop
app = MyApp(0)
app.MainLoop()

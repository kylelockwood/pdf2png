#!python3

import os
import subprocess
#import sys
from glob import glob
import wx

# Poppler is required for this type of file conversion
POPPATH =       r'C:\Program Files (x86)\Poppler\poppler-0.68.0\bin\pdftoppm.exe'
HOMEPATH =      'C:' + os.environ["HOMEPATH"]
DESKTOPPATH =   HOMEPATH + '\\Desktop\\'
SCRIPTPATH =    HOMEPATH + '\\Documents\\pdf2png\\'

# Define File Drop Target class
class FileDropTarget(wx.FileDropTarget):
""" Handles the dropped file"""
    def __init__(self, obj):
        # Initialize the wxFileDropTarget Object
        wx.FileDropTarget.__init__(self)
        self.obj = obj

    def OnDropFiles(self, x, y, filenames):
        # Get path from text box
        OUTPATH = get_path(app)

        # Check if file output path exists
        if not os.path.exists(OUTPATH):
            wx.MessageBox(f'\'{OUTPATH}\' does not exist.  Please specify a valid file destination.', 'Unknown path', wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP)
            destBox = app.frame.destinationBox
            destBox.Clear()
            destBox.WriteText(read_saved_path())
            return False
        
        # Iterate over all dropped files
        for file in filenames:
            # Create outFile name
            outFile = os.path.basename(file)
            outFile = outFile.split('.pdf')[0]

            # Check if valid file type
            if not file.endswith('.pdf'):
                wx.MessageBox(f'\'{outFile}\' is not a PDF', 'Invalid FIle Type', wx.OK | wx.ICON_ERROR | wx.STAY_ON_TOP)
                continue

            # Check if outFile already exists
            if glob(OUTPATH + outFile + '*'):
                choice = wx.MessageBox(f'\'{outFile}\' already exists.  Would you like to overwrite?', 'Info', wx.YES|wx.NO | wx.ICON_QUESTION | wx.STAY_ON_TOP)
                if choice == wx.NO:
                    continue

            # Write file name in main box
            self.obj.WriteText(file + '\n')

            # Create image file
            print(f'Converting \'{outFile}\' to png... ', end='', flush=True)
            subprocess.Popen(f'\"{POPPATH}\" -r 300 -png \"{file}\" \"{OUTPATH}{outFile}\"')
            print('Done')
        return True


class MainWindow(wx.Frame):
    """ Create main app window """
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, size=(287,280), style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        self.SetBackgroundColour(wx.Colour(240,255,255))
        wx.EVT_CLOSE(self, self.OnClose)

        # Create Text box to receive Dropped Files
        wx.StaticText(self, -1, 'Drag and drop PDF(s) here', (10, 10))
        self.textBox = wx.TextCtrl(self, -1, "", pos=(10,30), size=(250,150), style=wx.TE_MULTILINE) #, |wx.HSCROLL|wx.TE_READONLY
        dt = FileDropTarget(self.textBox)

        # Link the Drop Target Object to the Text Control
        self.textBox.SetDropTarget(dt)

        # CreateText box for output file path
        wx.StaticText(self, -1, 'File destination:', (10, 188))
        self.destinationBox = wx.TextCtrl(self, -1, "", pos=(10,208), size=(250,22), style=wx.TE_PROCESS_ENTER) #, |wx.HSCROLL|wx.TE_READONLY
        self.destinationBox.WriteText(OUTPATH)

        # Display the Window
        self.Show(True)

    def OnClose(self, event):
        # When the app is closed
        save_file(get_path(app))
        self.Destroy()
 

class MyApp(wx.App):
""" Creates the app instance"""
    def OnInit(self):
        # Declare the Main Application Window
        self.frame = MainWindow(None, -1, "PDF to PNG")
        self.SetTopWindow(self.frame)
        return True


def get_path(app):
    # Return the current value in destinationBox
    return app.frame.destinationBox.GetValue()


def save_file(content):
    # Save the output destination
    if not os.path.exists(content):
        content = DESKTOPPATH
    print(f'Saving {content} to outpath.txt')
    with open(SCRIPTPATH + 'outpath.txt', 'w') as f:
        f.write(content)
        f.close()
    return


def read_saved_path():
    # Get the stored output path from file
    if not os.path.exists(SCRIPTPATH + 'outpath.txt'):
        print('file does not exist')
        with open(SCRIPTPATH + 'outpath.txt', 'w') as f:
            f.write(DESKTOPPATH)
    with open(SCRIPTPATH + 'outpath.txt', 'r') as f:
        outpath = f.read()
        print(f'outpath : {outpath}')
        f.close()
        return outpath

 
# Declare the Application and start the Main Loop
OUTPATH = read_saved_path()
app = MyApp(0)
app.MainLoop()

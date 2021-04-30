"""
MIT License

Copyright (c) 2021 INeedADollar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from flask import Flask, send_file
from flask_sockets import Sockets
from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler

import threading
import os, os.path
import subprocess
import atexit
import sys
import ctypes

#******************************************************************************************************************************************************#
class _CursorInfo(ctypes.Structure):                                                                                                                   #
                                                                                                                                                       #
    """Represents a WinApi CursorInfo structure"""                                                                                                     #
                                                                                                                                                       #
    _fields_ = [("size", ctypes.c_int),                                                                                                                #
                ("visible", ctypes.c_byte)]                                                                                                            #
                                                                                                                                                       #
def hide_cursor():                                                                                                                                     #
                                                                                                                                                       #
    """Hides console cursor"""                                                                                                                         #
                                                                                                                                                       #
    ci = _CursorInfo()                                                                                                                                 #
    handle = ctypes.windll.kernel32.GetStdHandle(-11)                                                                                                  #
    ctypes.windll.kernel32.GetConsoleCursorInfo(handle, ctypes.byref(ci))                                                                              #
    ci.visible = False                                                                                                                                 #
    ctypes.windll.kernel32.SetConsoleCursorInfo(handle, ctypes.byref(ci))                                                                              #
#******************************************************************************************************************************************************#


#******************************************************************************************************************************************************#
class colors:                                                                                                                                          #
                                                                                                                                                       #
    """Enum like class that keeps colors for console text"""                                                                                           #
                                                                                                                                                       #
    GREEN = '\033[92m'                                                                                                                                 #
    RED   = '\033[91m'                                                                                                                                 #
    WHITE = '\033[0m'                                                                                                                                  #
#******************************************************************************************************************************************************#


#******************************************************************************************************************************************************#
globalWS = None #current Web Socket                                                                                                                    #
class Server:                                                                                                                                          #
                                                                                                                                                       #
    """Represents a WSGI Server"""                                                                                                                     #
                                                                                                                                                       #
    def __init__(self):                                                                                                                                #
        self.proc = FileWatcherProcess(self)                                                                                                           #
                                                                                                                                                       #
    def startServer(self):                                                                                                                             #
                                                                                                                                                       #
        """Starts the server"""                                                                                                                        #
                                                                                                                                                       #
        args = [r"filewatcher\\FileWatcher.exe", "--authorized: sadn29ue299sa[0as9yy19qldSDNX[OOJASPE29QE39G33QGLJLASBPA229"]                          #
        self.proc.startProcess(args)                                                                                                                   #
                                                                                                                                                       #
        server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)                                                                    #
        try:                                                                                                                                           #
            server.serve_forever()                                                                                                                     #
        except Exception:                                                                                                                              #
            ctypes.windll.user32.MessageBoxA(0, ctypes.c_char_p("Check if a server instance \nis already running, then try again.".encode("utf-8")),   #
                ctypes.c_char_p("Unexpected error".encode("utf-8")), 0x00000000 | 0x00000010 | 0x00001000)                                             #
            self.proc.closeProcess()                                                                                                                   #
            sys.exit(0)                                                                                                                                #
#******************************************************************************************************************************************************#


#******************************************************************************************************************************************************#
class FileWatcherProcess:                                                                                                                              #
                                                                                                                                                       #
    """Represents the process of FileWatcher"""                                                                                                        #
                                                                                                                                                       #
    def __init__(self, server):                                                                                                                        #
        self.server = server                                                                                                                           #
        self.proc = None                                                                                                                               #
        self.workingDirectory = None                                                                                                                   #
        self.htmlFile = None                                                                                                                           #
                                                                                                                                                       #
    def startProcess(self, args):                                                                                                                      #
                                                                                                                                                       #
        """Starts the process"""                                                                                                                       #
                                                                                                                                                       #
        try:                                                                                                                                           #
            self.proc = subprocess.Popen(args, stdout=subprocess.PIPE)                                                                                 #
            threading.Thread(target = FileWatcherProcess.parse_output, args = [self]).start()                                                          #
        except Exception:                                                                                                                              #
            if ctypes.windll.user32.MessageBoxA(0, ctypes.c_char_p("Make sure app file tree is correct and filewatcher folder contains all "           #
                "required files. Do you want to see more info on how to solve this?".encode("utf-8")), ctypes.c_char_p("FileWatcher not started"       #
                .encode("utf-8")), 0x00000004 | 0x00000020 | 0x00001000) == 6:                                                                         #
                                                                                                                                                       #
                os.system("start https://github.com/INeedADollar/Reload-Server#how-to-use")                                                            #
                                                                                                                                                       #
            sys.exit(0)                                                                                                                                #
                                                                                                                                                       #
    def closeProcess(self):                                                                                                                            #
                                                                                                                                                       #
        """Closes the process"""                                                                                                                       #
                                                                                                                                                       #
        try:                                                                                                                                           #
            self.proc.terminate()                                                                                                                      #
        except Exception:                                                                                                                              #
            pass                                                                                                                                       #
                                                                                                                                                       #
    @staticmethod                                                                                                                                      #
    def parse_output(fileWatcherProcess):                                                                                                              #
                                                                                                                                                       #
        """Static method that parses the process output"""                                                                                             #
                                                                                                                                                       #
        while True:                                                                                                                                    #
            line = fileWatcherProcess.proc.stdout.readline().decode("utf-8")                                                                           #
                                                                                                                                                       #
            if line == '':                                                                                                                             #
                break;                                                                                                                                 #
                                                                                                                                                       #
            if line == "Reload site\r\n":                                                                                                              #
                try:                                                                                                                                   #
                    globalWS.send("Reload")                                                                                                            #
                except Exception:                                                                                                                      #
                    pass                                                                                                                               #
                                                                                                                                                       #
                FileWatcherProcess.close_proc(fileWatcherProcess)                                                                                      #
                                                                                                                                                       #
                args = [r"filewatcher\\FileWatcher.exe", "--authorized: sadn29ue299sa[0as9yy19qldSDNX[OOJASPE29QE39G33QGLJLASBPA229"]                  #
                                                                                                                                                       #
                if os.path.exists(fileWatcherProcess.htmlFile):                                                                                        #
                    args.append(fileWatcherProcess.htmlFile)                                                                                           #
                else:                                                                                                                                  #
                    fileWatcherProcess.workingDirectory = None                                                                                         #
                    fileWatcherProcess.htmlFile = None                                                                                                 #
                    ctypes.windll.user32.MessageBoxA(0, ctypes.c_char_p("Selected HTML file was moved or deleted! Please choose other file!"           #
                        .encode("utf-8")), ctypes.c_char_p("File deleted".encode("utf-8")), 0x00000000 | 0x00000040 | 0x00001000)                      #
                                                                                                                                                       #
                fileWatcherProcess.startProcess(args)                                                                                                  #
                break                                                                                                                                  #
                                                                                                                                                       #
            if fileWatcherProcess.workingDirectory == None:                                                                                            #
                fileWatcherProcess.htmlFile = line[:-2]                                                                                                #
                fileWatcherProcess.workingDirectory = line[:-2].replace(line[:-2].split("/")[-1], "")                                                  #
                                                                                                                                                       #
                if fileWatcherProcess.workingDirectory == "":                                                                                          #
                    ctypes.windll.user32.MessageBoxA(0, ctypes.c_char_p("Choose a HTML file in order to use this app!".encode("utf-8")),               #
                        ctypes.c_char_p("No file chosen".encode("utf-8")), 0x00000000 | 0x00000040 | 0x00001000)                                       #
                                                                                                                                                       #
                    args = [r"filewatcher\\FileWatcher.exe", "--authorized: sadn29ue299sa[0as9yy19qldSDNX[OOJASPE29QE39G33QGLJLASBPA229"]              #
                    fileWatcherProcess.startProcess(args)                                                                                              #
                                                                                                                                                       #
                    fileWatcherProcess.workingDirectory = None                                                                                         #
                    fileWatcherProcess.htmlFile = None                                                                                                 #
                    break                                                                                                                              #
                                                                                                                                                       #
    @staticmethod                                                                                                                                      #
    def close_proc(fileWatcherProcess):                                                                                                                #
                                                                                                                                                       #
        """Static method for closing the process. Used when needing a static method"""                                                                 #
                                                                                                                                                       #
        if isinstance(fileWatcherProcess, FileWatcherProcess):                                                                                         #
            fileWatcherProcess.closeProcess()                                                                                                          #
#******************************************************************************************************************************************************#

 
#******************************************************************************************************************************************************#
app = Flask(__name__)   #Flask app instance                                                                                                            #
sockets = Sockets(app)  #Sockets instance                                                                                                              #
server = Server()       #Server instance                                                                                                               #
                                                                                                                                                       #
@sockets.route('/', defaults={'path': ''})                                                                                                             #
@sockets.route('/<path:path>')                                                                                                                         #
def echo_socket(ws, path = None):                                                                                                                      #
                                                                                                                                                       #
    """Method for socket routing"""                                                                                                                    #
                                                                                                                                                       #
    if path == None or server.proc.htmlFile == None or path != server.proc.htmlFile.split("/")[-1]:                                                    #
        return                                                                                                                                         #
                                                                                                                                                       #
    print(colors.GREEN + "SOCKET CONNECTED")                                                                                                           #
    global globalWS                                                                                                                                    #
    globalWS = ws                                                                                                                                      #
                                                                                                                                                       #
    while not ws.closed:                                                                                                                               #
        message = ws.receive()                                                                                                                         #
        try:                                                                                                                                           #
            ws.send(message)                                                                                                                           #
        except Exception:                                                                                                                              #
            pass                                                                                                                                       #
                                                                                                                                                       #
    print(colors.RED + "SOCKET DISCONNECTED\n\n")                                                                                                      #
                                                                                                                                                       #
@app.route('/', defaults={'path': ''})                                                                                                                 #
@app.route('/<path:path>')                                                                                                                             #
def catch_all(path):                                                                                                                                   #
                                                                                                                                                       #
    """Method for handling all flask routes"""                                                                                                         #
                                                                                                                                                       #
    if server.proc.workingDirectory != None:                                                                                                           #
        file = server.proc.workingDirectory + path                                                                                                     #
        if os.path.isfile(file):                                                                                                                       #
            return send_file(file)                                                                                                                     #
                                                                                                                                                       #
        return "File not found", 404                                                                                                                   #
                                                                                                                                                       #
    return "File not found", 404                                                                                                                       #
#******************************************************************************************************************************************************#


#******************************************************************************************************************************************************#
if __name__ == "__main__":                                                                                                                             #
                                                                                                                                                       #
    """Main"""                                                                                                                                         #
                                                                                                                                                       #
    os.system("")                                                                                                                                      #
    hide_cursor()                                                                                                                                      #
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0                                                                                                        #
                                                                                                                                                       #
    atexit.register(FileWatcherProcess.close_proc, [server.proc])                                                                                      #
    server.startServer()                                                                                                                               #
#******************************************************************************************************************************************************#

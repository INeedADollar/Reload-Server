# Reload-Server
[![Python](https://img.shields.io/badge/language-python-%23fff800?style=plastic&logo=appveyor)](https://en.wikipedia.org/wiki/Python_(programming_language))
[![C++](https://img.shields.io/badge/language-C%2B%2B-%23f34b7d.svg?style=plastic)](https://en.wikipedia.org/wiki/C%2B%2B)
[![Windows](https://img.shields.io/badge/platform-Windows-0078d7.svg?style=plastic)](https://en.wikipedia.org/wiki/Microsoft_Windows)
[![License](https://img.shields.io/github/github/license/INeedADollar/Reload-Server?style=plastic)](LICENSE)

Windows app that let's you build a website easier by reloading it at every file save. It also supports css and javascript files, updating the list of files to watch for changes at every file save. P.S. Browser with WebSockets support needed in order to work!

## Using app

To start using the app, even if you compiled yourself or you downloaded from [Releases section](https://github.com/INeedADollar/Reload-Server/releases), you need to have a file structure like this:

![image](https://user-images.githubusercontent.com/58915954/116579595-339bed00-a91b-11eb-944b-faaa45dc2f58.png)

Server.exe it's the [Python server](src/server/server.py) and filewatcher it's a folder that contains [FileWatcher app](src/filewatcher) that watches files for changes. 

### Steps to follow
1. Open server.exe (If you are prompted to allow access in Windows Firewall, press Allow Access button) 
2. A window to choose your website HTML file will appear on the screen. Go to your website folder and choose that HTML file 
<br>(Don't worry about script added in your HTML file, it's only for reloading your webpage, you can delete it when you finished the site)
4. Open a browser that supports WebSockets and type `localhost:5000/<your-website_file-name>.html`
5. Make sure you have a green message saying `SOCKET CONNECTED` in console. If you don't have this message reload won't work. (TIP: Make sure you typed the address correctly in your browser)
6. Have fun using the app. If you have any recommendations feel free to post in the [Discussions section](https://github.com/INeedADollar/Reload-Server/discussions) and any bugs you find post in [Issues](https://github.com/INeedADollar/Reload-Server/issues). Thank you! 🤗


https://user-images.githubusercontent.com/58915954/116588167-e112fe80-a923-11eb-8a01-30d18cf16b09.mp4


## Build

### Prerequisites
[Python 3.5+](https://www.python.org/downloads/), [Microsoft Visual Studio 2019](https://visualstudio.microsoft.com/) (latest version recommended) with Windows SDK and C++ package installed, [Qt Library 5.14](https://www.qt.io/download) (it should work with newer versions too) with [Visual Studion Qt Plugin](https://marketplace.visualstudio.com/items?itemName=TheQtCompany.QtVisualStudioTools-19123).
Don't worry if you use Qt Creator, you can forgot about Visual Studio requirements. Just create a Qt Creator project and add FileWatcher files to it.
  
### Download and build
* **FileWatcher build**

&emsp;&emsp;1. Open Visual Studio and select `Open a project` option. Go to folder where you have source code of [FileWatcher](src/filewatcher) and select `FileWatcher.sln` file.

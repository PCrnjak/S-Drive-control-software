[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


# S-Drive-control-software

![ezgif com-video-to-gif](https://user-images.githubusercontent.com/30388414/90382676-5c2ad200-e07f-11ea-8ffd-85459f8b4fb1.gif)

S-Drive control software lets you control and monitor S-Drive motor from PC.
This version supports plotting, showing data and controlling of only one motor at the time.

# Repository structure:
* master branch (latest version)
  * python script
  * windows exe
  * linux exe
  * user guide
* old versions
  
# How to install it?
1. Run it as python script
* Debendancies: `time`, `webbrowser`, `serial`, `numpy`, `tkinter`, `PIL`, `matplotlib`

2. Run it as exe on win10 x64 machine

# How to use it :
In S-Drive firmware you NEED to make `Main_serial_output_time` variable in Motor_parameters file MINIMUM 50 ms. If it is more PROGRAM WILL NOT WORK!
Connect your S-Drive board to PC.
Run software and enter your baud rate and COM port
Click connect.
Now you should see live data and be able to send commands

# Versions:
* Current S-Drive software version: 2.0
* compatible with S-Drive firmware version: 2.0
* compatible with S-Drive board version: 3.0, 3.1

# Support the project

This project is completely Open source and free to all and I would like to keep it that way, so any help 
in terms of donations or advice is really appreciated. Thank you!

[![Donate !](https://user-images.githubusercontent.com/30388414/86798915-a036ba00-c071-11ea-824d-4456f2cdf797.png)](https://paypal.me/PCrnjak?locale.x=en_US)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

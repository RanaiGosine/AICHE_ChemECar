# pHIRST CHEM-E-CAR STOPPING MECHANISM 
## DATA COLLECTION

The script `pressure-sensor.ino` is an arduino script that takes pressure data from the **Sparkfun Qwiic MicroPressure Sensor**, and sends it live through a COM port to which it is connected. When uploaded, pins **A4** and **A5** serve as **SCA** and **SCL** lines respectively.

The script `p_readout.py` provides a GUI for plotting the pressure data live. This data is saved to `pressure-data.csv` by default. `pressure-data.csv` should be deleted or renamed at the start of a new experiment. The script can also use _polynomial regression_ to fit a polynomial curve to the data.

## IMPORTANT NOTES

1) The COM port needs to be specified in the .py script depending on what port the arduino is connected to. the default is set to COM5.

2) The arduino script does not need to be uploaded each time the arduino is connected, unless some code was changed. There is no need to run the arduino IDE everytime the arduino is connected.

3) The code has been tested on an arduino NANO and arduino UNO and confirmed to work.

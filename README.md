First, I have to say, I AM NOT A PROGRAMMER!!!

A shout out to llamaXc for his WinWing Python code I used to send Explane12 data to the WW UFC without which this would never work.

Acknowledgments to the countless authors of python code I referenced on the interweb get this to work.

SinAppPro has to be running, then start Xplane


you most likly need to change these settings in the mainUdp.py file,  they are specific to my machine

  UDP_IP1 = "192.168.1.169"
  UDP_PORT1 = 49000
  
Also you can assign different datrefs to change the displayed data

my setting are
      ("sim/cockpit/radios/com1_freq_hz","hz","Com1 frequency",0),
      scratchPadNumbers =("sim/cockpit/radios/nav1_freq_hz", "hz", "Nav1 frequency",0), #current displayed
      option1 =("sim/cockpit2/gauges/indicators/radio_altimeter_height_ft_pilot","ft", "Radio-altimeter indicated height in feet, pilot-side	", 0), 
      option2 =("sim/flightmodel/position/mag_psi", "°", "The real magnetic heading of the aircraft",0),
      option3 =("sim/flightmodel/position/indicated_airspeed", "kt", "Air speed indicated - this takes into account air density and wind direction",0), 
      option4 =("sim/flightmodel/position/groundspeed","m/s", "The ground speed of the aircraft",0),
      option5 =("sim/cockpit/autopilot/heading_mag", "°", "The heading to fly ",0)


from ufc import UFCSimAppProHelper
import socket
import json
import binascii
import struct 
import math
import config
opt1 = 0
opt2 = 0
opt3 = 0
opt4 = 0
opt5 = 0
nav1 = 0
comm1 = 0
VHFString1 =""
start = 0 


#***************************************************************************************
def xplaneUDP():
# IP Address of machine running X-Plane. 

  UDP_IP1 = "192.168.1.169"
  UDP_PORT1 = 49000

  sock = socket.socket(socket.AF_INET, # Internet
                    socket.SOCK_DGRAM) # UDP

      # Open a Socket on UDP Port 49000



  # List of datarefs to request. 
  datarefs = [
      # ( dataref, unit, description, num decimals to display in formatted output )
      ("sim/cockpit/radios/com1_freq_hz","hz","Com1 frequency",0),
      ("sim/cockpit/radios/nav1_freq_hz", "hz", "Nav1 frequency",0),
      ("sim/cockpit2/gauges/indicators/radio_altimeter_height_ft_pilot","ft", "Radio-altimeter indicated height in feet, pilot-side	", 0), 
      ("sim/flightmodel/position/mag_psi", "°", "The real magnetic heading of the aircraft",0),
      ("sim/flightmodel/position/indicated_airspeed", "kt", "Air speed indicated - this takes into account air density and wind direction",0), 
      ("sim/flightmodel/position/groundspeed","m/s", "The ground speed of the aircraft",0),
      ("sim/cockpit/autopilot/heading_mag", "°", "The heading to fly ",0)
    ]

  def RequestDataRefs(sock):
      for idx,dataref in enumerate(datarefs):
        # Send one RREF Command for every dataref in the list.
        # Give them an index number and a frequency in Hz.
        # To disable sending you send frequency 0. 
        cmd = b"RREF\x00"
        freq=1
        string = datarefs[idx][0].encode()
        message = struct.pack("<5sii400s", cmd, freq, idx, string)
        assert(len(message)==413)
        sock.sendto(message, (UDP_IP1, UDP_PORT1))

  def DecodePacket(data):
        retvalues = {}
        # Read the Header "RREF,".
        header=data[0:5]
        if(header!=b"RREF,"):
          print("Unknown packet: ", binascii.hexlify(data))
        else:
          # We get 8 bytes for every dataref sent:
          #    An integer for idx and the float value. 
          values =data[5:]
          lenvalue = 8
          numvalues = int(len(values)/lenvalue)
          idx=0
          value=0
          for i in range(0,numvalues):
            singledata = data[(5+lenvalue*i):(5+lenvalue*(i+1))]
            (idx,value) = struct.unpack("<if", singledata)
            retvalues[idx] = (value, datarefs[idx][1], datarefs[idx][0])
        return retvalues



  RequestDataRefs(sock)
  global start
  while True:
    # Receive packet
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    # Decode Packet
    values = DecodePacket(data)
    # Example values:
    # {
    #   0: (  47.85240554 , '°N'  , 'sim/flightmodel/position/latitude'           ),
    #   1: (  12.54742622 , '°E'  , 'sim/flightmodel/position/longitude'          ),
    #   2: (  1502.2      , 'ft'  , 'sim/flightmodel/misc/h_ind'                  ),
    #   3: (  0.01        , 'm'   , 'sim/flightmodel/position/y_agl'              ),
    #   4: (  76.41       , '°'   , 'sim/flightmodel/position/mag_psi'            ),
    #   5: ( -9.76e-05    , 'kt'  , 'sim/flightmodel/position/indicated_airspeed' ),
    #   6: (  1.39e-05    , 'm/s' , 'sim/flightmodel/position/groundspeed'        ),
    #   7: ( -1.37e-06    , 'm/s' , 'sim/flightmodel/position/vh_ind'             )
    # }

    # Print Values:
    
    for key,val in values.items():
      
      #print(("{0:10."+str(datarefs[key][3])+"f}").format(val[0]))
      # print(("{0:10."+str(datarefs[key][3])+"f} {1:<5} {2}").format(val[0],val[1],val[2]))
      # print()
      match key:
        case 0:
          global comm1
          comm1 = "{: .0f}".format(val[0]*10)
        case 1:
          global nav1
          nav1 =  "{: .0f}".format(val[0]*10)
        case 2:
          global opt1  # radar altimeter
          opt1 = val[0]
          if (opt1 > 2500):
            opt1 = 9999
          opt1 ="{:.0f}".format(opt1)
          opt1 = str(opt1).zfill(4) 
            
        case 3:
          global opt2 #mag headind
          opt2 = val[0]
          opt2 ="{:.0f}".format(opt2)
          opt2 = str(opt2).zfill(3)           
        case 4:
          global opt3 # air speed knots
          opt3 = val[0]          
          opt3 ="{:.0f}".format(opt3)
          opt3 = str(opt3).zfill(3)          
        case 5:
          global opt4 #groung speed knots
          opt4 = val[0]
          opt4 = val[0]*1.94384
          opt4 ="{:.0f}".format(opt4)
          opt4 = str(opt4).zfill(3)          
        case 6:
          global opt5 # heading bug
          opt5 = val[0]
          opt5 ="{:.0f}".format(opt5)
          opt5 = str(opt5).zfill(3)        

    

      #send_json_udp_message(simapp_pro_ufc_payload)

    UDf()

      
      
#******************************************************************************************************************

def UDf():
  global start
  def send_json_udp_message(json_data, host='localhost', port=16536):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(json.dumps(json_data).encode('utf-8'), (host, port))
  if(start==0):   # only run once
    start = 1
    simapp_pro_start_messages = [
      {"func": "net", "msg": "ready"},
      {"func": "mission", "msg": "ready"},
      {"func": "mission", "msg": "start"},
      {"func": "mod", "msg": "FA-18C_hornet"}
    ]

    
    # Connect to SimApp Pro and prepare to start receiving data
    for payload in simapp_pro_start_messages:
      send_json_udp_message(payload)


    # Create a UFC payload
  ufc_payload = {
      "option1": str(opt1), 
      "option2": str(opt2),
      "option3": str(opt3),
      "option4": str(opt4),
      "option5": str(opt5),
      "com1": "T",
      "com2": "6",
      "scratchPadNumbers": str(nav1),
      "scratchPadString1": "I",
      "scratchPadString2": "L",
      "selectedWindows": ["1"]
      }
  ufcHelper = UFCSimAppProHelper(ufc_payload)

  # Create the SimApp Pro messaged it needs to update the UFC
  simapp_pro_ufc_payload = {
      "args": {
          "FA-18C_hornet": ufcHelper.get_ufc_payload_string(),
      },
      "func": "addCommon",
      "timestamp": 0.00
  }

  simapp_pro_set_brightness = {
      "args": {
          "0": {
              "109": "0.95"
          }
      },
      "func": "addOutput",
      "timestamp": 0
  }

  # Send message to SimApp Pro
  send_json_udp_message(simapp_pro_ufc_payload)
# send_json_udp_message(simapp_pro_set_brightness)


def main():
    xplaneUDP()
    #UDf()

if __name__ == '__main__':
  main()
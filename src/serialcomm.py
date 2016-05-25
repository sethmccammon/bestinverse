import serial
import time

class serialComm:
  def __init__(self, port_in = '/dev/ttyACM0'):
    self.port = port_in
    if "dummy_port" in port_in:
      print "Initializing Serial Comm to Dummy Port"
      self.valid = True
    else:
      self.valid = False
      try:
        self.ser = serial.Serial(self.port, 9600, timeout=10)
        self.valid = True
        self.max_msg_len = 16

      except serial.serialutil.SerialException:
        print 'Error: Comm Closed'




  def sendPacket(self, msg, timeout = .1):
    
    max_msg_len = 16
    if len(msg) > max_msg_len:
      print "Error: Message Longer than Max Length"
      return 0
    else:
      if "dummy_port" in self.port:
        print "~"+msg
      else:
        print "~"+msg
        self.ser.write('~'+msg)
    start_time = time.time()


    while True:
      response = self.ser.readline()
      print response
      if "OK" in response:
        return



def buildMsg(msg_type, args = []):
  if msg_type == 0: #GOTO MESSAGE
    if len(args) is not 2:
      print "Incorrect Args for type: GOTO"
    else:
      msg = "0:" + ("%.3f" % args[0]) + "," + ("%.3f" % args[1])

  elif msg_type == 1: #Calibration
    msg = "1:"

  elif msg_type == 2: #go fishing
    msg = "2:"

  elif msg_type == 3: #deposit Fish
    msg = "3:"

  else:
    print "Invalid Message Type"
    return None

  return msg


def main():
  comm = serialComm()
  while True:
    v1 = random.randint(0, 1)
    v2 = random.randint(0, 180)
    v3 = random.randing(0, 10)
    msg = "A:{} B:{} C:{}".format(v1, v2, v3)

    comm.sendPacket(msg)
    




if __name__ == '__main__':
  main()
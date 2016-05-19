import serial
from time import sleep

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
        return self.ser.write('~'+msg)


def buildMsg(msg_type, args = []):
  if msg_type == 0: #GOTO MESSAGE
    if len(args) is not 2:
      print "Incorrect Args for type: GOTO"
    else:
      msg = '1:'
      msg = msg + str(int(args[0]))#struct.pack('!b', args[0])
      msg = msg + "," + str(int(args[1]))#struct.pack('!b', args[1])
  if msg_type == 1: #Calibration
    msg = "2:"
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
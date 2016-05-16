import serial
from time import sleep

class serialComm:
  def __init__(self, port_in = '/dev/ttyACM0'):
    self.port = port_in
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
      return self.ser.write('~'+msg)



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
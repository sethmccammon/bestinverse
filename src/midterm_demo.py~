import sys, select, termios, tty
from serialcomm import serialComm



def main():
  comm = serialComm()


  print "WASD to move the X-Y table, F to grab a fish, q to quit"
  settings = termios.tcgetattr(sys.stdin)


  while True:
    x_dir = 0
    y_dir = 0
    fish = 0
    key = getKey(settings)
    # if key:
    #   print key
    if key == 'q':
      break
    elif key == 'w':
      y_dir = 1
    elif key == 's':
      y_dir = -1
    elif key == 'a':
      x_dir = -1
    elif key == 'd':
      x_dir = 1
    elif key == 'f':
      fish = 1

    msg = struct.pack('!b', x_dir)
    msg = msg + "$" + struct.pack('!b', y_dir)
    msg = msg + "%" + struct.pack('!b', fish)
    print msg
    comm.sendPacket(msg)


def getKey(settings):
  tty.setraw(sys.stdin.fileno())
  rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
  if rlist:
    key = sys.stdin.read(1)
  else:
    key = ''
  termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
  return key

if __name__ == "__main__":
  main()
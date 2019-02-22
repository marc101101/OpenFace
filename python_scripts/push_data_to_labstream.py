import sys
import time
k = 0
try:
    buff = ''
    while True:
        buff += sys.stdin.read(1)
        if buff.endswith('\n'):
            print("this is python log: "  +  buff[:-1])
            buff = ''
            k = k + 1
except KeyboardInterrupt:
   sys.stdout.flush()
   pass
print("End of Log: "  + str(k))
import time
from datetime import datetime

def log(msg):
    f = open("out.log", 'a')
    ts = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    f.write('[%s] %s\n' % (ts, msg))
    f.flush()
    f.close()    
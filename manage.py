import os
import sys
from server import Server
if __name__ == '__main__':
    try:
        Server(sys.argv[1].split(':')[0],int(sys.argv[1].split(':')[1]))
    except:
        pass

import os
import sys
from server import P2PServer
if __name__ == '__main__':
    try:
        P2PServer((sys.argv[1].split(':')[0], int(sys.argv[1].split(':')[1])))
    except:
        pass

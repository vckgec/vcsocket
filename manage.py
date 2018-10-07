import os
import sys
from server import P2PServer
if __name__ == '__main__':
    # try:
    P2PServer((sys.argv[1].split(':')[0].strip(), int(sys.argv[1].split(':')[1].strip())))
    # except Exception as e:
    #     print(e)

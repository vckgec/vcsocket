import os
import sys
from server import Server
if __name__ == '__main__':
    # try:
    Server((sys.argv[1].split(':')[0].strip(), int(sys.argv[1].split(':')[1].strip())))
    # except Exception as e:
    #     print(e)
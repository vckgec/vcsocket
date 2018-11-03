import struct
from collections import namedtuple

def mask(data,masking_key):
        """
        Performs the masking or unmasking operation on data
        using the simple masking algorithm:
        ..
           j                   = i MOD 4
           transformed-octet-i = original-octet-i XOR masking-key-octet-j
        """
        masked = bytearray(data)
        key = masking_key.encode()
        for i in range(len(data)):
            masked[i] = masked[i] ^ key[i%4]
        return masked

def unmask(masked_data,masking_key):
    masked_data = bytearray(masked_data)
    for i in range(len(masked_data)):
        masked_data[i] = masked_data[i]^masking_key[i%4]
    return masked_data

def encodeMessage(data,masking_key="None",OPCODE=0x1,FIN=1,RSVI1=0,RSVI2=0,RSVI3=0):
        # data = data.encode()
        ## +-+-+-+-+-------+
        ## |F|R|R|R| opcode|
        ## |I|S|S|S|  (4)  |
        ## |N|V|V|V|       |
        ## | |1|2|3|       |
        ## +-+-+-+-+-------+

        ## ((FIN << 7) | (RSVI1 << 6) | (RSVI2 << 5) | (RSVI3 << 4) | OPCODE ) = [128 + 0 + 0 + 0 + 1]
        ## header = bytes([129])

        header = struct.pack('!B', ((FIN << 7)
                             | (RSVI1 << 6)
                             | (RSVI2 << 5)
                             | (RSVI3 << 4)
                             | OPCODE ))

        ##                 +-+-------------+-------------------------------+
        ##                 |M| Payload len |    Extended payload length    |
        ##                 |A|     (7)     |             (16/63)           |
        ##                 |S|             |   (if payload len==126/127)   |
        ##                 |K|             |                               |
        ## +-+-+-+-+-------+-+-------------+ - - - - - - - - - - - - - - - +
        ## |     Extended payload length continued, if payload len == 127  |
        ## + - - - - - - - - - - - - - - - +-------------------------------+
        if masking_key: mask_bit = 1 << 7
        else: mask_bit = 0

        length = len(data)
        if length < 126:
            header += struct.pack('!B', (mask_bit | length))
        elif length < (1 << 16):
            header += struct.pack('!B', (mask_bit | 126)) + struct.pack('!H', length)
        elif length < (1 << 63):
            header += struct.pack('!B', (mask_bit | 127)) + struct.pack('!Q', length)        
        ## + - - - - - - - - - - - - - - - +-------------------------------+
        ## |                               |Masking-key, if MASK set to 1  |
        ## +-------------------------------+-------------------------------+
        ## | Masking-key (continued)       |          Payload Data         |
        ## +-------------------------------- - - - - - - - - - - - - - - - +
        ## :                     Payload Data continued ...                :
        ## + - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +
        ## |                     Payload Data continued ...                |
        ## +---------------------------------------------------------------+
        if not masking_key:
            return bytes(header + data)
        return bytes(header + masking_key.encode() + mask(data,masking_key))

def decodeMessage(message):
    seek = 0
    header = message[seek:seek+2]
    seek +=2
    b1 = header[0]
    fin = b1 >> 7 & 1
    rsv1 = b1 >> 6 & 1
    rsv2 = b1 >> 5 & 1
    rsv3 = b1 >> 4 & 1
    opcode = b1 & 0xf
    b2 = header[1]
    has_mask = b2 >> 7 & 1
    length_bits = b2 & 0x7f

    if length_bits == 126:
        length_bits = struct.unpack(">H", message[seek:seek+2])[0]
        seek+=2

    if length_bits == 127:
        length_bits = struct.unpack(">Q",message[seek:seek+length_bits])[0]
        seek+=8

    if has_mask:
        masking_key = message[seek:seek+4] #4 bit mask
        seek+=4        
        masked_data = message[seek:seek+length_bits]
        data = unmask(masked_data,masking_key)
    else:
        data = message[seek:seek+length_bits]
    seek += length_bits
    return data

def addr_from_args(args, host='127.0.0.1', port=9999):
    if len(args) >= 3:
        host, port = args[1], int(args[2])
    elif len(args) == 2:
        host, port = host, int(args[1])
    else:
        host, port = host, port
    return host, port


def msg_to_addr(data):
    ip, port = data.decode('utf-8').strip().split(':')
    return (ip, int(port))


def addr_to_msg(addr):
    return '{}:{}'.format(addr[0], str(addr[1])).encode('utf-8')

def send_msg(sock, msg):
    sock.sendall(encodeMessage(msg))

def recv_msg(sock):
    data = sock.recv(1024)
    data = decodeMessage(data)
    return data

class Client(namedtuple('Client', 'conn, pub, priv')):

    def peer_msg(self):
        return addr_to_msg(self.pub) + b'|' + addr_to_msg(self.priv)
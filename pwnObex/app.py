#-import serial #not pyserial :angry: -> https://pyserial.readthedocs.io/en/latest/pyserial.html
import pwintools
import struct
import time

# 16 bit int to big endian bytes
def b16(i): 
    return struct.pack('>H', i)

def obex_get(s):
    
    l = len(s) + 1 #string + null byte
    l = l * 2 # because two-byte chars are mandatory
    l = l + 2 + 1 # len=len + 2-byte length specifier + 1-byte request type specifier
    
    lhs = b"\x83" + b16(l)
    
    rhs = b""
    for c in s:
        rhs = rhs + b"\x00"+c.encode("ascii")
    
    rhs = rhs + b"\x00\x00" # null byte; rhs is over    
    
    ret = lhs+rhs 
    print(ret)
    return ret

io = pwintools.serialtube("COM8", baudrate=115200)
if(io.conn.isOpen() == False):
    io.conn.open()
print("ready")
buf = "ATI" #aka AT HI
print(buf)
io.sendline(buf)
buf = "AT+CPROT=?"
print(buf)
io.sendline(buf)
print(io.recvuntil("OK"))
print(" Okay")
print(io.recvall())

# https://www.ixbt.com/mobile/review/obex.shtml
# CONNECT
print("0. CPROT attempt")
io.sendline('AT+CPROT=0,"V1.0", 1', flush=False)
print("1. OBEX MODE")
print("2. Connect")
io.send_raw(bytearray.fromhex("43 4F 4E 4E 45 43 54 0D 0A"))
print(io.recvall())
print("3. OBEX 1.0: IRMC-SYNC")
io.send_raw(bytearray.fromhex("80 00 13 10 00 40 00 46 00 0C 49 52 4D 43 2D 53 59 4E 43"))
print(io.recvall())
print("4. OBEX 1.0: 7 bytes")
io.send_raw(bytearray.fromhex("A0 00 07 10 00 00 FF"))
print(io.recvall())
print("5. Get shuff")
buf = "\My Images\Frames\Jean.PNG"
print( "Trying for: "+buf)
io.send_raw(obex_get(buf))
time.sleep(0.5)
io.recvall()


#n =  nOBEX.Client("0.0.0.0", 1)

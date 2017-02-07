from socket import *
import thread
import re

BUFFSIZE	= 8192
HOST 		= '127.0.0.1'
PORT 		= 5544 
REGEX 		= re.compile( '.+\r\ncontent-length\s*:\s*' , re.IGNORECASE|re.DOTALL)
HOST_ATS	= '198.143.12.140'

def get_cont_len(data):
	chunk 	= REGEX.sub( '' , data)
	if chunk==data:
		return 'not found'
	else:
		return int(chunk.split('\r\n')[0] )

def handler(src_sock , dest_sock):
	while 1:
		try 	:
			data = src_sock.recv(BUFFSIZE)
			#if not data: break
			if (data.startswith('HTTP')) or (data.startswith('POST')) :
				print ':: ' ,get_cont_len(data) , ' ::\n'
			dest_sock.sendall(data)
		except:
			break
 
if __name__=='__main__':
	ADDR = (HOST, PORT)
	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serversock.bind(ADDR)
	serversock.listen(5)
	while 1:
		try	:	ua_sock, addr	= serversock.accept()
		except	:	break
		ats_sock = socket( AF_INET, SOCK_STREAM)
		ats_sock.connect( (HOST_ATS , 54320) )
		#print '...connected from:', addr
		thread.start_new_thread(handler, (ua_sock, ats_sock))
		thread.start_new_thread(handler, (ats_sock ,ua_sock ))


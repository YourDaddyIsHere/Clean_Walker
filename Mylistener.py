import socket
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces
from struct import unpack_from
from socket import inet_aton
from Wcandidate import Wcandidate
from WcandidateGroup import WcandidateGroup
from twisted.internet import task
from twisted.internet import reactor
#from Mywalker import Mywalker

class Mylistener:
	walker = None
	sock = None
	loop_listening = None
	BUFSIZE = 2048
	def __init__(self,walker,sock):
		self.walker = walker
		self.sock = sock
		self.loop_listening = task.LoopingCall(self.listening)
	def listening(self):
		print 'wating for message...'  
		data, addr = self.sock.recvfrom(self.BUFSIZE)  
		print '...received from and retuned to:',addr
		print data
		message_decoded = TestMessage_pb2.TestMessage()
		message_decoded.ParseFromString(data)
		print "receving a "+ message_decoded.message_type
		if(message_decoded.message_type=="introduction-request"):
			#print "it is a introduction-request"
			self.walker.on_introduction_request(message_decoded,addr)
		if(message_decoded.message_type=="introduction-response"):
			#print "it is a introduction-response"
			self.walker.on_introduction_response(message_decoded,addr)
		if(message_decoded.message_type=="puncture-request"):
			#print "it is a puncture-request"
			self.walker.on_puncture_request(message_decoded,addr)
	def start(self):
		self.loop_listening.start(0.1)
		reactor.run()

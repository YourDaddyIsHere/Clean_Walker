import time
class Wcandidate:
	#wan and lan address should be a tuple (ip,port)
	WALK_LIMIT=57.5
	STUMBLE_LIMIT=57.5
	INTRO_LIMIT = 27.5
	NETMASK = ""
	LAN_IP=""
	LAN_PORT=0
	LAN_ADDR = None
	WAN_IP =""
	WAN_PORT=0
	WAN_ADDR = None
	last_walk_time = 0 
	last_stumble_time = 0
	last_intro_time = 0
	def __init__(self,lan,wan,netmask="255.255.255.0"):
		assert isinstance(lan,tuple)
		assert isinstance(wan,tuple)
		self.LAN_ADDR = lan
		self.WAN_ADDR = wan
		self.last_walk_time = time.time()
		self.last_stumble_time = time.time()
		self.last_intro_time = time.time()
		self.NETMASK = netmask

	def get_candidate_type(self):
		#return the type (walk,stumble,intro,none) of the candidate
		now = time.time()
		if(now-self.last_walk_time<self.WALK_LIMIT):
			return "walk"
		if(now-self.last_stumble_time<self.STUMBLE_LIMIT):
			return "stumble"
		if(now-self.last_intro_time<self.INTRO_LIMIT):
			return "intro"
		return "stale"
	def get_LAN_IP(self):
		return self.LAN_ADDR[0]
	def get_LAN_PORT(self):
		return self.LAN_ADDR[1]
	def get_LAN_ADDR(self):
		return self.LAN_ADDR
	def get_NETMASK(self):
		return self.NETMASK
	def get_WAN_IP(self):
		return self.WAN_ADDR[0]
	def get_WAN_PORT(self):
		return self.WAN_ADDR[1]
	def get_WAN_ADDR(self):
		return self.WAN_ADDR

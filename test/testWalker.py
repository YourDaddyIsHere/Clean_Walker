from random import random
import unittest  
import sys
sys.path.append("..")
print sys.path
from walker import Walker
from struct import pack, unpack_from, Struct
from twisted.internet import reactor
from socket import inet_ntoa, inet_aton

#the walker will bind to a port when greated(because it inherits twisted.DatagramProtocol)
#it won't be initiated before bind to a specific port
#so I can't put the walker in setUp() function, or it will be created multiple times (every time a test_XXXX() fucntion got called, the setUp() will be called once)
#that will cause a "Address already in use" Exception
walker = Walker(port=23334)
#walker.reactor.listenUDP(walker.lan_port, walker)
class Test_Walker(unittest.TestCase):  
  
    def setUp(self):  

        self.lan_ip = walker.lan_ip
        self.lan_port = walker.lan_port
        self.lan_netmask = walker.lan_netmask
        self.lan_addr = walker.lan_addr
        #we have no knowledge for our wan IP for now.
        self._struct_B = Struct(">B")
        self._struct_BBH = Struct(">BBH")
        self._struct_BH = Struct(">BH")
        self._struct_H = Struct(">H")
        self._struct_HH = Struct(">HH")
        self._struct_LL = Struct(">LL")
        self._struct_Q = Struct(">Q")
        self._struct_QH = Struct(">QH")
        self._struct_QL = Struct(">QL")
        self._struct_QQHHBH = Struct(">QQHHBH")
        self._struct_ccB = Struct(">ccB")
        self._struct_4SH = Struct(">4sH")

        self._encode_message_map = dict()  # message.name : EncodeFunctions
        self._decode_message_map = dict()  # byte : DecodeFunctions
        # the dispersy-introduction-request and dispersy-introduction-response have several bitfield
        # flags that must be set correctly
        # reserve 1st bit for enable/disable advice
        self._encode_advice_map = {True: int("1", 2), False: int("0", 2)}
        self._decode_advice_map = dict((value, key) for key, value in self._encode_advice_map.iteritems())
        # reserve 2nd bit for enable/disable sync
        self._encode_sync_map = {True: int("10", 2), False: int("00", 2)}
        self._decode_sync_map = dict((value, key) for key, value in self._encode_sync_map.iteritems())
        # reserve 3rd bit for enable/disable tunnel (02/05/12)
        self._encode_tunnel_map = {True: int("100", 2), False: int("000", 2)}
        self._decode_tunnel_map = dict((value, key) for key, value in self._encode_tunnel_map.iteritems())
        # 4th, 5th and 6th bits are currently unused
        # reserve 7th and 8th bits for connection type
        self._encode_connection_type_map = {u"unknown": int("00000000", 2), u"public": int("10000000", 2), u"symmetric-NAT": int("11000000", 2)}
        self._decode_connection_type_map = dict((value, key) for key, value in self._encode_connection_type_map.iteritems())

        self.master_key = "3081a7301006072a8648ce3d020106052b81040027038192000407afa96c83660dccfbf02a45b68f4bc" + \
                     "4957539860a3fe1ad4a18ccbfc2a60af1174e1f5395a7917285d09ab67c3d80c56caf5396fc5b231d84ceac23627" + \
                     "930b4c35cbfce63a49805030dabbe9b5302a966b80eefd7003a0567c65ccec5ecde46520cfe1875b1187d469823d" + \
                     "221417684093f63c33a8ff656331898e4bc853bcfaac49bc0b2a99028195b7c7dca0aea65"
        self.master_key_hex = self.master_key.decode("HEX")

        self.crypto = walker.crypto
        self.ec = walker.ec
        self.key = walker.key
        self.mid = walker.mid
        #the dispersy vesion and community version of multichain community version of multichain community in the tracker
        self.dispersy_version = walker.dispersy_version
        self.community_version = walker.community_version
        #print ord(self.community_version)
        #create my key in multichain community, and convert it to mid for signiture use
        self.prefix = walker.prefix
        self.my_key = walker.my_key
        self.my_mid = walker.my_mid
        self.my_public_key = walker.my_public_key


        candidate_to_walk = walker.get_candidate_to_walk()
        #print candidate_to_walk
        candidate_to_walk_ADDR = candidate_to_walk.get_WAN_ADDR()
        #message_puncture_request = self.create_puncture_request(("8.8.8.8",8),("8.8.8.8",8))
        message_introduction_request = walker.create_introduction_request(candidate_to_walk_ADDR,walker.lan_addr,walker.lan_addr)
        #message_puncture_request = self.create_puncture_request(("8.8.8.8",8),("8.8.8.8",8))

        #self.sock.sendto(message_introduction_request.packet,candidate_to_walk_ADDR)
        walker.transport.write(message_introduction_request.packet,candidate_to_walk_ADDR)
        #self.transport.write(message_puncture_request.packet,candidate_to_walk_ADDR)
        #walker.listening_port.stopListening()
    def tearDown(self):
        walker.listening_port.stopListening()

    def test_create_introduction_request(self):
        #the following three address are fabricated
        #only for test use
        destination_address = ("8.8.8.8",8)
        source_lan_address = ("192.168.1.200",20000)
        source_wan_address = ("35.1.2.3",20000)
        #use the walker to create a message
        message = walker.create_introduction_request(destination_address,source_lan_address,source_wan_address)
        #now we create a message using in a KNOWN CORRECT WAY
        identifier = message.identifier
        data = [inet_aton(destination_address[0]), self._struct_H.pack(destination_address[1]),
                inet_aton(source_lan_address[0]), self._struct_H.pack(source_lan_address[1]),
                inet_aton(source_wan_address[0]), self._struct_H.pack(source_wan_address[1]),
                self._struct_B.pack(self._encode_advice_map[True] | self._encode_connection_type_map[u"unknown"] | self._encode_sync_map[False]),
                self._struct_H.pack(identifier)]
        container = [self.prefix,chr(246)]
        #container.append(self.my_mid)
        my_public_key = self.my_public_key
        #container.extend((self._struct_H.pack(len(my_public_key)), my_public_key))
        container.append(self.my_mid)
        #now = int(time())
        now = self._struct_Q.pack(walker._global_time)
        container.append(now)
        container.extend(data)
        #print container
        packet = "".join(container)
        packet_len = len(packet)
        signiture = walker.crypto.create_signature(self.my_key, packet)
        packet = packet + signiture
        self.assertEqual(message.packet[0:packet_len],packet[0:packet_len])

    def test_create_introduction_response(self):
        identifier = int(random() * 2 ** 16)
        destination_address = ("8.8.8.8",8)
        source_lan_address = ("192.168.1.200",20000)
        source_wan_address = ("35.1.2.3",20000)
        lan_introduction_address = ("2.2.2.2",2)
        wan_introduction_address = ("3.3.3.3",3)
        data = (inet_aton(destination_address[0]), self._struct_H.pack(destination_address[1]),
                inet_aton(source_lan_address[0]), self._struct_H.pack(source_lan_address[1]),
                inet_aton(source_wan_address[0]), self._struct_H.pack(source_wan_address[1]),
                inet_aton(lan_introduction_address[0]), self._struct_H.pack(lan_introduction_address[1]),
                inet_aton(wan_introduction_address[0]), self._struct_H.pack(wan_introduction_address[1]),
                self._struct_B.pack(self._encode_connection_type_map[u"unknown"] | self._encode_tunnel_map[False]),
                self._struct_H.pack(identifier))
        container = [self.prefix,chr(245)]
        container.append(self.my_mid)
        now = self._struct_Q.pack(walker._global_time)
        container.append(now)
        container.extend(data)
        packet = "".join(container)
        signiture = self.crypto.create_signature(self.my_key, packet)
        packet_len = len(packet)
        packet = packet + signiture

        message = walker.create_introduction_response(identifier,destination_address,source_lan_address,source_wan_address,lan_introduction_address,wan_introduction_address)
        self.assertEqual(message.packet[0:packet_len],packet[0:packet_len])

    def test_create_puncture_request(self):
        lan_walker_addr = ("2.2.2.2",2)
        wan_walker_addr = ("3.3.3.3",3)
        message = walker.create_puncture_request(lan_walker_addr,wan_walker_addr)
        identifier = message.identifier
        data = (inet_aton(lan_walker_addr[0]), self._struct_H.pack(lan_walker_addr[1]),
                inet_aton(wan_walker_addr[0]), self._struct_H.pack(wan_walker_addr[1]),
                self._struct_H.pack(identifier))
        container = [self.prefix,chr(250)]
        #my_public_key = self.my_public_key
        now = self._struct_Q.pack(walker._global_time)
        container.append(now)
        container.extend(data)
        #print container
        packet = "".join(container)
        packet_len = len(packet)
        #since it uses NoAuthentication, the signiture is ""
        signiture =""
        packet = packet+signiture
        self.assertEqual(message.packet[0:packet_len],packet[0:packet_len])
    def test_create_puncture(self):
        pass
    def test_create_identity(self):
        message = walker.create_identity()
        identifier = message.identifier
        container = [self.prefix,chr(248)]
        #container.append(self.my_mid)
        #for dispersy-identity, it always uses "bin" as encoding
        #regardless of community-version
        my_public_key = self.my_public_key
        container.extend((self._struct_H.pack(len(my_public_key)), my_public_key))
        #now = int(time())
        #global_time = (self._global_time,0)
        #print "global time tuple is: "+str(global_time)
        #print type(global_time)
        now = self._struct_Q.pack(walker._global_time)
        container.append(now)
        data=()
        container.extend(data)
        #print container
        packet = "".join(container)
        packet_len = len(packet)
        signiture = self.crypto.create_signature(self.my_key, packet)
        packet = packet+signiture
        self.assertEqual(message.packet[0:packet_len],packet[0:packet_len])

    #now we have finished all encoding function test, we can assume all those functions are correct
    def test_decode_introduction_request(self):
        destination_address = ("8.8.8.8",8)
        source_lan_address = ("192.168.1.200",20000)
        source_wan_address = ("35.1.2.3",20000)
        #use the walker to create a message
        message = walker.create_introduction_request(destination_address,source_lan_address,source_wan_address)
        message_decode = walker.decode_introduction_request(message.packet)
        self.assertEqual(message.destination_addr,message_decode.destination_addr)
        self.assertEqual(message.sender_lan_addr,message_decode.sender_lan_addr)
        self.assertEqual(message.sender_wan_addr,message_decode.sender_wan_addr)
    def test_decode_introduction_response(self):
        identifier = int(random() * 2 ** 16)
        destination_address = ("8.8.8.8",8)
        source_lan_address = ("192.168.1.200",20000)
        source_wan_address = ("35.1.2.3",20000)
        lan_introduction_address = ("2.2.2.2",2)
        wan_introduction_address = ("3.3.3.3",3)
        message = walker.create_introduction_response(identifier,destination_address,source_lan_address,source_wan_address,lan_introduction_address,wan_introduction_address)
        message_decode = walker.decode_introduction_response(message.packet)
        self.assertEqual(message.destination_addr,message_decode.destination_addr)
        self.assertEqual(message.sender_lan_addr,message_decode.sender_lan_addr)
        self.assertEqual(message.sender_wan_addr,message_decode.sender_wan_addr)
        self.assertEqual(message.lan_introducted_addr,message_decode.lan_introducted_addr)
        self.assertEqual(message.wan_introducted_addr,message_decode.wan_introducted_addr)
    def test_decode_puncture_request(self):
        lan_walker_addr = ("2.2.2.2",2)
        wan_walker_addr = ("3.3.3.3",3)
        message = walker.create_puncture_request(lan_walker_addr,wan_walker_addr)
        message_decode = walker.decode_puncture_request(message.packet)
        self.assertEqual(message.lan_walker_addr,message_decode.lan_walker_addr)
        self.assertEqual(message.wan_walker_addr,message_decode.wan_walker_addr)

    def test_decode_missing_identity(self):
        pass

  
if __name__ == '__main__':  
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Walker)
    unittest.TextTestRunner(verbosity=2).run(suite)
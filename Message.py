
class message:
    def __init__(self,destination_address=None,source_lan_address=None,source_wan_address=None,lan_introduction_address=None,wan_introduction_address=None,lan_walker_address=None,
                wan_walker_address=None,identifier=None,public_key=None,key_len=None,mid=None,global_time=None,signiture=None,message_type=None,prefix=None,packet=None):
        self.destination_address=destination_address
        self.source_lan_address = source_lan_address
        self.source_wan_address = source_wan_address
        self.lan_introduction_address=lan_introduction_address
        self.wan_introduction_address=wan_introduction_address
        self.lan_walker_address=lan_walker_address
        self.wan_walker_address=wan_walker_address
        self.identifier = identifier
        self.public_key=public_key
        self.key_len = key_len
        self.mid=mid
        self.global_time = global_time
        self.signiture = signiture
        self.message_type =-message_type
        self.prefix=prefix
        self.packet=packet


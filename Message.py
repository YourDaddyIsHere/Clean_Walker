class introduction_request:
    def __init__(self):
        self.destination_addr=None
        self.sender_lan_addr = None
        self.sender_wan_addr = None
        self.identifier = None
        self.mid=None
        self.global_time = None
        self.signiture = None
        self.message_type =-246
        self.prefix=None
        self.encode_advice_map=None
        self.encode_connection_type_map=None
        self.encode_sync_map=None
        self.packet=None

class introduction_response:
    def __init__(self):
        self.destination_addr=None
        self.sender_lan_addr = None
        self.sender_wan_addr = None
        self.lan_introduced_addr=None
        self.wan_introduced_addr=None
        self.identifier = None
        self.mid=None
        self.global_time = None
        self.signiture = None
        self.message_type =245
        self.prefix=None
        self.encode_advice_map=None
        self.encode_connection_type_map=None
        self.encode_sync_map=None
        self.packet=None


class puncture_request:
    def __init__(self):
        self.lan_walk_addr = None
        self.wan_walker_addr = None
        self.mid=None
        self.global_time = None
        self.signiture = None
        self.message_type =250
        self.prefix=None
        self.packet=None

class puncture:
    def __init__(self):
        self.sender_lan_addr = None
        self.sender_wan_addr = None
        self.message_type = 249

class identity:
    def __init__(self):
        self.public_key=None
        self.key_len = None
        self.global_time=None
        self.message_type=248
        self.signiture = None
        self.packet = None

    class missing_identity:
        def __init__(self):
            self.global_time=None
            self.packet=None
            self.message_type=247

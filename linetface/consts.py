# Ref: https://www.kernel.org/doc/Documentation/networking/operstates.txt

import enum
from enum import Enum, IntFlag


# Ref: https://git.kernel.org/pub/scm/network/iproute2/iproute2.git/tree/ip/ipaddress.c
class OperState(str, Enum):
    UNKNOWN = 'UNKNOWN'
    NOTPRESENT = 'NOTPRESENT'
    DOWN = 'DOWN'
    LOWERLAYERDOWN = 'LOWERLAYERDOWN'
    TESTING = 'TESTING'
    DORMANT = 'DORMANT'
    UP = 'UP'

    def __str__(self):
        return self.value


class LinkMode(Enum):
    DEFAULT = 0
    DORMANT = 1

    def __str__(self):
        return self.name


class LinkFlag(IntFlag):
    # The right-hand side values are copied from Linux kernel's "if.h" source code.
    # Special value "NO-CARRIER" to display when RUNNING flag is not set
    NO_CARRIER = 0
    UP = 1 << 0  # sysfs
    BROADCAST = 1 << 1  # __volatile__
    DEBUG = 1 << 2  # sysfs
    LOOPBACK = 1 << 3  # __volatile__
    POINTOPOINT = 1 << 4  # __volatile__
    NOTRAILERS = 1 << 5  # sysfs
    RUNNING = 1 << 6  # __volatile__
    NOARP = 1 << 7  # sysfs
    PROMISC = 1 << 8  # sysfs
    ALLMULTI = 1 << 9  # sysfs
    MASTER = 1 << 10  # __volatile__
    SLAVE = 1 << 11  # __volatile__
    MULTICAST = 1 << 12  # sysfs
    PORTSEL = 1 << 13  # sysfs
    AUTOMEDIA = 1 << 14  # sysfs
    DYNAMIC = 1 << 15  # sysfs
    LOWER_UP = 1 << 16  # __volatile__
    DORMANT = 1 << 17  # __volatile__
    ECHO = 1 << 18  # __volatile__

    def __str__(self):
        if self.name:
            if self.name == 'NO_CARRIER':
                # Compatible with output of "ip" tool
                return 'NO-CARRIER'
            return self.name
        return super().__str__()

    def __iter__(self):
        '''
        If we have a value being "OR"-combination of the members below, we can split
        it to a list of members. This method is used for building the "flags" result of "ip" tool.

        For example: 4099 -> [NO_CARRIER, BROADCAST, MULTICAST, UP]
        '''
        cls = self.__class__
        members, uncoverd = enum._decompose(cls, self._value_)
        if len(members) == 1:
            yield from members
            return
        # To be compliant with output of "ip" tool, we don't return "RUNNING",
        # and return NO_CARRIER in case RUNNING is not set.
        if cls.RUNNING not in members:
            members.insert(0, cls.NO_CARRIER)
        try:
            members.remove(cls.RUNNING)
        except ValueError:
            pass
        yield from members


# Aggregate from iproute2's ll_types.c and Linux kernel's if_arp.h
# The Linux source code has more type than iproute2.
# The integer value is the real value returned by kernel, the string value
# is the one to display to user.
class LinkType(int, Enum):
    def __new__(cls, value, display):
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.display = display
        return obj

    def __str__(self):
        return self.display

    NETROM = (0, 'netrom')             # from KA9Q: NET/ROM pseudo
    ETHER = (1, 'ether')
    EETHER = (2, 'eether')             # Experimental Ethernet
    AX25 = (3, 'ax25')                 # AX.25 Level = 2
    PRONET = (4, 'pronet')             # PROnet token ring
    CHAOS = (5, 'chaos')               # Chaosnet
    IEEE802 = (6, 'ieee802')           # IEEE = 802.2 Ethernet/TR/TB
    ARCNET = (7, 'arcnet')             # ARCnet
    APPLETLK = (8, 'atalk')            # APPLEtalk
    DLCI = (15, 'dlci')                # Frame Relay DLCI
    ATM = (19, 'atm')
    METRICOM = (23, 'metricom')        # Metricom STRIP (new IANA id)
    IEEE1394 = (24, 'ieee1394')        # IEEE = 1394 IPv4 - RFC = 2734
    # After IEEE1394, there is EUI64 = 27 (EUI-64) in Linux source code,
    # but not in iproute2.
    INFINIBAND = (32, 'infiniband')    # InfiniBand

    # Dummy types for non ARP hardware
    SLIP = (256, 'slip')
    CSLIP = (257, 'cslip')
    SLIP6 = (258, 'slip6')
    CSLIP6 = (259, 'cslip6')
    RSRVD = (260, 'rsrvd')             # Notional KISS type
    ADAPT = (264, 'adapt')
    ROSE = (270, 'rose')
    X25 = (271, 'x25')                 # CCITT X.25
    HWX25 = (272, 'hwx25')             # Boards with X.25 in firmware
    CAN = (280, 'can')                 # Controller Area Network
    PPP = (512, 'ppp')
    # There is an alias of HDLC, CISCO = 513, in Linux source code.
    HDLC = (513, 'hdlc')
    LAPB = (516, 'lapb')
    DDCMP = (517, 'ddcmp')             # Digital's DDCMP protocol
    RAWHDLC = (518, 'rawhdlc')
    # After RAWHDLC, there is RAWIP = 519 in Linux source code
    TUNNEL = (768, 'ipip')             # IPIP tunnel
    TUNNEL6 = (769, 'tunnel6')         # IP6IP6 tunnel
    FRAD = (770, 'frad')               # Frame Relay Access Device
    SKIP = (771, 'skip')               # SKIP vif
    LOOPBACK = (772, 'loopback')
    LOCALTLK = (773, 'ltalk')          # Localtalk device
    FDDI = (774, 'fddi')               # Fiber Distributed Data Interface
    BIF = (775, 'bif')                 # AP1000 BIF
    SIT = (776, 'sit')                 # sit0 device - IPv6-in-IPv4
    IPDDP = (777, 'ip/ddp')            # IP over DDP tunneller
    IPGRE = (778, 'gre')               # GRE over IP
    PIMREG = (779, 'pimreg')           # PIMSM register interface
    HIPPI = (780, 'hippi')             # High Performance Parallel Interface
    ASH = (781, 'ash')                 # Nexus = 64Mbps Ash
    ECONET = (782, 'econet')           # Acorn Econet
    IRDA = (783, 'irda')               # Linux-IrDA
    FCPP = (784, 'fcpp')               # Point to point fibrechannel
    FCAL = (785, 'fcal')               # Fibrechannel arbitrated loop
    FCPL = (786, 'fcpl')               # Fibrechannel public loop
    FCFABRIC = (787, 'fcfb0')          # Fibrechannel fabric
    FCFABRIC_1 = (788, 'fcfb1')
    FCFABRIC_2 = (789, 'fcfb2')
    FCFABRIC_3 = (790, 'fcfb3')
    FCFABRIC_4 = (791, 'fcfb4')
    FCFABRIC_5 = (792, 'fcfb5')
    FCFABRIC_6 = (793, 'fcfb6')
    FCFABRIC_7 = (794, 'fcfb7')
    FCFABRIC_8 = (795, 'fcfb8')
    FCFABRIC_9 = (796, 'fcfb9')
    FCFABRIC_10 = (797, 'fcfb10')
    FCFABRIC_11 = (798, 'fcfb11')
    FCFABRIC_12 = (799, 'fcfb12')
    IEEE802_TR = (800, 'tr')           # Magic type ident for TR
    IEEE80211 = (801, 'ieee802.11')    # IEEE = 802.11
    # IEEE = 802.11 + Prism2 header
    IEEE80211_PRISM = (802, 'ieee802.11/prism')
    # IEEE = 802.11 + radiotap header
    IEEE80211_RADIOTAP = (803, 'ieee802.11/radiotap')
    IEEE802154 = (804, 'ieee802.15.4')
    # IEEE = 802.15.4 network monitor
    IEEE802154_MONITOR = (805, 'ieee802.15.4/monitor')
    PHONET = (820, 'phonet')           # PhoNet media type
    PHONET_PIPE = (821, 'phonet_pipe')  # PhoNet pipe header
    CAIF = (822, 'caif')               # CAIF media type
    IP6GRE = (823, 'gre6')             # GRE over IPv6
    NETLINK = (824, 'netlink')         # Netlink header
    SIXLOWPAN = (825, '6lowpan')       # IPv6 over LoWPAN
    # After 6LOWPAN, there is VSOCKMON = 826 (Vsock monitor header)
    # in Linux source code
    VOID = (65535, 'void')             # Void type, nothing is known
    NONE = (65534, 'none')             # zero header length

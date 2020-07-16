import dataclasses
from dataclasses import dataclass
from ipaddress import IPv4Address, IPv6Address
from typing import List, Tuple, Union, Optional

from netaddr import EUI
from netaddr.strategy.eui48 import mac_unix_expanded
from .consts import LinkFlag, OperState, LinkMode, LinkType


class LinuxMAC(EUI):
    ''' Subclass of :py:class:`netaddr.EUI` to force display to common format used by Linux tools '''
    def __init__(self, addr: Union[str, EUI], version: Optional[int] = None):
        return super().__init__(addr, dialect=mac_unix_expanded)


@dataclass
class IPCommonInfo:
    '''
    Common class

    :meta private:
    '''
    ifindex: str
    ifname: str
    flags: List[LinkFlag]
    mtu: int
    qdisc: str
    operstate: OperState
    group: str
    txqlen: int
    link_type: LinkType
    address: LinuxMAC
    broadcast: LinuxMAC
    promiscuity: int
    min_mtu: int
    max_mtu: int
    num_tx_queues: int
    num_rx_queues: int
    gso_max_size: int
    gso_max_segs: int


@dataclass
class IPLink(IPCommonInfo):
    '''
    The class which represent a data structure member of ``ip -j -d link`` result.
    '''
    linkmode: LinkMode
    inet6_addr_gen_mode: str

    def to_dict(self):
        return dataclasses.asdict(self)


@dataclass
class AddrInfo:
    family: str
    local: Union[IPv4Address, IPv6Address]
    prefixlen: str
    broadcast: Union[IPv4Address, IPv6Address, None]
    scope: str
    dynamic: Optional[bool]
    mngtmpaddr: Optional[bool]
    noprefixroute: Optional[bool]
    label: Optional[str]
    valid_life_time: int
    preferred_life_time: int


@dataclass
class IPAddr(IPCommonInfo):
    '''
    The class which represent a data structure member of ``ip -j -d addr`` result.
    '''
    addr_info: Tuple[AddrInfo, ...]

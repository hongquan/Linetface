import dataclasses
from dataclasses import dataclass
from typing import List, Union, Optional

from netaddr import EUI
from netaddr.strategy.eui48 import mac_unix_expanded
from .consts import LinkFlag, OperState, LinkMode, LinkType


class LinuxMAC(EUI):
    ''' Subclass of netaddr.EUI to force display to common format used by Linux tools '''
    def __init__(self, addr: Union[str, EUI], version: Optional[int] = None):
        return super().__init__(addr, dialect=mac_unix_expanded)


@dataclass
class IPLink:
    '''
    The class which represent a data structure member of "ip -j link" result
    '''
    ifindex: str
    ifname: str
    flags: List[LinkFlag]
    mtu: int
    qdisc: str
    operstate: OperState
    linkmode: LinkMode
    group: str
    txqlen: int
    link_type: LinkType
    address: LinuxMAC
    broadcast: LinuxMAC

    def to_dict(self):
        return dataclasses.asdict(self)

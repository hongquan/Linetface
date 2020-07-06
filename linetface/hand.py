from typing import Tuple

from pyroute2 import IPRoute
from pyroute2.netlink.rtnl.ifinfmsg import ifinfmsg

from .core import IPLink, LinuxMAC
from .consts import LinkFlag, OperState, LinkType, LinkMode


def shinify_link(msg: ifinfmsg) -> IPLink:
    link_flags = LinkFlag(msg['flags'])
    operstate = msg.get_attr('IFLA_OPERSTATE')
    ifla_group = msg.get_attr('IFLA_GROUP')
    # pyroute returns IFLA_GROUP as number, but "ip" tool returns string.
    # I haven't found the mapping from number to string yet.
    dev_group = str(ifla_group) if ifla_group != 0 else 'default'
    return IPLink(
        ifindex=msg['index'],
        ifname=msg.get_attr('IFLA_IFNAME'),
        flags=tuple(link_flags),
        mtu=msg.get_attr('IFLA_MTU'),
        qdisc=msg.get_attr('IFLA_QDISC'),
        operstate=OperState(operstate),
        linkmode=LinkMode(msg.get_attr('IFLA_LINKMODE')),
        group=dev_group,
        txqlen=msg.get_attr('IFLA_TXQLEN'),
        link_type=LinkType(msg['ifi_type']),
        address=LinuxMAC(msg.get_attr('IFLA_ADDRESS')),
        broadcast=LinuxMAC(msg.get_attr('IFLA_BROADCAST'))
    )


def get_links() -> Tuple[IPLink, ...]:
    ip = IPRoute()
    links = []
    for raw in ip.get_links():
        links.append(shinify_link(raw))
    return tuple(links)

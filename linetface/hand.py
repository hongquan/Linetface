import struct
from typing import Tuple, Optional

from pyroute2 import IPRoute
from pyroute2.netlink import nla_slot, nla_base
from pyroute2.netlink.rtnl.ifinfmsg import ifinfmsg, ifinfbase

from .core import IPLink, LinuxMAC
from .consts import LinkFlag, OperState, LinkType, LinkMode, Inet6AddrGenMode


def extract_nla_short_int(msg: ifinfmsg, numeric_type: int) -> Optional[int]:
    for a in msg['attrs']:   # type: nla_slot
        if a.name != 'UNKNOWN':
            continue
        info: nla_base = a.value
        if info['header']['type'] != numeric_type:
            continue
        # We shift forward 4 bytes, because the first 4 bytes are for decoding header
        payload = struct.unpack_from('H', info.data, info.offset + 4)
        return payload[0]


# Before pyroute supports IFLA_MIN_MTU, we have to manually parse Netlink message to get it
def extract_min_mtu(msg: ifinfmsg) -> Optional[int]:
    # Numeric type of IFLA_MIN_MTU is 50
    return extract_nla_short_int(msg, 50)


def extract_max_mtu(msg: ifinfmsg) -> Optional[int]:
    # Numeric type of IFLA_MAX_MTU is 51
    return extract_nla_short_int(msg, 51)


def shinify_link(msg: ifinfmsg) -> IPLink:
    link_flags = LinkFlag(msg['flags'])
    operstate = msg.get_attr('IFLA_OPERSTATE')
    ifla_group = msg.get_attr('IFLA_GROUP')
    # pyroute returns IFLA_GROUP as number, but "ip" tool returns string.
    # I haven't found the mapping from number to string yet.
    dev_group = str(ifla_group) if ifla_group != 0 else 'default'
    # WireGuard NIC doesn't have IFLA_ADDRESS and IFLA_BROADCAST
    ifla_address = msg.get_attr('IFLA_ADDRESS')
    mac_address = LinuxMAC(ifla_address) if ifla_address is not None else None
    ifla_broadcast = msg.get_attr('IFLA_BROADCAST')
    broadcast = LinuxMAC(ifla_broadcast) if ifla_broadcast is not None else None
    # pyroute2 doesn't recognize IFLA_MIN_MTU and IFLA_MAX_MTU yet,
    # it return those data as:
    # ('UNKNOWN', {'header': {'length': 8, 'type': 50}}),
    # ('UNKNOWN', {'header': {'length': 8, 'type': 51}}),
    min_mtu = msg.get_attr('IFLA_MIN_MTU')
    if min_mtu is None:
        min_mtu = extract_min_mtu(msg)
    max_mtu = msg.get_attr('IFLA_MAX_MTU')
    if max_mtu is None:
        max_mtu = extract_max_mtu(msg)
    af_spec: ifinfbase.af_spec_inet = msg.get_attr('IFLA_AF_SPEC')
    inet: ifinfbase.af_spec_inet.inet6 = af_spec.get_attr('AF_INET6')
    # FIXME: iproute2 print hex of unknown IFLA_INET6_ADDR_GEN_MODE value. We should support it.
    inet6_addr_gen_mode = Inet6AddrGenMode(inet.get_attr('IFLA_INET6_ADDR_GEN_MODE'))

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
        address=mac_address,
        broadcast=broadcast,
        promiscuity=msg.get_attr('IFLA_PROMISCUITY'),
        min_mtu=min_mtu,
        max_mtu=max_mtu,
        inet6_addr_gen_mode=inet6_addr_gen_mode,
        num_tx_queues=msg.get_attr('IFLA_NUM_TX_QUEUES'),
        num_rx_queues=msg.get_attr('IFLA_NUM_RX_QUEUES'),
        gso_max_size=msg.get_attr('IFLA_GSO_MAX_SIZE'),
        gso_max_segs=msg.get_attr('IFLA_GSO_MAX_SEGS')
    )


def get_links() -> Tuple[IPLink, ...]:
    ip = IPRoute()
    links = []
    for raw in ip.get_links():
        links.append(shinify_link(raw))
    return tuple(links)

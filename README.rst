=========
Linetface
=========

.. image:: https://madewithlove.now.sh/vn?heart=true&colorA=%23ffcd00&colorB=%23da251d

Retrieve information about network interfaces and routes of Linux machine, as |ip|_ tool does.

*This is still work in progress.*

Linetface has similar purpose as netifaces_ but unlike netifaces_, it does not aim to be portable, and aims to get more detail. It tries to return the same data as JSON output of Linux standard |ip|_ tool, in form of Python data type which is convenient to be consumed by other Python applications.

Motivation
----------

I used to work in an IoT project, where one of the features is to discover Onvif-compliant IP cameras in local network. I used WSDiscovery_ and observed its failure in some uncommon cases: the presence of WireGuard or Docker interfaces. To workaround it, I have to limit WSDiscovery_ to scan only muticast-supporting interfaces. The netifaces_ library doesn't help determine which interfaces allow multicast. I have to use external ``ip -j a`` command and parse its JSON result the get the info I need. However, using ``ip`` command, I stumble upon another issue: If I deploy my app to an Alpine-based Docker container, the above command fails, because in original Alpine Linux, the ``ip`` command of ``iproute2`` is replaced with ``ip`` command of BusyBox_, which does not support generating JSON. A naive solution is to always install iproute2_, but to have a library which returns the same result as |ip|_ would be the most elegant.

That is the reason I create Linetface.


Usage
-----

.. code-block:: python

    >>> from linetface import get_links

    >>> get_links()
    (
        IPLink(
            ifindex=1,
            ifname='lo',
            flags=(<LinkFlag.LOWER_UP: 65536>, <LinkFlag.LOOPBACK: 8>, <LinkFlag.UP: 1>),
            mtu=65536,
            qdisc='noqueue',
            operstate=<OperState.UNKNOWN: 'UNKNOWN'>,
            linkmode=<LinkMode.DEFAULT: 0>,
            group='default',
            txqlen=1000,
            link_type=<LinkType.LOOPBACK: 772>,
            address=EUI('00:00:00:00:00:00'),
            broadcast=EUI('00:00:00:00:00:00')
        ),
        IPLink(
            ifindex=2,
            ifname='enp2s0',
            flags=(<LinkFlag.NO_CARRIER: 0>, <LinkFlag.MULTICAST: 4096>, <LinkFlag.BROADCAST: 2>, <LinkFlag.UP: 1>),
            mtu=1500,
            qdisc='fq_codel',
            operstate=<OperState.DOWN: 'DOWN'>,
            linkmode=<LinkMode.DEFAULT: 0>,
            group='default',
            txqlen=1000,
            link_type=<LinkType.ETHER: 1>,
            address=EUI('54:bf:64:09:eb:3d'),
            broadcast=EUI('ff:ff:ff:ff:ff:ff')
        ),
        IPLink(
            ifindex=3,
            ifname='wlp1s0',
            flags=(<LinkFlag.LOWER_UP: 65536>, <LinkFlag.MULTICAST: 4096>, <LinkFlag.BROADCAST: 2>, <LinkFlag.UP: 1>),
            mtu=1500,
            qdisc='noqueue',
            operstate=<OperState.UP: 'UP'>,
            linkmode=<LinkMode.DORMANT: 1>,
            group='default',
            txqlen=1000,
            link_type=<LinkType.ETHER: 1>,
            address=EUI('0c:54:15:fa:0a:23'),
            broadcast=EUI('ff:ff:ff:ff:ff:ff')
        )
    )



.. |ip| replace:: ``ip``
.. _ip: https://wiki.linuxfoundation.org/networking/iproute2
.. _iproute2: https://wiki.linuxfoundation.org/networking/iproute2
.. _netifaces: https://github.com/al45tair/netifaces
.. _WSDiscovery: https://github.com/andreikop/python-ws-discovery
.. _BusyBox: https://www.busybox.net/

import json
import subprocess
from linetface.hand import get_links


def test_get_links():
    ip_stdout = subprocess.run(('ip', '-j', 'a'), check=True, stdout=subprocess.PIPE).stdout
    standard = json.loads(ip_stdout)
    first_stdlink = next(b for b in standard if b['ifindex'] == 1)
    first_link = get_links()[0]
    assert first_link.ifname == first_stdlink['ifname']
    assert str(first_link.operstate) == first_stdlink['operstate']
    assert str(first_link.address) == first_stdlink['address']

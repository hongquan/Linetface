from pathlib import Path

from single_version import get_version

from .hand import get_links     # NOQA: F401


__version__ = get_version('linetface', Path(__file__).parent.parent)

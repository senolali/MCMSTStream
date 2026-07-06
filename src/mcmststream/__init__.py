"""MCMSTStream: MST over KD-tree-based micro-clusters for streaming data.

Reference
---------
Erdinç, B., Kaya, M., & Şenol, A. (2024). MCMSTStream: applying minimum
spanning tree to KD-tree-based micro-clusters to define arbitrary-shaped
clusters in streaming data. Neural Computing and Applications, 36(13),
7025-7042. https://doi.org/10.1007/s00521-024-09443-1
"""

from .core import MCMSTStream
from .utils import load_exclastar

__all__ = ["MCMSTStream", "load_exclastar"]
__version__ = "1.2.3"

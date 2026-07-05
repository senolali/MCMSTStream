# MCMSTStream

[![PyPI version](https://img.shields.io/pypi/v/mcmststream.svg)](https://pypi.org/project/mcmststream/)
[![Python](https://img.shields.io/pypi/pyversions/mcmststream.svg)](https://pypi.org/project/mcmststream/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paper](https://img.shields.io/badge/DOI-10.1007%2Fs00521--024--09443--1-blue)](https://doi.org/10.1007/s00521-024-09443-1)

**MCMSTStream** is a density-based stream clustering algorithm that applies a
**Minimum Spanning Tree (MST)** over **KD-tree-based micro-clusters** to define
**arbitrary-shaped clusters** in streaming data.

Published in *Neural Computing and Applications* (2024) 36:7025–7042.

## Key features

- Online (sliding-window) stream clustering
- Detects **arbitrary-shaped** (non-spherical) clusters
- Robust to **outliers and noisy data**
- Handles **high-dimensional** streams via KD-tree range search
- Scikit-learn-style API: `fit`, `partial_fit`, `fit_predict`, `predict`, `get_params`, `set_params`

## Installation

```bash
pip install mcmststream
```

For the built-in visualization support:

```bash
pip install "mcmststream[viz]"
```

## Quick start

```python
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import adjusted_rand_score
from mcmststream import MCMSTStream, load_exclastar

# Load the bundled ExclaStar benchmark dataset
X, y_true = load_exclastar()
X = MinMaxScaler().fit_transform(X)

clusterer = MCMSTStream(
    W=270,        # sliding window width
    N=2,          # min points to define a micro-cluster
    r=0.14,       # micro-cluster radius
    n_micro=2,    # min micro-clusters to define a macro-cluster
    random_state=42,
    keep_history=True,
)

# Process the stream point by point
for point in X:
    clusterer.partial_fit(point)

print("ARI = %.4f" % adjusted_rand_score(y_true, clusterer.history_labels_))
```

Optional visualization of the current window:

```python
clusterer.visualize(title="MCMSTStream on ExclaStar")
```

## Parameters

| Parameter | Description | Paper symbol |
|---|---|---|
| `W` | Sliding window width | *W* |
| `N` | Minimum number of points within radius `r` to define a micro-cluster | *N* |
| `r` | Micro-cluster radius; micro-clusters within `2r` are linked by the MST | *r* |
| `n_micro` | Minimum number of micro-clusters to form a macro-cluster | *n_micro* |
| `dense_mc_promotion` | If `True`, a component whose total point count is ≥ `n_micro * N` also becomes a macro-cluster even with fewer than `n_micro` micro-clusters (extension beyond the paper; default `False`) | — |

## How it works

1. **Micro-clusters** are formed with a KD-tree range search: at least `N`
   points within radius `r`.
2. **Macro-clusters** are built by running Prim's MST over micro-cluster
   centers, connecting those within `2r`.
3. As the stream evolves, micro/macro-clusters are updated, merged, or
   deleted, adapting to concept drift.

## Citation

If you use this package in your research, please cite:

```bibtex
@article{erdinc2024mcmststream,
  title   = {MCMSTStream: applying minimum spanning tree to KD-tree-based
             micro-clusters to define arbitrary-shaped clusters in streaming data},
  author  = {Erdin{\c{c}}, Berfin and Kaya, Mahmut and {\c{S}}enol, Ali},
  journal = {Neural Computing and Applications},
  volume  = {36},
  number  = {13},
  pages   = {7025--7042},
  year    = {2024},
  doi     = {10.1007/s00521-024-09443-1}
}
```

## Related projects

- [MCMSTClustering](https://pypi.org/project/mcmst-clust/) — the batch (static data) counterpart
- [KD-AR Stream](https://github.com/senolali/kd-ar-stream) — KD-tree and adaptive radius stream clustering

## License

MIT — see [LICENSE](LICENSE).

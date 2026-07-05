"""Demo: MCMSTStream on the ExclaStar dataset.

Run directly:  python examples/exclastar_demo.py
This code is intentionally NOT at module level inside the package, so that
`import mcmststream` has no side effects.
"""

import numpy as np
from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.preprocessing import MinMaxScaler

from mcmststream import MCMSTStream, load_exclastar


def main(visualize_every=0):
    X, y_true = load_exclastar()
    X_scaled = MinMaxScaler().fit_transform(X)

    clusterer = MCMSTStream(
        W=270,
        n_micro=2,
        N=2,
        r=0.14,
        random_state=42,
        keep_history=True,
    )

    for i, point in enumerate(X_scaled):
        clusterer.partial_fit(point)
        if visualize_every and i > 0 and i % visualize_every == 0:
            print(f"Step {i}: "
                  f"{len(clusterer.micro_clusters)} micro-clusters, "
                  f"{clusterer.n_clusters_} macro-clusters")
            clusterer.visualize(title=f"Step {i}")

    ari = adjusted_rand_score(y_true, clusterer.history_labels_)
    print("ARI = %.4f" % ari)
    return ari


if __name__ == "__main__":
    main(visualize_every=0)  # set e.g. 100 to watch the stream evolve

"""Basic sanity tests for mcmststream."""

import io
import contextlib
import subprocess
import sys

import numpy as np


def test_import_has_no_side_effects():
    """Importing the package must not print anything or open figures."""
    code = (
        "import io, contextlib, sys;"
        "buf = io.StringIO();\n"
        "with contextlib.redirect_stdout(buf):\n"
        "    import mcmststream\n"
        "assert buf.getvalue() == '', 'import produced output: %r' % buf.getvalue()\n"
        "print('clean')"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "clean"


def test_exclastar_clustering_quality():
    from sklearn.metrics.cluster import adjusted_rand_score
    from sklearn.preprocessing import MinMaxScaler
    from mcmststream import MCMSTStream, load_exclastar

    X, y_true = load_exclastar()
    X = MinMaxScaler().fit_transform(X)

    clusterer = MCMSTStream(W=270, n_micro=2, N=2, r=0.14,
                            random_state=42, keep_history=True)
    for p in X:
        clusterer.partial_fit(p)

    ari = adjusted_rand_score(y_true, clusterer.history_labels_)
    assert ari > 0.85, f"ARI too low: {ari:.4f}"


def test_sklearn_style_api():
    from mcmststream import MCMSTStream

    c = MCMSTStream(W=100, r=0.2)
    params = c.get_params()
    assert params["W"] == 100 and params["r"] == 0.2
    c.set_params(r=0.3)
    assert c.r == 0.3

    rng = np.random.default_rng(0)
    X = rng.random((50, 2))
    labels = c.fit_predict(X)
    assert len(labels) > 0


def test_dense_mc_promotion_flag():
    """dense_mc_promotion=True promotes a lone dense micro-cluster; False (default) does not."""
    from mcmststream import MCMSTStream

    rng = np.random.default_rng(0)
    dense = rng.normal([0.5, 0.5], 0.02, size=(80, 2))

    # Default: paper behavior, no macro-cluster from a single MC
    c_off = MCMSTStream(W=200, n_micro=5, N=10, r=0.1, random_state=0)
    for p in dense:
        c_off.partial_fit(p)
    assert c_off.n_clusters_ == 0

    # Flag on: >= n_micro * N = 50 points -> macro-cluster
    c_on = MCMSTStream(W=200, n_micro=5, N=10, r=0.1, random_state=0,
                       dense_mc_promotion=True)
    for p in dense:
        c_on.partial_fit(p)
    assert c_on.n_clusters_ >= 1

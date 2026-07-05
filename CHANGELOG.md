# Changelog

## 1.1.0 (2026-07-05)

### Fixed
- **Critical:** removed module-level demo code from `core.py`. Previously,
  `import mcmststream` executed a demo (printing step logs, opening matplotlib
  figures) and required the unrelated `kd_ar_stream` package, causing
  `ImportError` when it was not installed. Importing the package now has no
  side effects.
- Removed global `warnings.filterwarnings("ignore")`, which silenced all
  warnings in the user's process.
- Removed a duplicated `return self` in `set_params`.

### Changed
- `matplotlib` is now an optional dependency (`pip install mcmststream[viz]`),
  imported lazily inside `visualize()`.
- Migrated to `src/` layout with a modern `pyproject.toml` (PEP 621).
- Corrected project metadata (homepage previously pointed to kd-ar-stream).
- Added tests, examples, CI (tests + Trusted Publishing release workflow).

## 1.0.4
- Previous release.

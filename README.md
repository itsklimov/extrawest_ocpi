<a href="https://www.extrawest.com/"><img src="https://drive.google.com/uc?export=view&id=1kXfNj5WfW2oSMzQR82xYBI6Bw_W8-LpK" width="20%"></a>
# Extrawest OCPI

[![Python 3.13+](https://img.shields.io/badge/python-3.13%20%7C%203.14-blue.svg)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/badge/pydantic-v2-E92063.svg)](https://docs.pydantic.dev/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![commit-check](https://img.shields.io/badge/commit--check-enabled-brightgreen?logo=Git&logoColor=white)](https://github.com/commit-check/commit-check)

---

Python implementation of Open Charge Point Interface (OCPI) protocol based on FastAPI.

**🚀 Now supports Python 3.13 & 3.14 with Pydantic v2!**

Supported OCPI versions: 2.2.1, 2.1.1

OCPI Documentation: [2.2.1](https://github.com/ocpi/ocpi/tree/release-2.2.1-bugfixes), [2.1.1](https://github.com/ocpi/ocpi/tree/release-2.1.1-bugfixes)

---


## Requirements

---

**Python >= 3.13** (Python 3.13 and 3.14 fully supported)

**Dependencies:**
- Pydantic v2.10+
- FastAPI v0.115+
- httpx v0.27+


## Installation

---

### From PyPI (Original - Python 3.10 only)
```bash
pip install extrawest-ocpi
```

### From This Fork (Python 3.13/3.14 Support)
```bash
pip install git+https://github.com/itsklimov/extrawest_ocpi.git
```

Or with uv (recommended):
```bash
uv add git+https://github.com/itsklimov/extrawest_ocpi.git
```

**See [MIGRATION.md](MIGRATION.md) for upgrade details.**

Documentation for original version: [extrawest-ocpi.readthedocs.io](https://extrawest-ocpi.readthedocs.io/en/latest/)


## Roadmap

---

- Issues fixing


## Related

---

The project was created through inspiration and adaptation of this project  [PY_OCPI](https://github.com/TECHS-Technological-Solutions/ocpi).


## License

---

This project is licensed under the terms of the [MIT](https://github.com/extrawest/extrawest_ocpi/blob/main/LICENSE) license.


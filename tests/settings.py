"""
Contains data for tests.

.. data:: DATA_DIR
"""

import pathlib


__all__ = [
    'DATA_DIR'
]


# ``datadir`` pytest plugin provides fixture only with ``function`` scope
# so I use set way to data dir manually
DATA_DIR = pathlib.Path(__file__).parent / 'data'

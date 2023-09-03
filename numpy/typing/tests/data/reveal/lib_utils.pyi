from io import StringIO
from typing import Any

import numpy as np

AR: np.ndarray[Any, np.dtype[np.float64]]
AR_DICT: dict[str, np.ndarray[Any, np.dtype[np.float64]]]
FILE: StringIO

def func(a: int) -> bool: ...

reveal_type(np.byte_bounds(AR))  # E: tuple[builtins.int, builtins.int]
reveal_type(np.byte_bounds(np.float64()))  # E: tuple[builtins.int, builtins.int]

reveal_type(np.info(1, output=FILE))  # E: None

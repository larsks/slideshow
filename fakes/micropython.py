try:
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False  # pyright:ignore[reportConstantRedefinition]

if TYPE_CHECKING:
    from typing import TypeVar

T = TypeVar("T")


def const(arg: T) -> T:
    """
    Returns its input argument unchanged, with type hints.
    """
    return arg

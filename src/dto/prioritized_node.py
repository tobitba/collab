from dataclasses import field, dataclass
from typing import Any


@dataclass(order = True)
class PrioritizedNode:
    priority: int
    item: Any = field(compare = False)
    action: str = field(compare = False)
from dataclasses import dataclass, field
from random import randint
from typing import List, Literal, get_args

TargetLengthOption = Literal[3, 4, 5]


@dataclass
class MOO:
    target_length: TargetLengthOption = 3
    target: List[int] = field(init=False)

    def __post_init__(self) -> None:
        if self.target_length not in get_args(TargetLengthOption):
            raise ValueError(f"'target_length' should be in {get_args(TargetLengthOption)}.")
        self.target = [randint(0, 9) for _ in range(self.target_length)]

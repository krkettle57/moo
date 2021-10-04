from __future__ import annotations

from dataclasses import dataclass, field
from random import randint
from typing import List, Literal, get_args

TargetLengthOption = Literal[3, 4, 5]


@dataclass
class CallResultSet:
    called: List[int]
    num_eat: int
    num_bite: int


@dataclass
class MOO:
    target_length: TargetLengthOption = 3
    called_results: List[CallResultSet] = field(default_factory=list)
    target: List[int] = field(init=False)

    def __post_init__(self) -> None:
        if self.target_length not in get_args(TargetLengthOption):
            raise ValueError(f"'target_length' should be in {get_args(TargetLengthOption)}.")
        self.target = [randint(0, 9) for _ in range(self.target_length)]

    def call(self, called: List[int]) -> CallResultSet:
        if len(called) != self.target_length:
            raise ValueError(f"Length of 'called' must be {self.target_length}")

        num_eat = sum([td == cd for td, cd in zip(self.target, called)])
        num_bite = sum(set(self.target) & set(called)) - num_eat

        result = CallResultSet(called, num_eat, num_bite)
        self.called_results.append(result)

        return result

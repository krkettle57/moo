from __future__ import annotations

from dataclasses import dataclass, field
from random import randint
from typing import List, Literal, Tuple, get_args

TargetLengthOption = Literal[3, 4, 5]


@dataclass
class CallResultSet:
    called: Called
    num_eat: int
    num_bite: int


@dataclass
class Target:
    target: str

    @classmethod
    def generate(self, length: TargetLengthOption) -> Target:
        if length not in get_args(TargetLengthOption):
            raise ValueError(f"'length' should be in {get_args(TargetLengthOption)}.")

        target = "".join([str(randint(0, 9)) for _ in range(length)])
        return Target(target)

    @property
    def length(self) -> int:
        return len(self.as_list())

    def as_list(self) -> List[str]:
        return list(self.target)


@dataclass
class Called:
    called: str
    target: Target

    def __post_init__(self) -> None:
        if len(self.as_list()) != self.target.length:
            raise ValueError(f"Length of 'called' must be {self.target.length}")

        if not self.called.isdigit():
            raise ValueError("'called' must contain only number")

    def as_list(self) -> List[str]:
        return list(self.called)

    def get_eat_bite_num(self) -> Tuple[int, int]:
        num_eat = sum([td == cd for td, cd in zip(self.target.as_list(), self.called)])
        num_bite = len(set(self.target.as_list()) & set(self.called)) - num_eat
        return num_eat, num_bite

    def get_result_set(self) -> CallResultSet:
        num_eat, num_bite = self.get_eat_bite_num()
        return CallResultSet(self, num_eat, num_bite)


@dataclass
class MOO:
    target: Target
    called_results: List[CallResultSet] = field(default_factory=list)
    on_play: bool = field(default=True)

    def call(self, digits: str) -> CallResultSet:
        called = Called(digits, self.target)
        result = called.get_result_set()
        self.called_results.append(result)

        return result

    def finish(self) -> None:
        self.on_play = False

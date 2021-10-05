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
        return len(self.target)

    def as_list(self) -> List[str]:
        return list(self.target)


@dataclass
class Called:
    called: str
    target: Target

    def __post_init__(self) -> None:
        if len(self.called) != self.target.length:
            raise ValueError(f"Length of 'called' must be {self.target.length}")

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
    target_length: TargetLengthOption
    target: List[int] = field(default_factory=list)
    called_results: List[CallResultSet] = field(default_factory=list)
    onPlay: bool = field(default=True)

    def __post_init__(self) -> None:
        if self.target_length not in get_args(TargetLengthOption):
            raise ValueError(f"'target_length' should be in {get_args(TargetLengthOption)}.")

        if len(self.target) == 0:
            self.target = [randint(0, 9) for _ in range(self.target_length)]

    def call(self, called: List[int]) -> CallResultSet:
        if len(called) != self.target_length:
            raise ValueError(f"Length of 'called' must be {self.target_length}")

        num_eat = sum([td == cd for td, cd in zip(self.target, called)])
        num_bite = len(set(self.target) & set(called)) - num_eat

        result = CallResultSet("".join([str(i) for i in called]), num_eat, num_bite)
        self.called_results.append(result)

        return result

    def finish(self) -> None:
        self.onPlay = False

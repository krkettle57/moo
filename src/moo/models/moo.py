from __future__ import annotations

from dataclasses import dataclass, field
from random import randint
from typing import List, Literal, Tuple, get_args

from dataclasses_json import dataclass_json

from moo.exceptions import InvalidLengthInputError, InvalidValueInputError

TargetLengthOption = Literal[3, 4, 5]


@dataclass_json
@dataclass
class CallResultSet:
    called: Called
    num_eat: int
    num_bite: int


@dataclass_json
@dataclass
class Target:
    target: str

    @classmethod
    def generate(self, length: TargetLengthOption) -> Target:
        if length not in get_args(TargetLengthOption):
            raise InvalidLengthInputError(f"'length' should be in {get_args(TargetLengthOption)}.")

        target = "".join([str(randint(0, 9)) for _ in range(length)])
        return Target(target)

    @property
    def length(self) -> int:
        return len(self.as_list())

    def as_list(self) -> List[str]:
        return list(self.target)


@dataclass_json
@dataclass
class Called:
    called: str
    target: Target

    def __post_init__(self) -> None:
        if len(self.as_list()) != self.target.length:
            raise InvalidLengthInputError(f"Length of 'called' must be {self.target.length}")

        if not self.called.isdigit():
            raise InvalidValueInputError("'called' must contain only number")

    def as_list(self) -> List[str]:
        return list(self.called)

    def get_eat_bite_num(self) -> Tuple[int, int]:
        num_eat = sum([td == cd for td, cd in zip(self.target.as_list(), self.called)])
        num_bite = len(set(self.target.as_list()) & set(self.called)) - num_eat
        return num_eat, num_bite

    def get_result_set(self) -> CallResultSet:
        num_eat, num_bite = self.get_eat_bite_num()
        return CallResultSet(self, num_eat, num_bite)


@dataclass_json
@dataclass
class MOO:
    target: Target
    called_results: List[CallResultSet] = field(default_factory=list)
    on_play: bool = field(default=True)

    def call(self, digits: str) -> CallResultSet:
        called = Called(digits, self.target)
        result = called.get_result_set()
        self.called_results.append(result)

        if result.num_eat == self.target.length:
            self.finish()

        return result

    def finish(self) -> None:
        self.on_play = False

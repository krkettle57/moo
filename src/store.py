import json
import os
from dataclasses import asdict, dataclass
from typing import Protocol

from model import MOO, Called, CallResultSet, Target


class MOOFileStore(Protocol):
    def load(self) -> MOO:
        pass

    def save(self, moo: MOO) -> None:
        pass

    def exists(self) -> bool:
        pass


@dataclass
class MOOJSONStore(MOOFileStore):
    filename: str = ".moo.json"
    ensure_ascii: bool = False
    indent: int = 2

    def load(self) -> MOO:
        with open(self.filename) as f:
            data = json.load(f)
        target = Target(**data["target"])
        called_results = []
        for result in data["called_results"]:
            called_data = result["called"]
            called = Called(called=called_data["called"], target=Target(**called_data["target"]))
            called_result = CallResultSet(called, result["num_eat"], result["num_bite"])
            called_results.append(called_result)
        on_play = data["on_play"]
        return MOO(target=target, called_results=called_results, on_play=on_play)

    def save(self, moo: MOO) -> None:
        with open(self.filename, "w") as f:
            json.dump(asdict(moo), f, ensure_ascii=self.ensure_ascii, indent=self.indent)

    def exists(self) -> bool:
        return os.path.exists(self.filename)

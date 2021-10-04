import json
import os
from dataclasses import asdict, dataclass
from typing import Protocol

from model import MOO


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
            return json.load(f)

    def save(self, moo: MOO) -> None:
        with open(self.filename, "w") as f:
            json.dump(asdict(moo), f, ensure_ascii=self.ensure_ascii, indent=self.indent)

    def exists(self) -> bool:
        return os.path.exists(self.filename)

import os
from dataclasses import dataclass
from typing import Protocol

from models.moo import MOO


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
            moo = MOO.from_json(f.read())
        return moo

    def save(self, moo: MOO) -> None:
        with open(self.filename, "w") as f:
            f.write(moo.to_json(indent=self.indent, ensure_ascii=self.ensure_ascii))

    def exists(self) -> bool:
        return os.path.exists(self.filename)

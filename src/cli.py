from dataclasses import dataclass
from enum import Enum

from model import MOO, TargetLengthOption
from store import MOOFileStore, MOOJSONStore


class CLIMessage(Enum):
    MOO_ALREADY_STARTED = "現在進行中のMOOが存在します。\n新しくMOOを開始しますか？[y/n]"
    CANCEL_NEW_MOO = "新しいMOOの開始を中止しました\n"


@dataclass
class MOOCLIHandler:
    store: MOOFileStore = MOOJSONStore()

    def start(self, called: str, target_length: TargetLengthOption = 3) -> str:
        if self.store.exists():
            yn = CLIMessage.MOO_ALREADY_STARTED.value
            if yn.lower().strip() != "y":
                return CLIMessage.CANCEL_NEW_MOO.value

        moo = MOO(target_length)
        self.store.save(moo)
        return self.turn(called)

    def turn(self, called: str) -> str:
        # 管理ファイルからMOOをload
        # callを実行し、終了判定
        # 結果を返す
        return "[DEV]: turn"

    def history(self) -> str:
        # 管理ファイルの有無を確認する
        # ターンの履歴を返す
        return "[DEV]: history"

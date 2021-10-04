from dataclasses import dataclass
from enum import Enum

from model import MOO, TargetLengthOption
from store import MOOFileStore, MOOJSONStore


class CLIMessage(Enum):
    MOO_ALREADY_STARTED = "現在進行中のMOOが存在します。\n新しくMOOを開始しますか？[y/n]: "
    CANCEL_NEW_MOO = "新しいMOOの開始を中止しました。"
    START_MOO = "MOOを開始します！"
    GIVEUP_MOO = "MOOを終了します。ターゲットは{target}でした。"


@dataclass
class MOOCLIHandler:
    store: MOOFileStore = MOOJSONStore()

    def start(self, target_length: TargetLengthOption = 3) -> str:
        if self.store.exists() and self.store.load().onPlay:
            yn = input(CLIMessage.MOO_ALREADY_STARTED.value)
            if yn.lower().strip() != "y":
                return CLIMessage.CANCEL_NEW_MOO.value

        moo = MOO(target_length)
        self.store.save(moo)
        return CLIMessage.START_MOO.value

    def giveup(self) -> str:
        moo = self.store.load()
        moo.finish()
        self.store.save(moo)
        target = "".join([str(i) for i in moo.target])
        return CLIMessage.GIVEUP_MOO.value.format(target=target)

    def turn(self, called: str) -> str:
        # 管理ファイルからMOOをload
        # callを実行し、終了判定
        # 結果を返す
        return "[DEV]: turn"

    def history(self) -> str:
        # 管理ファイルの有無を確認する
        # ターンの履歴を返す
        return "[DEV]: history"

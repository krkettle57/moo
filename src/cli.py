from dataclasses import dataclass
from enum import Enum
from typing import Union

from model import MOO, TargetLengthOption
from store import MOOFileStore, MOOJSONStore


class CLIMessage(Enum):
    MOO_ALREADY_STARTED = "現在進行中のMOOが存在します。\n新しくMOOを開始しますか？[y/n]: "
    CANCEL_NEW_MOO = "新しいMOOの開始を中止しました。"
    START_MOO = "MOOを開始します！"
    GIVEUP_MOO = "MOOを終了します。ターゲットは{target}でした。"
    INVALID_DIGIT_CALL = "数字のみを用いてコールして下さい。"
    INVALID_LENGTH_CALL = "{target_length}桁でコールして下さい。"
    CLEAR_MOO = "クリア！ターゲット: {target}, コール数: {num_call}"
    RESULT_CALL = "コール: {called}, {num_eat}-EAT, {num_bite}-BITE"


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

    def turn(self, called: Union[str, int]) -> str:
        moo = self.store.load()

        # validate called
        called = str(called)
        if called.isdigit() is None:
            return CLIMessage.INVALID_DIGIT_CALL.value

        if len(called) != moo.target_length:
            return CLIMessage.INVALID_LENGTH_CALL.value

        # call
        result = moo.call([int(s) for s in list(called)])
        self.store.save(moo)

        # validate result
        if result.num_eat == moo.target_length:
            moo.finish()
            return CLIMessage.CLEAR_MOO.value.format(target=moo.target, num_call=len(moo.called_results))

        return CLIMessage.RESULT_CALL.value.format(called=called, num_eat=result.num_eat, num_bite=result.num_bite)

    def history(self) -> str:
        # 管理ファイルの有無を確認する
        # ターンの履歴を返す
        return "[DEV]: history"

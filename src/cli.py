from dataclasses import dataclass
from typing import Union

from model import MOO, Target, TargetLengthOption
from store import MOOFileStore, MOOJSONStore

NO_EXIST_DOING_MOO = "進行中のMOOが存在しません。 startコマンドで開始して下さい。"


@dataclass
class MOOCLIHandler:
    store: MOOFileStore = MOOJSONStore()

    def start(self, target_length: TargetLengthOption = 3) -> str:
        if self._is_on_play():
            yn = input("進行中のMOOが存在します。\n新しくMOOを開始しますか？[y/n]: ")
            if yn.lower().strip() != "y":
                return "新しいMOOの開始を中止しました。"

        target = Target.generate(target_length)
        moo = MOO(target)
        self.store.save(moo)
        return "MOOを開始します！"

    def giveup(self) -> str:
        if not self._is_on_play():
            return NO_EXIST_DOING_MOO

        moo = self.store.load()
        moo.finish()
        self.store.save(moo)
        return f"MOOを終了します。ターゲットは{moo.target.target}でした。"

    def turn(self, called: Union[str, int]) -> str:
        if not self._is_on_play():
            return NO_EXIST_DOING_MOO

        moo = self.store.load()
        result = moo.call(str(called))
        self.store.save(moo)

        # validate result
        if result.num_eat == moo.target.length:
            moo.finish()
            return f"クリア！ターゲット: {moo.target.target}, コール数: {len(moo.called_results)}"

        return f"コール: {result.called.called}, {result.num_eat}-EAT, {result.num_bite}-BITE"

    def history(self) -> str:
        # 管理ファイルの有無を確認する
        # ターンの履歴を返す
        return "[DEV]: history"

    def _is_on_play(self) -> bool:
        return self.store.exists() and self.store.load().on_play

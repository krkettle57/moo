from dataclasses import dataclass, field
from typing import List, Union

from model import MOO, CallResultSet, Target, TargetLengthOption
from store import MOOFileStore, MOOJSONStore


class MOOCLIViewer:
    def start_verify(self, yes: str = "y", no: str = "n") -> str:
        return f"進行中のMOOが存在します。\n新しくMOOを開始しますか？[{yes}/{no}]: "

    def start_done(self) -> str:
        return "MOOを開始しました"

    def start_cancel(self) -> str:
        return "新しいMOOの開始を中止しました。"

    def giveup(self, target: Target) -> str:
        return f"MOOを終了します。ターゲットは{target.target}でした。"

    def clear(self, moo: MOO) -> str:
        return f"クリア！ターゲット: {moo.target.target}, コール数: {len(moo.called_results)}"

    def called_result(self, result: CallResultSet) -> str:
        return f"コール: {result.called.called}, {result.num_eat}-EAT, {result.num_bite}-BITE"

    def history(self, called_results: List[CallResultSet]) -> str:
        hist = [self.called_result(result) for result in called_results]
        return "\n".join(["[Called History]"] + hist)

    def no_moo_on_play(self) -> str:
        return "進行中のMOOが存在しません。 startコマンドで開始して下さい。"

    def no_moo_started(self) -> str:
        return "MOOのプレイ記録が存在しません。startコマンドで開始して下さい。"


@dataclass
class MOOCLIHandler:
    viewer: MOOCLIViewer = field(default=MOOCLIViewer(), init=False)
    store: MOOFileStore = MOOJSONStore()

    def start(self, target_length: TargetLengthOption = 3) -> str:
        if self._is_on_play():
            yn = input(self.viewer.start_verify())
            if yn.lower().strip() != "y":
                return self.viewer.start_done()

        target = Target.generate(target_length)
        moo = MOO(target)
        self.store.save(moo)
        return self.viewer.start_done()

    def giveup(self) -> str:
        if not self._is_on_play():
            return self.viewer.no_moo_on_play()

        moo = self.store.load()
        moo.finish()
        self.store.save(moo)
        return self.viewer.giveup(moo.target)

    def turn(self, called: Union[str, int]) -> str:
        if not self._is_on_play():
            return self.viewer.no_moo_on_play()

        moo = self.store.load()
        result = moo.call(str(called))
        self.store.save(moo)

        if result.num_eat == moo.target.length:
            return self.viewer.clear(moo)

        return self.viewer.called_result(result)

    def history(self) -> str:
        if not self._is_started():
            return self.viewer.no_moo_started()

        moo = self.store.load()
        return self.viewer.history(moo.called_results)

    def _is_started(self) -> bool:
        return self.store.exists()

    def _is_on_play(self) -> bool:
        return self._is_started() and self.store.load().on_play

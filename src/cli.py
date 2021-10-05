from dataclasses import dataclass, field
from typing import Union

from model import MOO, Target, TargetLengthOption
from store import MOOFileStore, MOOJSONStore
from viewer import MOOCLIViewer


@dataclass
class MOOCLIHandler:
    """CLI版 MOO"""

    __viewer: MOOCLIViewer = field(default=MOOCLIViewer(), init=False)
    __store: MOOFileStore = MOOJSONStore()

    def start(self, target_length: TargetLengthOption = 3) -> str:
        """MOOを開始します

        Parameters
        ----------
        target_length : TargetLengthOption, optional
            ターゲットの桁数

        Returns
        -------
        str
            出力メッセージ
        """
        if self._is_on_play():
            yn = input(self.__viewer.start_verify())
            if yn.lower().strip() != "y":
                return self.__viewer.start_done()

        target = Target.generate(target_length)
        moo = MOO(target)
        self.__store.save(moo)
        return self.__viewer.start_done()

    def call(self, called: Union[str, int]) -> str:
        """ターゲットと思われる数字列をコールします

        Parameters
        ----------
        called : Union[str, int]
            コールする数字列

        Returns
        -------
        str
            出力メッセージ
        """
        if not self._is_on_play():
            return self.__viewer.no_moo_on_play()

        moo = self.__store.load()
        result = moo.call(str(called))
        self.__store.save(moo)

        if result.num_eat == moo.target.length:
            return self.__viewer.clear(moo)

        return self.__viewer.called_result(result)

    def giveup(self) -> str:
        """MOOを終了し、ターゲットを表示します

        Returns
        -------
        str
            出力メッセージ
        """
        if not self._is_on_play():
            return self.__viewer.no_moo_on_play()

        moo = self.__store.load()
        moo.finish()
        self.__store.save(moo)
        return self.__viewer.giveup(moo.target)

    def history(self) -> str:
        """コール結果一覧を表示します

        Returns
        -------
        str
            出力メッセージ
        """
        if not self._is_started():
            return self.__viewer.no_moo_started()

        moo = self.__store.load()
        return self.__viewer.history(moo.called_results)

    def _is_started(self) -> bool:
        return self.__store.exists()

    def _is_on_play(self) -> bool:
        return self._is_started() and self.__store.load().on_play

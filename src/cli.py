from dataclasses import dataclass, field
from typing import Union

from model import MOO, Target, TargetLengthOption
from store import MOOFileStore, MOOJSONStore
from viewer import MOOCLIViewer


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

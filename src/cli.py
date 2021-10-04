from dataclasses import dataclass

from store import MOOFileStore, MOOJSONStore


@dataclass
class MOOCLIHandler:
    store: MOOFileStore = MOOJSONStore()

    def start(self) -> None:
        # 管理ファイルの有無を確認する
        # 管理ファイルを作成する
        # 初回ターンを実行する
        pass

    def turn(self, called: str) -> str:
        # 管理ファイルからMOOをload
        # callを実行し、終了判定
        # 結果を返す
        pass

    def history(self) -> str:
        # 管理ファイルの有無を確認する
        # ターンの履歴を返す
        pass

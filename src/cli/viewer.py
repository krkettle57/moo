from typing import List, get_args

from models.moo import MOO, CallResultSet, Target, TargetLengthOption


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
        return f"Call: {result.called.called}, {result.num_eat}-EAT, {result.num_bite}-BITE"

    def history(self, called_results: List[CallResultSet]) -> str:
        hist = [self.called_result(result) for result in called_results]
        return "\n".join(["[Called History]"] + hist)

    def no_moo_on_play(self) -> str:
        return "進行中のMOOが存在しません。 startコマンドで開始して下さい。"

    def no_moo_started(self) -> str:
        return "MOOのプレイ記録が存在しません。startコマンドで開始して下さい。"

    def invalid_target_length(self) -> str:
        options = ", ".join([str(i) for i in get_args(TargetLengthOption)])
        return f"ターゲットの桁数は{options}のいずれかで入力して下さい。"

    def invalid_call_length(self, target_length: int) -> str:
        return f"コールする値は{target_length}桁で入力して下さい。"

    def invalid_call_value(self) -> str:
        return "コールする値の各桁は0~9のいずれかで入力して下さい。"

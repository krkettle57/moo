class InvalidInputError(ValueError):
    """ユーザによって無効な入力がされた時に発生するエラー"""


class InvalidLengthInputError(InvalidInputError):
    """ユーザによって無効な桁の値が入力された時に発生するエラー"""


class InvalidValueInputError(InvalidInputError):
    """ユーザによって無効な値がされた時に発生するエラー"""

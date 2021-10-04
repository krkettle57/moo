import pytest
from model import MOO


class TestMOO:
    def test_target_default(self) -> None:
        moo = MOO()
        assert len(moo.target) == 3
        for num in moo.target:
            assert num in [i for i in range(10)]

    def test_target_length4(self) -> None:
        moo = MOO(target_length=4)
        assert len(moo.target) == 4
        for num in moo.target:
            assert num in [i for i in range(10)]

    def test_target_length10(self) -> None:
        with pytest.raises(ValueError):
            MOO(target_length=10)

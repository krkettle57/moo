import pytest
from model import MOO


class TestMOOConstructor:
    def test_target_default(self):
        moo = MOO()
        assert len(moo.target) == 3
        for num in moo.target:
            assert num in [i for i in range(10)]

    def test_target_length4(self):
        moo = MOO(target_length=4)
        assert len(moo.target) == 4
        for num in moo.target:
            assert num in [i for i in range(10)]

    def test_target_length10(self):
        with pytest.raises(ValueError):
            MOO(target_length=10)


@pytest.fixture()
def fixed_moo(mocker):
    moo = MOO()
    moo.target = [1, 2, 3]

    yield moo


class TestMOOCall:
    def test_call_correct(self, fixed_moo) -> None:
        called_result = fixed_moo.call([1, 2, 3])
        assert called_result.num_eat == 3

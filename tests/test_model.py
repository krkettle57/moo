import pytest
from model import MOO


class TestMOOConstructor:
    def test_target_length3(self):
        moo = MOO(3)
        assert len(moo.target) == 3
        for num in moo.target:
            assert num in [i for i in range(10)]

    def test_target_length4(self):
        moo = MOO(4)
        assert len(moo.target) == 4
        for num in moo.target:
            assert num in [i for i in range(10)]

    def test_target_length10(self):
        with pytest.raises(ValueError):
            MOO(target_length=10)


@pytest.fixture()
def fixed_moo():
    moo = MOO(3)
    moo.target = [1, 2, 3]

    yield moo


class TestMOOCall:
    def test_call_3eat(self, fixed_moo) -> None:
        called_result = fixed_moo.call([1, 2, 3])
        assert called_result.num_eat == 3
        assert called_result.num_bite == 0

    def test_call_2eat0bite(self, fixed_moo) -> None:
        called_result = fixed_moo.call([1, 2, 4])
        assert called_result.num_eat == 2
        assert called_result.num_bite == 0

    def test_call_1eat0bite(self, fixed_moo) -> None:
        called_result = fixed_moo.call([1, 4, 5])
        assert called_result.num_eat == 1
        assert called_result.num_bite == 0

    def test_call_1eat1bite(self, fixed_moo) -> None:
        called_result = fixed_moo.call([1, 4, 2])
        assert called_result.num_eat == 1
        assert called_result.num_bite == 1

    def test_call_1eat2bite(self, fixed_moo) -> None:
        called_result = fixed_moo.call([1, 3, 2])
        assert called_result.num_eat == 1
        assert called_result.num_bite == 2

    def test_call_0eat0bite(self, fixed_moo) -> None:
        called_result = fixed_moo.call([4, 5, 6])
        assert called_result.num_eat == 0
        assert called_result.num_bite == 0

    def test_call_0eat1bite(self, fixed_moo) -> None:
        called_result = fixed_moo.call([4, 5, 1])
        assert called_result.num_eat == 0
        assert called_result.num_bite == 1

    def test_call_0eat2bite(self, fixed_moo) -> None:
        called_result = fixed_moo.call([3, 5, 1])
        assert called_result.num_eat == 0
        assert called_result.num_bite == 2

    def test_call_3bite(self, fixed_moo) -> None:
        called_result = fixed_moo.call([2, 3, 1])
        assert called_result.num_eat == 0
        assert called_result.num_bite == 3

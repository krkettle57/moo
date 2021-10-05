import pytest
from model import MOO, Called, Target


class TargetConstructor:
    def test_target_length3(self):
        target = Target.generate(3)
        assert len(target.target) == 3
        assert target.target.isdigit()

    def test_target_length4(self):
        target = Target.generate(4)
        assert len(target.target) == 4
        assert target.target.isdigit()

    def test_target_length10(self):
        with pytest.raises(ValueError):
            Target.generate(10)


@pytest.fixture()
def fixed_target():
    target = Target.generate(3)
    target.target = "123"

    yield target


class TestCalled:
    def test_call_3eat(self, fixed_target) -> None:
        called_result = Called("123", fixed_target).get_result_set()
        assert called_result.num_eat == 3
        assert called_result.num_bite == 0

    def test_call_2eat0bite(self, fixed_target) -> None:
        called_result = Called("124", fixed_target).get_result_set()
        assert called_result.num_eat == 2
        assert called_result.num_bite == 0

    def test_call_1eat0bite(self, fixed_target) -> None:
        called_result = Called("145", fixed_target).get_result_set()
        assert called_result.num_eat == 1
        assert called_result.num_bite == 0

    def test_call_1eat1bite(self, fixed_target) -> None:
        called_result = Called("142", fixed_target).get_result_set()
        assert called_result.num_eat == 1
        assert called_result.num_bite == 1

    def test_call_1eat2bite(self, fixed_target) -> None:
        called_result = Called("132", fixed_target).get_result_set()
        assert called_result.num_eat == 1
        assert called_result.num_bite == 2

    def test_call_0eat0bite(self, fixed_target) -> None:
        called_result = Called("456", fixed_target).get_result_set()
        assert called_result.num_eat == 0
        assert called_result.num_bite == 0

    def test_call_0eat1bite(self, fixed_target) -> None:
        called_result = Called("451", fixed_target).get_result_set()
        assert called_result.num_eat == 0
        assert called_result.num_bite == 1

    def test_call_0eat2bite(self, fixed_target) -> None:
        called_result = Called("351", fixed_target).get_result_set()
        assert called_result.num_eat == 0
        assert called_result.num_bite == 2

    def test_call_3bite(self, fixed_target) -> None:
        called_result = Called("231", fixed_target).get_result_set()
        assert called_result.num_eat == 0
        assert called_result.num_bite == 3

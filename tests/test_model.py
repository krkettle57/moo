import pytest
from model import Called, Target


@pytest.fixture()
def fixed_target():
    target = Target("123")

    yield target


class TestTarget:
    def test_gen_length3(self):
        target = Target.generate(3)
        assert len(target.target) == 3
        assert target.target.isdigit()

    def test_gen_length4(self):
        target = Target.generate(4)
        assert len(target.target) == 4
        assert target.target.isdigit()

    def test_gen_length10(self):
        with pytest.raises(ValueError):
            Target.generate(10)

    def test_length(self, fixed_target):
        assert fixed_target.length == 3

    def test_as_list(self, fixed_target):
        assert fixed_target.as_list() == ["1", "2", "3"]


class TestCalled:
    def test_3eat(self, fixed_target) -> None:
        called_result = Called("123", fixed_target).get_result_set()
        assert called_result.num_eat == 3
        assert called_result.num_bite == 0

    def test_2eat0bite(self, fixed_target) -> None:
        called_result = Called("124", fixed_target).get_result_set()
        assert called_result.num_eat == 2
        assert called_result.num_bite == 0

    def test_1eat0bite(self, fixed_target) -> None:
        called_result = Called("145", fixed_target).get_result_set()
        assert called_result.num_eat == 1
        assert called_result.num_bite == 0

    def test_1eat1bite(self, fixed_target) -> None:
        called_result = Called("142", fixed_target).get_result_set()
        assert called_result.num_eat == 1
        assert called_result.num_bite == 1

    def test_1eat2bite(self, fixed_target) -> None:
        called_result = Called("132", fixed_target).get_result_set()
        assert called_result.num_eat == 1
        assert called_result.num_bite == 2

    def test_0eat0bite(self, fixed_target) -> None:
        called_result = Called("456", fixed_target).get_result_set()
        assert called_result.num_eat == 0
        assert called_result.num_bite == 0

    def test_0eat1bite(self, fixed_target) -> None:
        called_result = Called("451", fixed_target).get_result_set()
        assert called_result.num_eat == 0
        assert called_result.num_bite == 1

    def test_0eat2bite(self, fixed_target) -> None:
        called_result = Called("351", fixed_target).get_result_set()
        assert called_result.num_eat == 0
        assert called_result.num_bite == 2

    def test_3bite(self, fixed_target) -> None:
        called_result = Called("231", fixed_target).get_result_set()
        assert called_result.num_eat == 0
        assert called_result.num_bite == 3

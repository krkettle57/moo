import pytest
from moo.models.moo import MOO, Called, CallResultSet, Target


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
    def test_3eat(self, fixed_target):
        num_eat, num_bite = Called("123", fixed_target).get_eat_bite_num()
        assert num_eat == 3
        assert num_bite == 0

    def test_2eat0bite(self, fixed_target):
        num_eat, num_bite = Called("124", fixed_target).get_eat_bite_num()
        assert num_eat == 2
        assert num_bite == 0

    def test_1eat0bite(self, fixed_target):
        num_eat, num_bite = Called("145", fixed_target).get_eat_bite_num()
        assert num_eat == 1
        assert num_bite == 0

    def test_1eat1bite(self, fixed_target):
        num_eat, num_bite = Called("142", fixed_target).get_eat_bite_num()
        assert num_eat == 1
        assert num_bite == 1

    def test_1eat2bite(self, fixed_target):
        num_eat, num_bite = Called("132", fixed_target).get_eat_bite_num()
        assert num_eat == 1
        assert num_bite == 2

    def test_0eat0bite(self, fixed_target):
        num_eat, num_bite = Called("456", fixed_target).get_eat_bite_num()
        assert num_eat == 0
        assert num_bite == 0

    def test_0eat1bite(self, fixed_target):
        num_eat, num_bite = Called("451", fixed_target).get_eat_bite_num()
        assert num_eat == 0
        assert num_bite == 1

    def test_0eat2bite(self, fixed_target):
        num_eat, num_bite = Called("351", fixed_target).get_eat_bite_num()
        assert num_eat == 0
        assert num_bite == 2

    def test_3bite(self, fixed_target):
        num_eat, num_bite = Called("231", fixed_target).get_eat_bite_num()
        assert num_eat == 0
        assert num_bite == 3

    def test_as_list(self, fixed_target):
        called = Called("123", fixed_target)
        assert called.as_list() == ["1", "2", "3"]

    def test_get_result_set(self, fixed_target):
        called = Called("123", fixed_target)
        assert called.get_result_set() == CallResultSet(called, 3, 0)


@pytest.fixture()
def fixed_moo(fixed_target):
    moo = MOO(fixed_target)

    yield moo


class TestMOO:
    def test_call_correct(self, fixed_moo):
        fixed_moo.call("123")
        assert not fixed_moo.on_play
        assert fixed_moo.called_results == [CallResultSet(Called("123", fixed_moo.target), 3, 0)]

    def test_call_wrong(self, fixed_moo):
        fixed_moo.call("456")
        assert fixed_moo.on_play
        assert fixed_moo.called_results == [CallResultSet(Called("456", fixed_moo.target), 0, 0)]

    def test_call_wrong_and_correct(self, fixed_moo):
        fixed_moo.call("456")
        fixed_moo.call("123")
        assert not fixed_moo.on_play
        assert fixed_moo.called_results == [
            CallResultSet(Called("456", fixed_moo.target), 0, 0),
            CallResultSet(Called("123", fixed_moo.target), 3, 0),
        ]

    def test_finish(self, fixed_moo):
        fixed_moo.finish()
        assert not fixed_moo.on_play

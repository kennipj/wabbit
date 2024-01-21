from utils import compile_and_exec


def test_1():
    source = "print 1 + 2 * 3;"
    assert compile_and_exec(source) == ["7"]


def test_2():
    source = "print 1 * 2 - 3;"
    assert compile_and_exec(source) == ["-1"]


def test_3():
    source = "print (1 + 2) * 3;"
    assert compile_and_exec(source) == ["9"]


def test_4():
    source = "print -1 + 2 * 3;"
    assert compile_and_exec(source) == ["5"]


def test_5():
    source = "print -1 + ((2 * 3) - 4 * 2 - 3 + 1);"
    assert compile_and_exec(source) == ["-5"]

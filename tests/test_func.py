from utils import compile_and_exec


def test_1():
    source = """
        func square(n int) int {
            return n*n;
        }
        print square(5);
    """
    assert compile_and_exec(source) == ["25"]


def test_2():
    source = """
        func fib(n int) int {
            if n < 2 {
                return 1;
            } else {
                return fib(n-1) + fib(n-2);
            }
            return 0;
        }
        print fib(10);
    """
    assert compile_and_exec(source) == ["89"]


def test_3():
    source = """
        func nothing() int {
            return 5;
        }
        print nothing();
    """
    assert compile_and_exec(source) == ["5"]


def test_4():
    source = """
    func multi(x int, y float, z bool, a char) bool {
        return true and false;
    }
    print multi(2, 3.0, true, '7');
    """
    assert compile_and_exec(source) == ["false"]


def test_5():
    source = """
    func some_func(x int) char {
        return '1';
    }
    print some_func(5);
    """
    assert compile_and_exec(source) == ["1"]

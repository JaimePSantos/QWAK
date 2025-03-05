import sys
import unittest
from termcolor import colored

def run_tests(test_pattern):
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern=test_pattern)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result.wasSuccessful()

def run_qwakpath_tests():
    from tests.test_QwakPath import TestQWAKComplete
    test_instance = TestQWAKComplete()
    methods = [method for method in dir(test_instance) if method.startswith('test_')]
    for method in methods:
        try:
            getattr(test_instance, method)()
            print(colored(f"OK - {method}", "green"))
        except Exception as e:
            print(colored(f"ERR: {method}", "red"))
        finally:
            print(colored(f"END - {method}", "cyan"))

def run_stochastic_tests():
    from tests.test_StochasticQwak import TestStochasticQWAK
    test_instance = TestStochasticQWAK()
    methods = [method for method in dir(test_instance) if method.startswith('test_')]
    for method in methods:
        try:
            getattr(test_instance, method)()
            print(colored(f"OK - {method}", "green"))
        except Exception as e:
            print(colored(f"ERR: {method}", "red"))
        finally:
            print(colored(f"END - {method}", "cyan"))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python installcheck.py [full|cupy|Stochastic|qwakpath|stochasticQwak]")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "full":
        success = run_tests("test_*.py")
        run_qwakpath_tests()
        run_stochastic_tests()
        sys.exit(0)
    elif arg == "cupy":
        success = run_tests("test_cupy*.py")
    elif arg == "Stochastic":
        success = run_tests("test_stochastic*.py")
    elif arg == "qwakpath":
        run_qwakpath_tests()
        sys.exit(0)
    elif arg == "stochasticQwak":
        run_stochastic_tests()
        sys.exit(0)
    else:
        print("Invalid argument. Use 'full', 'cupy', 'Stochastic', 'qwakpath', or 'stochasticQwak'.")
        sys.exit(1)

    if success:
        print("All tests passed.")
    else:
        print("Some tests failed.")
        sys.exit(1)

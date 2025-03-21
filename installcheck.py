import sys
import unittest

def color_text(text, color):
    """Returns the text wrapped in ANSI color codes.

    Parameters
    ----------
    text : str
        The text to be colored.
    color : str
        The color to apply. Options are 'green', 'red', 'cyan', 'yellow'.

    Returns
    -------
    str
        The colored text.
    """
    colors = {
        "green": "\033[92m",
        "red": "\033[91m",
        "cyan": "\033[96m",
        "yellow": "\033[93m",
        "end": "\033[0m"
    }
    return f"{colors[color]}{text}{colors['end']}"

def run_tests(test_pattern):
    """Discovers and runs unittests matching the given pattern.

    Parameters
    ----------
    test_pattern : str
        The pattern to match test files.

    Returns
    -------
    bool
        True if all tests pass, False otherwise.
    """
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir='.', pattern=test_pattern)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result.wasSuccessful()

def run_qwakpath_tests():
    """Runs the tests in the test_QwakPath file."""
    from tests.test_QwakPath import TestQWAKComplete
    test_instance = TestQWAKComplete()
    methods = [method for method in dir(test_instance) if method.startswith('test_')]
    print(color_text("run_qwakpath_tests", "yellow"))
    for method in methods:
        try:
            getattr(test_instance, method)()
            print("\t" + color_text(f"OK - {method}", "green"))
        except Exception as e:
            print("\t" + color_text(f"ERR: {method}", "red"))
        finally:
            print("\t" + color_text(f"END - {method}", "cyan"))

def run_stochastic_tests():
    """Runs the tests in the test_StochasticQwak file."""
    from tests.test_StochasticQwak import TestStochasticQWAK
    test_instance = TestStochasticQWAK()
    methods = [method for method in dir(test_instance) if method.startswith('test_')]
    print(color_text("run_stochastic_tests", "yellow"))
    for method in methods:
        try:
            getattr(test_instance, method)()
            print("\t" + color_text(f"OK - {method}", "green"))
        except Exception as e:
            print("\t" + color_text(f"ERR: {method}", "red"))
        finally:
            print("\t" + color_text(f"END - {method}", "cyan"))

def run_cupy_tests():
    """Runs the tests in the test_QwakCupyCycle file."""
    from tests.test_QwakCupyCycle import TestQWAKCupyCycle
    test_instance = TestQWAKCupyCycle()
    methods = [method for method in dir(test_instance) if method.startswith('test_')]
    print(color_text("run_cupy_tests", "yellow"))
    for method in methods:
        try:
            getattr(test_instance, method)()
            print("\t" + color_text(f"OK - {method}", "green"))
        except Exception as e:
            print("\t" + color_text(f"ERR: {method}", "red"))
        finally:
            print("\t" + color_text(f"END - {method}", "cyan"))

def run_cycle_tests():
    """Runs the tests in the test_QwakCycle file."""
    from tests.test_QwakCycle import TestQWAKCycle
    test_instance = TestQWAKCycle()
    methods = [method for method in dir(test_instance) if method.startswith('test_')]
    print(color_text("run_cycle_tests", "yellow"))
    for method in methods:
        try:
            getattr(test_instance, method)()
            print("\t" + color_text(f"OK - {method}", "green"))
        except Exception as e:
            print("\t" + color_text(f"ERR: {method}", "red"))
        finally:
            print("\t" + color_text(f"END - {method}", "cyan"))

def run_complete_tests():
    """Runs the tests in the test_QwakComplete file."""
    from tests.test_QwakComplete import TestQWAKComplete
    test_instance = TestQWAKComplete()
    methods = [method for method in dir(test_instance) if method.startswith('test_')]
    print(color_text("run_complete_tests", "yellow"))
    for method in methods:
        try:
            getattr(test_instance, method)()
            print("\t" + color_text(f"OK - {method}", "green"))
        except Exception as e:
            print("\t" + color_text(f"ERR: {method}", "red"))
        finally:
            print("\t" + color_text(f"END - {method}", "cyan"))

if __name__ == "__main__":
    """Main entry point for the script. Parses command line arguments and runs the appropriate tests."""
    if len(sys.argv) != 2:
        print("Usage: python installcheck.py [full|cupy|Stochastic|qwakpath|stochasticQwak|cycle|complete]")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "full":
        success = run_tests("test_*.py")
        run_qwakpath_tests()
        run_stochastic_tests()
        run_cupy_tests()
        run_cycle_tests()
        run_complete_tests()
        sys.exit(0)
    elif arg == "cupy":
        run_cupy_tests()
        sys.exit(0)
    elif arg == "Stochastic":
        success = run_tests("test_stochastic*.py")
    elif arg == "qwakpath":
        run_qwakpath_tests()
        sys.exit(0)
    elif arg == "stochasticQwak":
        run_stochastic_tests()
        sys.exit(0)
    elif arg == "cycle":
        run_cycle_tests()
        sys.exit(0)
    elif arg == "complete":
        run_complete_tests()
        sys.exit(0)
    else:
        print("Invalid argument. Use 'full', 'cupy', 'Stochastic', 'qwakpath', 'stochasticQwak', 'cycle', or 'complete'.")
        sys.exit(1)

    if success:
        print("All tests passed.")
    else:
        print("Some tests failed.")
        sys.exit(1)

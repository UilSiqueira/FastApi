import asyncio
import sys

from deps import clear_test_db
from helpers import run_custom_test, ordering_key, get_test_dirs, import_test_functions

all_tests = 'test'


async def run_tests(tests_to_run=all_tests):
    if len(sys.argv) > 1:
        tests_to_run = sys.argv[1]

    test_dirs = get_test_dirs()
    test_functions = import_test_functions(test_dirs, tests_to_run)
    async_tests = [await run_custom_test(function) for function in test_functions]

    try:
        result = [value for value in async_tests]
        ordered_results = sorted(result, key=ordering_key)

        for index, value in enumerate(ordered_results, start=1):
            print(f"{index} - {value}")
    finally:
        # clear db after tests
        await clear_test_db()


if __name__ == "__main__":
    asyncio.run(run_tests())

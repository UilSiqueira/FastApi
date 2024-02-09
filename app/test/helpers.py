import os
import traceback
import importlib
from pathlib import Path


def format_string(result, test_name, error=""):
    result_ok = f"{result}:   {test_name}\n"
    result_failed = f"{result}:   {test_name} - {error}\n"

    test_result = result_ok if not error else result_failed
    return test_result


async def run_custom_test(test_function, *args):
    try:
        result = await test_function(*args)

        if result is None:
            return format_string("PASSED", test_function.__name__)

    except AssertionError as error:
        return format_string("***FAILED***", test_function.__name__, str(error))

    except Exception as error:
        traceback_error = "".join(
            traceback.format_exception(type(error), error, error.__traceback__)
        )
        return format_string(
            "***ERROR*** - Exception", test_function.__name__, str(traceback_error)
        )  # Complete error: str(traceback_error)


def ordering_key(string):
    if string.startswith("PASSED"):
        return ""
    else:
        return string[:5]


def get_test_dirs():
    base_dir = Path.cwd()
    test_dir = base_dir / "test"

    test_subdirs = [
        subdir.name
        for subdir in test_dir.iterdir()
        if subdir.is_dir() and not subdir.name.startswith("__")
    ]

    return test_subdirs


def get_test_files(folder):
    files_python = [file for file in os.listdir(folder) if file.endswith(".py")]
    return files_python


def import_test_functions(packages, tests_to_run='test'):
    base_dir = os.getcwd()
    test_dir = f"{base_dir}/test"
    test_module = test_dir[1:].replace("/", ".")
    function_objects = []

    for package in packages:
        files = get_test_files(f"{test_dir}/{package}")
        for file in files:
            module_name = file.replace(".py", "")
            module_path = f"{test_module}.{package}.{module_name}"

            try:
                module = importlib.import_module(module_path)
                functions = [
                    func for func in dir(module)
                    if callable(getattr(module, func)) and func.startswith(tests_to_run)
                ]

                for func_name in functions:
                    func = getattr(module, func_name)
                    globals()[func_name] = func
                    function_objects.append(getattr(module, func_name))
            except Exception as e:
                print(f"Error importing function from module: {module_name}: {e}")
    return function_objects

#!/usr/bin/env python3
"""
Custom mini-language interpreter.
Commands:
    hi                  -> prints "Hello!"
    print <text...>     -> prints the given text
"""

import importlib
import importlib.util
import sys
import os
import time
import subprocess
import json
import jsonhandle
import iot
isinrepl = False  # Global variable to track if we are in REPL mode

def load_variables():
    try:
        variables = jsonhandle.handle_json("variables.json")
        if isinstance(variables, dict):
            return variables
    except FileNotFoundError:
        pass
    return {}


def save_variables(variables):
    if not isinstance(variables, dict):
        raise ValueError("Variables data must be saved as a dictionary.")
    jsonhandle.handle_json("variables.json", variables)


def evaluate_setvar_value(value, suffix):
    value = value.strip()
    if not value:
        raise ValueError("Empty setvar value")

    if value.startswith("!"):
        value = value[1:].strip()

    if value.startswith("input"):
        prompt = value[5:].strip()
        if prompt and prompt[0] in "'\"" and prompt[-1] == prompt[0]:
            prompt = prompt[1:-1]
        return input(prompt or "Input: ")

    try:
        result = eval(value, globals())
    except Exception as e:
        raise ValueError(f"Unable to evaluate expression '{value}': {e}")

    if callable(result):
        return result()
    return result


def runcommand(command_line, line_num=None):
    try:
        """Parses and executes a single command line."""
        parts = command_line.strip().split()
        if not parts:
            return True  # Skip empty lines

        command = parts[0].lower()
        args = parts[1:]  # everything after the command
        suffix = f" (line {line_num})" if line_num is not None else ""

        if command == "hi":
            print("Hello!")
        elif command == "print":
            if args:
                print(" ".join(args))
            else:
                print(f"Error: 'print' requires arguments{suffix}")
        elif command == "exit":
            if line_num is None:
                print("Exiting REPL.")
            else:
                print("Exiting interpreter.")
            return False
        elif command == "setvar":
            if len(args) >= 2:
                var_name = args[0]
                raw_value = " ".join(args[1:])
                try:
                    var_value = evaluate_setvar_value(raw_value, suffix) if raw_value.startswith("!") else raw_value
                except Exception as e:
                    print(f"Error setting variable '{var_name}': {e}{suffix}")
                    return True

                try:
                    variables = load_variables()
                    variables[var_name] = var_value
                    save_variables(variables)
                    print(f"Variable '{var_name}' set to '{var_value}'{suffix}")
                except Exception as e:
                    print(f"Error saving variable '{var_name}': {e}{suffix}")
            else:
                print(f"Error: 'setvar' requires a variable name and value{suffix}")
        elif command == "getvar":
            if len(args) == 1:
                var_name = args[0]
                try:
                    variables = jsonhandle.handle_json("variables.json")
                    if isinstance(variables, dict) and var_name in variables:
                        print(f"{var_name} = {variables[var_name]}{suffix}")
                    else:
                        print(f"Variable '{var_name}' not found{suffix}")
                except FileNotFoundError:
                    print(f"No variables stored yet{suffix}")
            else:
                print(f"Error: 'getvar' requires a variable name{suffix}")
        elif command == "help":
            if line_num is None or isinrepl:
                print("Available commands:")
                print("  hi                  -> prints 'Hello!'")
                print("  print <text...>     -> prints the given text")
                print("  setvar <name> <value> -> sets a variable")
                print("  setvar <name> !input -> prompts for input and stores the result")
                print("  setvar <name> !<function> -> calls a function and stores its return value")
                print("  getvar <name>       -> retrieves a variable's value")
                print("  deletevar <name>    -> deletes a stored variable")
                print("  listvars            -> lists all stored variables")
                print("  wait <seconds>      -> pauses for a given number of seconds")
                print("  sleep <seconds>     -> pauses for a given number of seconds")
                print("  repeat <n> <cmd>    -> runs a command n times")
                print("  addoffpackage <name> -> installs a package from PyPI")
                print("  addlocalpackage <path> -> installs a local package or imports a .py file")
                print("  runfile <filename>  -> executes a custom .bscript file")
                print("  runfunction <module> <function> -> runs a function from a module")
                print("  clear               -> clears the terminal screen")
                print("  time                -> shows the current time")
                print("  date                -> shows the current date")
                print("  datetime            -> shows the current date and time")
                print("  exit                -> exits the interpreter")
                print("  help                -> shows this help message")
                print("  howbscript          -> shows how to make a .bscript file")
                print("  exit                -> exits the interpreter")
        elif command == "wait":
            if len(args) == 1 and args[0].isdigit():
                wait_time = int(args[0])
                print(f"Waiting for {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Error: 'wait' requires a single integer argument{suffix}")
        elif command == "addoffpackage":
            if len(args) == 1:
                package_name = args[0]
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
                    print(f"Package '{package_name}' added{suffix}")
                except subprocess.CalledProcessError:
                    print(f"Failed to add package '{package_name}'{suffix}")
            else:
                print(f"Error: 'addoffpackage' requires a single package name{suffix}")
        elif command == "addlocalpackage":
            if len(args) == 1:
                package_source = args[0]
                try:
                    if os.path.exists(package_source):
                        if package_source.endswith(".py"):
                            module_name = os.path.splitext(os.path.basename(package_source))[0]
                            spec = importlib.util.spec_from_file_location(module_name, package_source)
                            if spec is not None and spec.loader is not None:
                                module = importlib.util.module_from_spec(spec)
                                sys.modules[module_name] = module
                                loader = spec.loader
                                if hasattr(loader, "exec_module"):
                                    loader.exec_module(module)
                                elif hasattr(loader, "load_module"):
                                    loader.load_module(module_name)
                                else:
                                    raise ImportError("Loader does not support module execution")
                                print(f"Python file '{package_source}' imported as module '{module_name}'{suffix}.")
                            else:
                                print(f"Error: Could not create module spec or loader for '{package_source}'{suffix}.")
                        else:
                            print(f"Installing local package from '{package_source}'{suffix}...")
                            subprocess.check_call([sys.executable, "-m", "pip", "install", package_source])
                            print(f"Local package '{package_source}' installed successfully{suffix}.")
                    else:
                        print(f"Installing package '{package_source}' from PyPI{suffix}...")
                        subprocess.check_call([sys.executable, "-m", "pip", "install", package_source])
                        print(f"Package '{package_source}' installed successfully from PyPI{suffix}.")
                except subprocess.CalledProcessError as e:
                    print(f"Installation failed for '{package_source}'. Error code: {e.returncode}{suffix}")
                except FileNotFoundError:
                    print(f"Error: File '{package_source}' not found{suffix}.")
                except Exception as e:
                    print(f"Unexpected error while processing '{package_source}': {e}{suffix}")
            else:
                print(f"Error: 'addlocalpackage' requires exactly one argument (path, .py file, or package name){suffix}")
        elif command == "runfile":
            if len(args) == 1:
                run_custom_file(args[0])
            else:
                print(f"Error: 'runfile' requires exactly one argument (file path){suffix}")
        elif command == "runfunction":
            if len(args) == 2:
                module_name = args[0]
                function_name = args[1]
                try:
                    module = importlib.import_module(module_name)
                    func = getattr(module, function_name)
                    if callable(func):
                        func()
                    else:
                        print(f"Error: '{function_name}' in module '{module_name}' is not callable.{suffix}")
                except ModuleNotFoundError:
                    print(f"Error: Module '{module_name}' not found.{suffix}")
                except AttributeError:
                    print(f"Error: Function '{function_name}' not found in module '{module_name}'.{suffix}")
                except Exception as e:
                    print(f"Unexpected error while running function '{function_name}': {e}{suffix}")
            else:
                print(f"Error: 'runfunction' requires exactly two arguments (module name and function name){suffix}")
        elif command == "deletevar":
            if len(args) == 1:
                var_name = args[0]
                try:
                    variables = jsonhandle.handle_json("variables.json")
                    if isinstance(variables, dict) and var_name in variables:
                        del variables[var_name]
                        jsonhandle.handle_json("variables.json", variables)
                        print(f"Variable '{var_name}' deleted{suffix}")
                    else:
                        print(f"Variable '{var_name}' not found{suffix}")
                except FileNotFoundError:
                    print(f"No variables stored yet{suffix}")
            else:
                print(f"Error: 'deletevar' requires a variable name{suffix}")
        elif command == "listvars":
            try:
                variables = jsonhandle.handle_json("variables.json")
                if isinstance(variables, dict):
                    if variables:
                        print("Stored variables:")
                        for var_name, var_value in variables.items():
                            print(f"  {var_name} = {var_value}")
                    else:
                        print("No variables stored.")
                else:
                    print("No variables stored.")
            except FileNotFoundError:
                print("No variables stored yet.")
        elif command == "repeat":
            if len(args) >= 2 and args[0].isdigit():
                repeat_count = int(args[0])
                repeat_command = " ".join(args[1:])
                repeat_steps = [step.strip() for step in repeat_command.split("/") if step.strip()]
                for _ in range(repeat_count):
                    for step in repeat_steps:
                        runcommand(step, line_num)
            else:
                print(f"Error: 'repeat' requires a count and a command{suffix}")
        elif command == "howbscript":
            print("To create a .bscript file, simply write your commands in a text file and save it with the .bscript extension.")
            print("You can then run it using the 'runfile <filename>' command in the REPL or by passing the filename as an argument when starting the interpreter.")
            print("Example .bscript content:")
            print("# This is a comment")
            print("print hello world # This will print 'hello world'")
            print("setvar myvar 42 # This sets a variable 'myvar' to 42")
            print("getvar myvar # This retrieves the value of 'myvar'")
            print("addoffpackage requests # This installs the 'requests' package from PyPI")
            print("addlocalpackage ./local_package # This installs a local package from the specified path")
            print("runfunction mymodule myfunction # This runs 'myfunction' from 'mymodule'")
            print("deletevar myvar # This deletes the variable 'myvar'")
            print("listvars # This lists all stored variables")
            print("repeat 3 print hello # This will print 'hello' three times")
            print("exit # This exits the interpreter")
        elif command == "comment":
            # This command does nothing; it's just a comment
            pass
        elif command.startswith("#"):
            # This is a comment line; ignore it
            pass
        elif command == "clear":
            if line_num is None:
                os.system('cls' if os.name == 'nt' else 'clear')
            else:
                print(f"Error: 'clear' command can only be used in REPL mode{suffix}")
        elif command == "time":
            print(f"Current time: {time.strftime('%Y-%m-%d %H:%M:%S')}{suffix}")
        elif command == "date":
            print(f"Current date: {time.strftime('%Y-%m-%d')}{suffix}")
        elif command == "datetime":
            print(f"Current date and time: {time.strftime('%Y-%m-%d %H:%M:%S')}{suffix}")
        elif command == "sleep":
            if len(args) == 1 and args[0].isdigit():
                sleep_time = int(args[0])
                print(f"Sleeping for {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                print(f"Error: 'sleep' requires a single integer argument{suffix}")
        elif command == "listmodules":
            print("Currently loaded modules:")
            for module_name in sorted(sys.modules.keys()):
                print(f"  {module_name}")
        elif command == "reloadmodule":
            if len(args) == 1:
                module_name = args[0]
                if module_name in sys.modules:
                    try:
                        importlib.reload(sys.modules[module_name])
                        print(f"Module '{module_name}' reloaded{suffix}")
                    except Exception as e:
                        print(f"Error reloading module '{module_name}': {e}{suffix}")
                else:
                    print(f"Module '{module_name}' is not currently loaded{suffix}")
            else:
                print(f"Error: 'reloadmodule' requires a single module name{suffix}")
        elif command == "unloadmodule":
            if len(args) == 1:
                module_name = args[0]
                if module_name in sys.modules:
                    del sys.modules[module_name]
                    print(f"Module '{module_name}' unloaded{suffix}")
                else:
                    print(f"Module '{module_name}' is not currently loaded{suffix}")
            else:
                print(f"Error: 'unloadmodule' requires a single module name{suffix}")
        elif command == "listvars":
            try:
                variables = jsonhandle.handle_json("variables.json")
                if isinstance(variables, dict):
                    if variables:
                        print("Stored variables:")
                        for var_name, var_value in variables.items():
                            print(f"  {var_name} = {var_value}")
                    else:
                        print("No variables stored.")
                else:
                    print("No variables stored.")
            except FileNotFoundError:
                print("No variables stored yet.")
        elif command == "while":
            if len(args) >= 2:
                condition = args[0]
                loop_command = " ".join(args[1:])
                while True:
                    try:
                        if eval(condition):
                            runcommand(loop_command, line_num)
                        else:
                            break
                    except Exception as e:
                        print(f"Error evaluating condition '{condition}': {e}{suffix}")
                        break
            else:
                print(f"Error: 'while' requires a condition and a command{suffix}")
        elif command == "if":
            if len(args) >= 2:
                condition = args[0]
                if_command = " ".join(args[1:])
                ifelif_command = " ".join(args[2:]) if len(args) > 2 else None
                ifelse_command = " ".join(args[2:]) if len(args) > 2 else " ".join(args[5:]) if len(args) > 5 else None
                if ifelif_command and ifelif_command.startswith("elif"):
                    elif_condition = args[2]
                    elif_command = " ".join(args[3:])
                    try:
                        if eval(condition):
                            runcommand(if_command, line_num)
                        elif eval(elif_condition):
                            runcommand(elif_command, line_num)
                    except Exception as e:
                        print(f"Error evaluating condition '{condition}' or '{elif_condition}': {e}{suffix}")
                elif ifelse_command and ifelse_command.startswith("else"):
                    else_command = " ".join(args[3:])
                    try:
                        if eval(condition):
                            runcommand(if_command, line_num)
                        else:
                            runcommand(else_command, line_num)
                    except Exception as e:
                        print(f"Error evaluating condition '{condition}': {e}{suffix}")
                if ifelif_command == "elif":
                    elif_condition = args[2]
                    elif_command = " ".join(args[3:])
                    try:
                        if eval(condition):
                            runcommand(if_command, line_num)
                        elif eval(elif_condition):
                            runcommand(elif_command, line_num)
                    except Exception as e:
                        print(f"Error evaluating condition '{condition}' or '{elif_condition}': {e}{suffix}")
                try:
                    if eval(condition):
                        runcommand(if_command, line_num)
                except Exception as e:
                    print(f"Error evaluating condition '{condition}': {e}{suffix}")
            else:
                print(f"Error: 'if' requires a condition and a command{suffix}")
        elif command == "for":
            if len(args) >= 3 and args[1] == "in":
                var_name = args[0]
                iterable = args[2]
                loop_command = " ".join(args[3:])
                try:
                    for value in eval(iterable):
                        jsonhandle.handle_json("variables.json", {var_name: value})
                        runcommand(loop_command, line_num)
                except Exception as e:
                    print(f"Error in 'for' loop: {e}{suffix}")
            else:
                print(f"Error: 'for' requires a variable, 'in', an iterable, and a command{suffix}")
        elif command == "try":
            if len(args) >= 2:
                try_command = " ".join(args[:-1])
                except_command = args[-1]
                try:
                    runcommand(try_command, line_num)
                except Exception as e:
                    print(f"Error in 'try' block: {e}{suffix}")
                    runcommand(except_command, line_num)
            else:
                print(f"Error: 'try' requires a command and an 'except' command{suffix}")
        elif command == "except":
            print(f"Error: 'except' should follow a 'try' block{suffix}")
        elif command == "finally":
            print(f"Error: 'finally' should follow a 'try' block{suffix}")
        elif command == "raise":
            if args:
                raise Exception(" ".join(args))
            else:
                raise Exception("An error was raised.")
        elif command == "assert":
            if len(args) >= 1:
                condition = " ".join(args)
                try:
                    assert eval(condition)
                except AssertionError:
                    print(f"Assertion failed: {condition}{suffix}")
                except Exception as e:
                    print(f"Error evaluating assertion '{condition}': {e}{suffix}")
            else:
                print(f"Error: 'assert' requires a condition to evaluate{suffix}")
        elif command == "import":
            if len(args) == 1:
                module_name = args[0]
                try:
                    importlib.import_module(module_name)
                    print(f"Module '{module_name}' imported{suffix}")
                except ModuleNotFoundError:
                    print(f"Error: Module '{module_name}' not found{suffix}")
                except Exception as e:
                    print(f"Unexpected error while importing module '{module_name}': {e}{suffix}")
            else:
                print(f"Error: 'import' requires a single module name{suffix}")
        elif command == "unimport":
            if len(args) == 1:
                module_name = args[0]
                if module_name in sys.modules:
                    del sys.modules[module_name]
                    print(f"Module '{module_name}' unimported{suffix}")
                else:
                    print(f"Module '{module_name}' is not currently imported{suffix}")
            else:
                print(f"Error: 'unimport' requires a single module name{suffix}")
        elif command == "listimported":
            print("Currently imported modules:")
            for module_name in sorted(sys.modules.keys()):
                print(f"  {module_name}")
        elif command == "reload":
            if len(args) == 1:
                module_name = args[0]
                if module_name in sys.modules:
                    try:
                        importlib.reload(sys.modules[module_name])
                        print(f"Module '{module_name}' reloaded{suffix}")
                    except Exception as e:
                        print(f"Error reloading module '{module_name}': {e}{suffix}")
                else:
                    print(f"Module '{module_name}' is not currently imported{suffix}")
            else:
                print(f"Error: 'reload' requires a single module name{suffix}")
        elif command == "unload":
            if len(args) == 1:
                module_name = args[0]
                if module_name in sys.modules:
                    del sys.modules[module_name]
                    print(f"Module '{module_name}' unloaded{suffix}")
                else:
                    print(f"Module '{module_name}' is not currently imported{suffix}")
            else:
                print(f"Error: 'unload' requires a single module name{suffix}")
        elif command == "listloaded":
            print("Currently loaded modules:")
            for module_name in sorted(sys.modules.keys()):
                print(f"  {module_name}")
        elif command == "exit":
            if line_num is None:
                print("Exiting REPL.")
            else:
                print("Exiting interpreter.")
            sys.exit(0) 
        elif command == "input":
            user_input = input("Input: ")
            print(f"You entered: {user_input}{suffix}")
            return user_input
        elif command == "eval":
            if args:
                expression = " ".join(args)
                try:
                    result = eval(expression, globals())
                    print(f"Result: {result}{suffix}")
                except Exception as e:
                    print(f"Error evaluating expression '{expression}': {e}{suffix}")
        elif command == "exec":
            if args:
                code = " ".join(args)
                try:
                    exec(code, globals())
                    print(f"Executed code: {code}{suffix}")
                except Exception as e:
                    print(f"Error executing code '{code}': {e}{suffix}")
        elif command == "filecreate":
            if len(args) == 2:
                file_path = args[0]
                file_content = args[1]
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(file_content)
                    print(f"File '{file_path}' created{suffix}")
                except Exception as e:
                    print(f"Error creating file '{file_path}': {e}{suffix}")
        elif command == "fileread":
            if len(args) == 1:
                file_path = args[0]
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    print(f"Content of '{file_path}':\n{content}{suffix}")
                except Exception as e:
                    print(f"Error reading file '{file_path}': {e}{suffix}")
        elif command == "filedelete":
            if len(args) == 1:
                file_path = args[0]
                try:
                    os.remove(file_path)
                    print(f"File '{file_path}' deleted{suffix}")
                except Exception as e:
                    print(f"Error deleting file '{file_path}': {e}{suffix}")
        elif command == "fileappend":
            if len(args) == 2:
                file_path = args[0]
                content_to_append = args[1]
                try:
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write(content_to_append)
                    print(f"Appended to file '{file_path}'{suffix}")
                except Exception as e:
                    print(f"Error appending to file '{file_path}': {e}{suffix}")
        elif command == "iot-init":
            if len(args) == 2:
                email = args[0]
                password = args[1]
                try:
                    iot.init(email, password)
                except Exception as e:
                    print(f"Error initializing IoT: {e}{suffix}")
        elif command == "iot-senddata":
            remainder = command_line.strip()[len(parts[0]):].lstrip()
            try:
                data, end = json.JSONDecoder().raw_decode(remainder)
                credentials = remainder[end:].split(maxsplit=1)
                if not isinstance(data, dict) or len(credentials) != 2:
                    raise ValueError("expected a JSON object followed by email and password")
                email2, password2 = credentials
                iot.senddata(data, email=email2, password=password2)
                print(f"Data sent to IoT{suffix}")
            except Exception as e:
                print(f"Error sending data to IoT: {e}{suffix}")
        elif command == "iot-getdata":
            if len(args) == 2:
                email = args[0]
                password = args[1]
                try:
                    print(iot.getdata(email=email, password=password))
                except Exception as e:
                    print(f"Error retrieving data from IoT: {e}{suffix}")
        else:
            print(f"Unknown command '{command}'{suffix}")
    except Exception as e:
        print(f"Error processing command '{command_line}': {e}")

    return True

def repl_mode():
    global isinrepl
    isinrepl = True
    print("ScriptB REPL. Type 'exit' to quit, 'help' for assistance, 'runfile <filename>' to execute a custom file, 'howbscript' to show how to make a .bscript.")
    input_buffer = []
    while True:
        try:
            line = input(">>> ")
        except EOFError as e:
            print(f"\nExiting REPL. {e}")
            break
        except KeyboardInterrupt:
            print("\nExiting REPL.")
            sys.exit(0)

        if not runcommand(line):
            break

def run_custom_file(filepath):
    """Reads and executes commands from a custom file."""
    if not os.path.isfile(filepath):
        print(f"Error: File '{filepath}' not found.")
        return

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                if not runcommand(line, line_num):
                    break

    except Exception as e:
        print(f"Error reading file: {e}")

def main():
    # Check if 3 arguments are passed: script name, filename, and "debug"
    if len(sys.argv) == 3 and sys.argv[2] == "debug":
        print("DEBUG")
        try:
            # Pass the filename (sys.argv[1]), not "debug"
            run_custom_file(sys.argv[1])
        except Exception as e:
            print(f"Error : {e}")
            print("Close this window to exit")
            while True:
                pass
    elif len(sys.argv) != 2:
        repl_mode()
    else:
        run_custom_file(sys.argv[1])

if __name__ == "__main__":
    main()

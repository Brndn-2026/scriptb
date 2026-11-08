# Language reference

ScriptB reads one command per line. Its interpreter splits the line on whitespace; it does not parse quoted arguments like a shell. Examples below show the command forms implemented in the current interpreter, not a promise of a stable language specification.

## Basic commands

| Form | Behavior |
| --- | --- |
| `hi` | Prints `Hello!`. |
| `print <text...>` | Prints the remaining whitespace-separated words. |
| `repeat <count> <command>` | Runs a command repeatedly; a slash (`/`) can separate multiple commands. |
| `wait <seconds>` / `sleep <seconds>` | Pauses for a non-negative integer number of seconds. |
| `# <comment>` / `comment` | Does nothing. |
| `help` / `howbscript` | Prints the built-in help or a short script-file example in the interactive prompt. |
| `exit` | Ends the prompt or script. |

## Variables

| Form | Behavior |
| --- | --- |
| `setvar <name> <value>` | Stores a value in `variables.json`; values beginning with `!` are evaluated or prompt for input. |
| `getvar <name>` | Prints a stored value. |
| `listvars` | Lists stored values. |
| `deletevar <name>` | Deletes a stored value. |

Variable storage is JSON-backed. Do not use `setvar` with an untrusted expression: `!` values can invoke Python evaluation.

## Conditions and loops

`if <expression> <command>`, `while <expression> <command>`, and `for <name> in <expression> <command>` are implemented as single-line commands. The interpreter evaluates expressions as Python and does not provide conventional indented blocks. Keep expressions to a single whitespace-delimited token; test behavior carefully before relying on these commands.

## Files, modules, and Python operations

The interpreter also implements `filecreate`, `fileread`, `fileappend`, and `filedelete`; `import`, `unimport`, `reload`, `unload`, `listimported`, `listmodules`, and related module-listing commands; `runfile` and `runfunction`; and `addoffpackage` / `addlocalpackage` for package or local-file operations. `eval` and `exec` evaluate or execute Python code. These commands can change files, install packages, or run code in the interpreter process.

`time`, `date`, and `datetime` print the current local time or date. `clear` is available only in the interactive prompt. The source also contains `iot-init`, `iot-senddata`, and `iot-getdata`, which depend on the project's external IoT service.

## Safety and compatibility

Only run scripts you trust. In particular, Python evaluation/execution, module and package operations, and file commands are not sandboxed. The bundled executable in this repository is for Windows; support for other operating systems has not been verified.

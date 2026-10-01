# ScriptB Language Reference

This is an initial reference, not a complete language specification. It records syntax demonstrated by the shipped sample scripts. Parsing rules, types, error behavior, and compatibility guarantees are not yet documented.

## Running scripts

Run a file from PowerShell in the project folder:

```powershell
.\scriptb.exe .\path\to\file.bscript
```

The release also includes `bscript.exe`, which is invoked by `main.bat` to run `main.bscript`.

## Demonstrated commands

| Form | Demonstrated behavior |
| --- | --- |
| `print text` | Prints the text after `print`. |
| `repeat count command` | Runs the following command the specified number of times, as in `repeat 3 print Hello`. |
| `wait seconds` | Requests a delay, as in `wait 1`. Exact timing behavior is not specified. |
| `# comment` | A comment line is present in `test.bscript`; placement and parsing rules are not specified. |

## Still to specify

The bundled `test.bscript` contains additional command probes, including variables, conditionals, loops, assertions, module operations, and exception-like forms. That file is not a formal specification, and this release's behavior for those commands has not been documented here. Treat them as unverified until they have dedicated examples and tests.
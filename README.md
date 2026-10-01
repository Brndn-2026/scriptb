# ScriptB

ScriptB is a small, command-based language for learning scripting and experimenting with short programs. It favors readable instructions such as `print` and `repeat`; this release is aimed at beginners, not as a replacement for Python or shell scripting.

The project currently ships Windows executables and `.bscript` examples. This checkout does not include the interpreter source or build instructions.

## Quick start

Open this folder in PowerShell and run the included example:

```powershell
.\scriptb.exe .\example.bscript
```

To run the starter program instead:

```powershell
.\main.bat
```

`main.bat` runs `main.bscript` from the project folder, even when launched from another directory. Both commands require the executable files included in this release.

## A first script

```text
print Hello, ScriptB!
repeat 3 print Hello again!
```

Save these lines in a file ending in `.bscript`, then pass its path to `scriptb.exe` as shown above. The `repeat` form shown here prints the message three times.

## Interactive mode

Start the interactive prompt with:

```powershell
.\scriptb.exe
```

At the prompt, use `runfile path\to\file.bscript` to run a script file.

## Documentation

- [Quick start](docs/quickstart.md)
- [Tutorial](docs/tutorial.md)
- [Language reference](docs/reference.md) (initial, incomplete)
- [Examples](docs/examples.md)
- [Roadmap](ROADMAP.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## Project links

- [ScriptB website](https://brndn-2026.github.io/scriptb-website/)
- [ScriptB IoT project](https://scriptb-iot.onrender.com/) (separate project)

The root-level `test.bscript` contains command probes, not a complete language specification. The reference documents only the syntax currently demonstrated in the shipped examples; more commands need verification and documentation.

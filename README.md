# ScriptB

ScriptB is a small, Python-based command language for beginners and hobbyists who want to try short scripts and simple automation without starting with a larger programming environment.

## Try it on Windows

This repository includes a Windows executable and a runnable example:

```powershell
git clone https://github.com/Brndn-2026/scriptb.git
cd scriptb
.\scriptb.exe .\example.bscript
```

The example prints a message, then repeats another message three times. To start the interactive prompt instead, run `.\scriptb.exe` with no file argument. The packaged executable is the verified quick-start here; other platforms are not confirmed.

## A first ScriptB program

```text
print Hello from ScriptB!
repeat 3 print Learning by repetition!
```

Save these lines as a `.bscript` file and pass its path to `scriptb.exe`.

## What it can do

The interpreter supports command-line scripts and an interactive prompt; printing, repeating commands, integer waits, and simple variables; one-line conditions and loops; date/time and basic file commands; and Python module or package operations. The source also contains an IoT integration.

ScriptB is an early, compact interpreter rather than a full-featured general-purpose language. Commands are split on whitespace, so quoted arguments and paths with spaces are not handled as a conventional shell would. Control-flow commands run a single command on one line, and their expressions use Python evaluation. Commands such as `eval`, `exec`, file operations, imports, and package installation can affect the machine running the interpreter: only run scripts you trust. Only the included Windows executable has been verified here; support for other platforms is unconfirmed.

## Documentation and project links

- [Quick start](docs/quickstart.md)
- [Language reference](docs/reference.md)
- [Tutorial](docs/tutorial.md)
- [Examples](docs/examples.md) and the runnable [example.bscript](example.bscript)
- [ScriptB website](https://brndn-2026.github.io/scriptb-website/)
- [GitHub releases](https://github.com/Brndn-2026/scriptb/releases)
- [Source repository](https://github.com/Brndn-2026/scriptb)

## Contributing

Bug reports and focused pull requests are welcome. Describe the behavior you observed, include a small `.bscript` reproduction when possible, and say how you verified a change. The repository does not currently have an automated test suite; avoid running `test.bscript` without inspecting it first, since it exercises commands that can have side effects.

## License

ScriptB is distributed under the [MIT License](LICENSE).

# ScriptB

ScriptB is a small scripting language with commands such as `print`, `wait`, and `repeat`. This release includes Windows executables and example `.bscript` programs.

## Try it

On Windows, open this folder in a terminal and run an included script:

```powershell
.\scriptb.exe .\example.bscript
```

Or run the starter program with:

```powershell
.\main.bat
```

`main.bat` runs `main.bscript` from the project folder, even if you launch it while your terminal is in another directory.

## Example

```text
print Hello, ScriptB!
wait 1
repeat 3 print Hello again!
```

Save the lines in a `.bscript` file, then pass its path to `scriptb.exe` as shown above.

## Interactive mode

Start the REPL with:

```powershell
.\scriptb.exe
```

Use `runfile path\to\file.bscript` in the REPL to run a script file.

## Project links

- [ScriptB website](https://brndn-2026.github.io/scriptb-website/)
- [ScriptB IoT project](https://scriptb-iot.onrender.com/)

The `test.bscript` file contains additional command examples. For the language reference and updates, see the project wiki.

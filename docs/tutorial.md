# A short tutorial

## 1. Write a script

Create a text file named `hello.bscript` with these lines:

```text
print Hello from ScriptB!
repeat 3 print This line repeats.
```

Each line is a command. `print` displays the words after the command, and `repeat` runs the following command the requested number of times.

## 2. Run it

From the folder containing `scriptb.exe` and `hello.bscript`, run this in PowerShell:

```powershell
.\scriptb.exe .\hello.bscript
```

You should see the greeting once and the second message three times.

## 3. Try the interactive prompt

Run the executable without a filename:

```powershell
.\scriptb.exe
```

At the `>>>` prompt, try `print hello`, then type `exit` to leave. You can run a saved script from the prompt with `runfile hello.bscript`.

The parser treats spaces as argument separators, and control flow is single-line rather than block-based. See the [reference](reference.md) for the available commands and limitations.

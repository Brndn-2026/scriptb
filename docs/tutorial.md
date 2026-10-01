# ScriptB Tutorial

This walkthrough builds a tiny script from the syntax demonstrated in this release.

## 1. Print a message

Create `greetings.bscript` and add:

```text
print Hello, ScriptB!
```

Run it from PowerShell in the project folder:

```powershell
.\scriptb.exe .\greetings.bscript
```

The interpreter prints `Hello, ScriptB!`.

## 2. Repeat an instruction

Add a repeat command on the next line:

```text
print Hello, ScriptB!
repeat 3 print Welcome back!
```

Run the file again. The first message prints once, then the second message prints three times. In this release's examples, the form is `repeat count command`.

## 3. Add a delay

The bundled examples also use `wait` with a number of seconds:

```text
print Starting
wait 1
print One second later
```

Run this separately to observe the delay. Timing details and error behavior are not yet specified.

## Where to go next

Try editing `main.bscript`, then run it with `main.bat` from the project folder.

```powershell
.\main.bat
```

See the [quick start](quickstart.md), [reference](reference.md), and [examples](examples.md).
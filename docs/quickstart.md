# ScriptB Quick Start

This guide uses the Windows executables included in this release.

## Run an included script

Open PowerShell in the ScriptB folder and run:

```powershell
.\scriptb.exe .\example.bscript
```

Expected output:

```text
This is an Example
```

## Run the starter program

Run the batch file:

```powershell
.\main.bat
```

It runs `main.bscript` and prints a welcome message followed by three greetings. The batch file switches to its own folder first, so it can also be launched from elsewhere.

## Write and run a script

Create a text file named `hello.bscript` in the project folder:

```text
print Hello, ScriptB!
repeat 3 print Hello again!
```

Run it with:

```powershell
.\scriptb.exe .\hello.bscript
```

The output is one greeting followed by `Hello again!` three times. See the [tutorial](tutorial.md) for a short walkthrough and the [reference](reference.md) for the currently documented syntax.
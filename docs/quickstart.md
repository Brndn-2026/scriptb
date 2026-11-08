# Quick start

## Run the included example on Windows

The repository includes `scriptb.exe` and `example.bscript`. In PowerShell, from the project directory:

```powershell
.\scriptb.exe .\example.bscript
```

To try the same steps after cloning:

```powershell
git clone https://github.com/Brndn-2026/scriptb.git
cd scriptb
.\scriptb.exe .\example.bscript
```

The example prints one message and repeats another three times. To start the interactive prompt, run `.\scriptb.exe` without a file path. At the `>>>` prompt, enter a command such as `print hello`, or use `runfile example.bscript` to run a script.

Only the included Windows executable has been verified for these instructions. Running the Python source directly or using another platform is not covered by this quick start.

For command details, see the [language reference](reference.md), [tutorial](tutorial.md), and [examples](examples.md).

# Examples

## Print and repeat

```text
print Hello from ScriptB!
repeat 3 print Learning by repetition!
```

This is also the content of the repository's [example.bscript](../example.bscript), which can be run with:

```powershell
.\scriptb.exe .\example.bscript
```

## Wait

```text
print Starting
wait 1
print One second later
```

`wait` accepts an integer number of seconds.

## Try the prompt

Start `scriptb.exe` without a script path, then enter:

```text
print hello
repeat 2 print again
```

The repository's `test.bscript` is a broader command exercise, not a no-side-effects beginner example. Inspect it before running because it can perform file and package operations.

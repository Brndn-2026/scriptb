# Contributing to ScriptB

Thanks for helping make ScriptB easier to learn and use. This checkout contains prebuilt Windows executables and sample scripts, but not the interpreter source or build instructions.

## Report a problem

When opening an issue in the project's source repository, include:

- Windows version and ScriptB executable name.
- The smallest `.bscript` file that reproduces the problem.
- The exact command used and the output you expected and received.
- Whether the problem also occurs with the included `example.bscript`.

Do not include passwords, access tokens, or other private data in examples or logs.

## Improve documentation or examples

Keep examples short and runnable with the shipped executables. Label behavior as unverified when it has not been reproduced, and avoid presenting `test.bscript` as a complete language specification.

## Interpreter changes

To contribute interpreter code, use the repository that contains the interpreter source. This release folder alone is not enough to build or modify the interpreter; include the source repository and its build/test instructions with any code change.
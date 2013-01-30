# Jardumpr 

## Usage

```
usage: jardumpr.py [-h] [--raw] jarfile [jarfile ...]

positional arguments:
  jarfile

optional arguments:
  -h, --help  show this help message and exit
  --raw
```

"--raw" outputs the jasmin-style disassembled bytecode. Without --raw,
you get a list of symbols (classes and methods) that are provided
by the package, or referenced by the package.

The tool accepts both .jar and .class files as input.

## Install instructions

- Have java configured

- Run "python buildit.py"


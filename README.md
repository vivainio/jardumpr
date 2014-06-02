# Jardumpr 

## Usage


```

usage: jardumpr.py [-h] [--raw] [--old OLD] [--new NEW] [--test]
                   [jarfile [jarfile ...]]

positional arguments:
  jarfile

optional arguments:
  -h, --help  show this help message and exit
  --raw       dump Jasmin style assembly
  --old OLD   old .jar/.apk file for comparison
  --new NEW   new .jar/.apk file for comparison
  --test      quick sanity test

```

"--raw" outputs the jasmin-style disassembled bytecode. Without --raw,
you get a list of symbols (classes and methods) that are provided
by the package, or referenced by the package.

The tool accepts both .jar and .class files as input.

## Install instructions

- Have java configured

- Run "python buildit.py"

- If you want to diff apk's, you need to have "apktool" in system path.
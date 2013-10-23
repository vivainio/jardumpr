#!/usr/bin/env python
import os, tempfile, zipfile, re, shutil, argparse, sys
import mglob
import subprocess
import tempfile

BINROOT = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))


def decompile(filelist):
    classpath = [
        BINROOT + "/bin",
        BINROOT + "/lib/*",
    ]

    #print classpath
    #assert all(map(os.path.exists, classpath))
    os.environ["CLASSPATH"] = ":".join(classpath)

    #out = os.popen("java JasminifierClassAdapter " +paths).read()
    out = subprocess.check_output(["java", "JasminifierClassAdapter"] + filelist)
    provides = re.findall("^.provide (.*)$", out, re.MULTILINE)
    depends = re.findall("^.dep (.*)$", out, re.MULTILINE)
    depclasses = set(el.split(';', 1)[0] for el in depends)
    provclasses = set(el.split(';', 1)[0] for el in provides)

    depclasses -= provclasses

    return {'provides': provides, 'depends': depclasses,
            'raw': out}

#print "deps", depclasses

tempdirs = []


def extract_jar(jarf):
    zf = zipfile.ZipFile(jarf, "r")
    td = tempfile.mkdtemp()
    tempdirs.append(td)
    zf.extractall(td)
    return mglob.expand("rec:" + td + "=*.class")


def dump_jar_data(jarf, outf):
    #decompile(['data/Local.class'])
    outf.write("# file: " + jarf + "\n")
    if jarf.lower().endswith("jar"):
        files = extract_jar(jarf)
        d = decompile(files)
    else:
        d = decompile([jarf])

    if args.raw:
        outf.write(d['raw'])
        return
    for k in sorted(set(d['provides'])):
        outf.write(k + "\n")

    outf.write("#\n# External references\n#\n")
    for k in sorted(d['depends']):
        outf.write(k + ";ref\n")


def parseargs():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("jarfiles", metavar="jarfile", nargs="*")
    parser.add_argument("--raw", action="store_true")
    parser.add_argument("--old", type=str)
    parser.add_argument("--new", type=str)
    parser.add_argument("--test", action="store_true")

    args = parser.parse_args()
    return args

def compare_dumps(da, db):
    os.system("diff " + da + " " + db + " | diffstat -m -f0")

def compare(a, b):
    args.raw = True
    af = tempfile.NamedTemporaryFile()
    dump_jar_data(a, af)
    bf = tempfile.NamedTemporaryFile()
    dump_jar_data(b, bf)

    #print af.name
    compare_dumps(af.name, bf.name)


def main():
    global args

    args = parseargs()
    if args.test:
        print "Minor change"
        compare("test/Original/LCDUITest.jar", "test/MinorChange/LCDUITest.jar")
        print "bigger change"
        compare("test/Original/LCDUITest.jar", "test/Change/LCDUITest.jar")
        return

    if args.old:
        compare(args.old, args.new)
        return

    jars = args.jarfiles
    #print "process",jars
    for j in jars:
        dump_jar_data(j, sys.stdout)

    for td in tempdirs:
        shutil.rmtree(td)


if __name__ == "__main__":
    main()
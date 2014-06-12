#!/usr/bin/env python
import os, tempfile, zipfile, re, shutil, argparse, sys
import mglob
import subprocess
import tempfile
import apklib

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
    try:
        out = subprocess.check_output(["java", "JasminifierClassAdapter"] + filelist)
    except subprocess.CalledProcessError:
        print "corrupt: " + repr(filelist)
        return

    provides = re.findall("^.provide (.*)$", out, re.MULTILINE)
    depends = re.findall("^.dep (.*)$", out, re.MULTILINE)
    depclasses = set(el.split(';', 1)[0] for el in depends)
    provclasses = set(el.split(';', 1)[0] for el in provides)

    depclasses -= provclasses

    return {'provides': provides, 'depends': depclasses,
            'raw': out}

#print "deps", depclasses

tempdirs = []

def c(s):
    return os.popen(s).read()


def extract_jar(jarf):
    try:
        zf = zipfile.ZipFile(jarf, "r")
    except zipfile.BadZipfile:
        print "corrupt: bad zip,",jarf
        raise
    td = tempfile.mkdtemp()
    tempdirs.append(td)
    try:
        zf.extractall(td)
    except:
        print "corrupt: bad zip",jarf

    return mglob.expand("rec:" + td + "=*.class")


def dump_jar_data(jarf, outf):
    #decompile(['data/Local.class'])
    # outf.write("# file: " + jarf + "\n")
    if jarf.lower().endswith("jar"):
        files = extract_jar(jarf)
        d = decompile(files)
    else:
        d = decompile([jarf])

    if not d:
        # error, don't write anything
        return

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
    parser.add_argument("--raw", action="store_true", help='dump Jasmin style assembly')
    parser.add_argument("--old", type=str, help="old .jar/.apk file for comparison")
    parser.add_argument("--new", type=str, help="new .jar/.apk file for comparison")
    parser.add_argument("--test", action="store_true", help="quick sanity test")

    args = parser.parse_args()
    return args

def parse_diffstat(s):
    if not s.strip():
        return 0
    return int(s.split("|")[1].split()[0])



def compare_dumps(da, db):
    #out = c("diff " + da + " " + db)
    #print out
    out = c("diff " + da + " " + db + " | diffstat -m -f0 -q")
    r = parse_diffstat(out)
    #print out
    lc = open(da).read().count("\n")
    if not lc:
        print "corrupt: no output"
        return

    print "changes:",r
    print "linecount:",lc
    print "per_1k:",(r/float(lc)) * 1000

def compare_apk(a,b):
    aa = apklib.Apk(a)
    bb = apklib.Apk(b)
    af = aa.extract("a")
    bf = bb.extract("b")
    compare_dumps(af, bf)

    apklib.delete_temp_files()


def compare(a, b):
    args.raw = True
    af = tempfile.NamedTemporaryFile(delete=True)
    try:
        dump_jar_data(a, af)
    except Exception,e:
        print "corrupt: old, %s, %s" % (a, e.message)
        return
    bf = tempfile.NamedTemporaryFile(delete=True)

    try:
        dump_jar_data(b, bf)
    except Exception,e:
        print "corrupt: new, %s, %s" % (b, e.message)
        return

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
        if args.old.endswith(".apk"):
            compare_apk(args.old, args.new)
            return
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
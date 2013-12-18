__author__ = 'vivainio'

import os,tempfile
import subprocess


apktool = "/usr/local/bin/apktool"

tempdir = tempfile.mkdtemp()


def c(args):
    print ">",args
    subprocess.check_call(args)


def cat(outf, filenames):
    with open(outf, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(os.path.basename(fname))
                outfile.write(infile.read())

def find(pth, endswith):
    files = []
    for dirpath, dirnames, filenames in os.walk(pth):
        for fname in filenames:
            if fname.endswith(endswith):
                path = os.path.join(dirpath,fname)
                #assert path.startswith(pth)
                files.append(path)

    return files

class Apk:
    def __init__(self, fn):
        self.fn = os.path.abspath(fn)
        assert os.path.isfile(fn)

    def extract(self):
        tgt = tempdir + "/1"
        c([apktool, "d", self.fn, tgt])
        smalis = sorted(find(tgt + "/smali/", ".smali"))
        alls = tempdir + "/all.smali"
        cat(alls, smalis)
        assert os.path.isfile(alls)

        return alls

        #smalis = tgt + ""
        #c("ls " + td)


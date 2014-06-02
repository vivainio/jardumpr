__author__ = 'vivainio'

import os,tempfile,pprint
import subprocess


#apktool = "/usr/local/bin/apktool"

apktool = "apktool"


tempdir = tempfile.mkdtemp()


def c(args):
    #print ">",args
    out = subprocess.check_output(args, stderr=subprocess.STDOUT)


def cat(outf, filenames):
    with open(outf, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:

                outfile.write("# " + os.path.basename(fname) + "\n\n")
                lines = infile.readlines()
                olines = [l for l in lines if not l.lstrip().startswith(".line")]

                outfile.writelines(olines)

def find(pth, endswith):
    files = []
    for dirpath, dirnames, filenames in os.walk(pth):
        for fname in filenames:
            if fname.endswith(endswith):
                path = os.path.join(dirpath,fname)
                #assert path.startswith(pth)
                files.append(path)

    return files


wellknown = ("/smali/android", "/smali/com/google")


class Apk:
    def __init__(self, fn):
        self.fn = os.path.abspath(fn)
        assert os.path.isfile(fn)

    def extract(self, tag = "1"):
        """
        tag must be valid directory name
        """

        tgt = tempdir + "/" + tag

        try:
            c([apktool, "d", self.fn, tgt])
        except subprocess.CalledProcessError,e:
            print "corrupt: apktool, %s" % (e.message)


        def any_in(ss, s):
            for el in ss:
                if el in s:
                    return True
            return False


        smalis = sorted([ent for ent in find(tgt + "/smali/", ".smali") if not any_in(wellknown, ent)])
        #pprint.pprint(smalis)
        alls = tgt + "/all.smali"
        cat(alls, smalis)
        assert os.path.isfile(alls)

        return alls

        #smalis = tgt + ""
        #c("ls " + td)


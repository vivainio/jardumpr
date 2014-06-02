__author__ = 'vivainio'

import unittest, os
import tempfile

from subprocess import Popen, PIPE
import apklib
import glob

def c(s, noerr = False):
    #print s

    p = Popen(s, shell=True, stdout=PIPE, stderr=PIPE)
    o,e = p.stdout.read(), p.stderr.read()
    if e and not noerr:
        print "// stderr"
        print e
        print "//"
    return o

def one(gpat):
    fs = glob.glob(gpat)
    assert len(fs) == 1
    return fs[0]

class TestApkLib(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        pass

    def test_create(self):
        a = apklib.Apk("test/apk/leoreader.apk")

    #@unittest.skip("expensive")
    def test_extract(self):
        a = apklib.Apk(one("test/apk/1/*.apk"))
        f1 = a.extract()
        print f1

    #@unittest.skip("expensive")
    def test_diff(self):
        a = apklib.Apk(one("test/apk/1/*.apk"))
        b = apklib.Apk(one("test/apk/2/*.apk"))
        asmali = a.extract("a")
        bsmali = b.extract("b")
        #os.system("diff " + asmali + " " + bsmali)


    def test_find(self):
        r  = apklib.find("/usr/bin/", "")
        #print r
        self.assert_(r > 0)

    #@unittest.skip("expensive")
    def test_extcall(self):
        #os.system('python -c "import sys; print sys.path"')
        out = c("python jardumpr.py --old=%s --new=%s" % (
            one("test/apk/1/*.apk"),
            one("test/apk/2/*.apk")))
        #print out

    def test_corrupt(self):
        out = c("python jardumpr.py --old=%s --new=%s" % (
            one("test/apk/1/*.apk"),
            "test/apk/corrupt/empty.apk"))
        print out
        if not 'corrupt:' in out:
            print "Wanted corrupt, got",out
            self.assert_('corrupt:' in out)

if __name__ == "__main__":
    unittest.main()
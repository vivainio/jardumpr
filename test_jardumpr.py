import unittest, os
import glob
from subprocess import Popen, PIPE

def c(s, noerr = False):
    #print s

    p = Popen(s, shell=True, stdout=PIPE, stderr=PIPE)
    o,e = p.stdout.read(), p.stderr.read()
    if e and not noerr:
        print "// stderr"
        print e
        print "//"
    return o

class TestJardumpr(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        pass

    def test_dump(self):
        out = c("python jardumpr.py test/Original/LCDUITest.jar")
        self.assert_(len(out) > 500)
        #print len(out)

    def test_raw_dump(self):
        out = c("python jardumpr.py --raw test/Original/LCDUITest.jar")
        #print len(out)
        self.assert_(len(out) > 10000)

    def test_compare(self):
        out = c("python jardumpr.py --old=test/Original/LCDUITest.jar --new=test/MinorChange/LCDUITest.jar")
        #print out
        [self.assert_(s in out) for s in ['changes', 'linecount', 'per_1k']]
        #self.assert_(len(out) > 10000)

    def test_compare_same(self):
        out = c("python jardumpr.py --old=test/Original/LCDUITest.jar --new=test/Original/LCDUITest.jar")
        self.assert_('changes: 0' in out)

    def test_compare_rename(self):
        out = c("python jardumpr.py --old=test/Original/LCDUITest.jar --new=test/Original/LCDUITest_newname.jar")
        self.assert_('changes: 0' in out)

        #print out


    def test_sshout(self):
        out = c("python jardumpr.py --old=test/StatusShoutBins/0.9/StatusShout.jar --new=test/StatusShoutBins/1.0/StatusShout.jar")
        #print out
        out = c("python jardumpr.py --old=test/StatusShoutBins/1.0/StatusShout.jar --new=test/StatusShoutBins/1.1/StatusShout.jar")
        #print out
    def test_corrupt(self):
        for f in glob.glob("test/Corrupt/*"):
            out = c("python jardumpr.py %s" % f, noerr=True)
            if not 'corrupt:' in out:
                print "Wanted corrupt, got",out
                self.assert_('corrupt:' in out)

    def test_compare_corrupt(self):
        for f in glob.glob("test/Corrupt/*"):


            out = c("python jardumpr.py --old=test/Original/LCDUITest.jar --new=%s" % f, noerr=True)
            if not 'corrupt:' in out:
                print "Problematic output:",out
            self.assert_('corrupt:' in out)
            out = c("python jardumpr.py --old=%s --new=test/MinorChange/LCDUITest.jar" % f, noerr=True)


if __name__ == "__main__":
    unittest.main()
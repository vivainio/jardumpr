import unittest, os

def c(s):
    return os.popen(s).read()

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
        out = c(" python jardumpr.py --old=test/Original/LCDUITest.jar --new=test/MinorChange/LCDUITest.jar")
        #print out
        [self.assert_(s in out) for s in ['changes', 'linecount', 'per_1k']]
        #self.assert_(len(out) > 10000)

    def test_compare_same(self):
        out = c(" python jardumpr.py --old=test/Original/LCDUITest.jar --new=test/Original/LCDUITest.jar")
        print out

    def test_sshout(self):
        out = c(" python jardumpr.py --old=test/StatusShoutBins/0.9/StatusShout.jar --new=test/StatusShoutBins/1.0/StatusShout.jar")
        print out
        out = c(" python jardumpr.py --old=test/StatusShoutBins/1.0/StatusShout.jar --new=test/StatusShoutBins/1.1/StatusShout.jar")
        print out
if __name__ == "__main__":
    unittest.main()
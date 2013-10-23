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
        [self.assert_(ch in out) for ch in ['-', '+', '!']]
        #self.assert_(len(out) > 10000)


if __name__ == "__main__":
    unittest.main()
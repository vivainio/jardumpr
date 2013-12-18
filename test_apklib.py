__author__ = 'vivainio'

import unittest, os
import tempfile

import apklib

class TestApkLib(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        pass

    def test_create(self):
        a = apklib.Apk("test/apk/leoreader.apk")

    #@unittest.skip("expensive")
    def test_extract(self):
        a = apklib.Apk("test/apk/leoreader.apk")
        f1 = a.extract()
        print f1

    def test_find(self):
        r  = apklib.find("/usr/bin/", "")
        #print r
        self.assert_(r > 0)




if __name__ == "__main__":
    unittest.main()
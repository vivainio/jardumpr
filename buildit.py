import os


def c(s):
    print ">", s
    os.system(s)


os.environ["CLASSPATH"] = "lib/*"
c("javac -d bin/ src/*.java")

print "Done! To create a global symlink do:"
print "sudo ln -s %s /usr/local/bin/jardumpr" % os.path.abspath("./jardumpr.py")
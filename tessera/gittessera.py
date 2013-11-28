from gittle import Gittle
from tessara import Tessara

class GitTessera:


    def __init__(self):
        self.gitdir = "."
        self.git = Gittle(self.gitdir)
        Tessera._tesserae = "%s/.tesserae"  %self.gitdir


    def init(self, args = []):
        if len(args) != 0:
        return False

        if os.path.exists(Tessera._tesserae):
        return False
        os.mkdir(Tessera._tesserae)

        files = []
        t = "%s/template" % Tessera._tesserae
        shutil.copyfile("%s/template" % os.path.dirname(os.path.realpath(__file__)), t)
        files.append(t)

        t = "%s/status" % Tessera._tesserae
        shutil.copyfile("%s/status" % os.path.dirname(os.path.realpath(__file__)), t)
        files.append(t)

        return self.git_add(files, "tessera: initialized")


    def ls(self, args = []):
        # FIXME: check args
        if not os.path.exists(Tessera._tesserae):
            return False

        contents = [ Tessera._tesserae + "/" + x for x in os.listdir(Tessera._tesserae) if stat.S_ISDIR(os.lstat(Tessera._tesserae + "/" + x).st_mode)]
        sorted(contents, cmp = cmp_tessera)
        tesserae = []
        for tessera_path in contents:
            tesserae.append(Tessera(tessera_path))
        return tesserae

def cmp_tessera(a, b):
  aa = os.lstat("%s/tessera"%a)
  bb = os.lstat("%s/tessera"%b)
  return aa.st_mtime < bb.st_mtime


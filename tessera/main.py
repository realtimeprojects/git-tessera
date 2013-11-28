#!/usr/bin/env python

from sys import argv, stdin, stdout, stderr, exit
from subprocess import check_output, Popen
import os
import shutil
import stat
import re
from gittle import Gittle
from uuid import uuid1

from colorful import colorful

def cmp_tessera(a, b):
  aa = os.lstat("%s/tessera"%a)
  bb = os.lstat("%s/tessera"%b)
  return aa.st_mtime < bb.st_mtime

class Tessera:
  _tesserae = None
  _status = []

  def __init__(self, tessera_path):
    self.tessera_path = tessera_path
    self.filename = "%s/tessera"%tessera_path
    self.title = None
    self.status = None
    self._read()
    self._parse()

    if not Tessera._status:
      status_file = "%s/status"%Tessera._tesserae
      if os.path.exists(status_file): # FIXME: else set _status False and dont come back
        f = open(status_file, 'r')
        for line in f.readlines():
          line = line.strip()
          if line:
            a = re.split(r'[ \t]+', line)
            if len(a) != 2:
              print "invalid status line: %s"%line
              break
            Tessera._status.append( ( a[0], a[1] ) )
        f.close()


  def _read(self):
    if not os.path.exists(self.filename):
      stderr.write("tessera file not found: %s\n"%self.fielname)
      return None

    f = open(self.filename, 'r')
    self.body = f.read().split('\n')
    f.close()

  def _parse(self):
    self.title = "no title"
    for i in range(len(self.body)):
      if self.body[i].startswith("# "):
        self.title = self.body[i][2:].strip()
        self.body.pop(i)
        break

    self.status = "no status"
    for i in range(len(self.body)):
      if self.body[i].startswith("@status "):
        self.status = self.body[i][8:].strip()
        self.body.pop(i)
        break

  def summary(self):
    l = len(self.title)
    color = None
    for s in Tessera._status:
      if s[0] == self.status:
        color = s[1]
        break
    status = self.status
    if color:
      if hasattr(colorful, color):
        f = getattr(colorful, color)
        status = f(self.status)
    return "%s %s %s %s"%(self.get_ident_short(), colorful.bold_white(self.title), " " * (40 - l), status)

  def get_ident(self ):
    return os.path.basename(self.tessera_path)

  def get_ident_short(self):
    return self.get_ident().split('-')[0]

  def get_body(self):
    return '\n'.join(self.body)


class GitTessera:

  def __init__(self):
    self.gitdir = "."
    self.git = Gittle(self.gitdir)
    Tessera._tesserae = "%s/.tesserae"%self.gitdir


  def cmd_init(self, args):
    if len(args) != 0:
      stderr.write("git tessera init takes no arguments\n")
      return False

    #if self.git.is_dirty():
      #stderr.write("repo is dirty\n")
      #return False

    if os.path.exists(Tessera._tesserae):
      stderr.write("git tesserae directory already exists: %s\n"%Tessera._tesserae)
      return False
    os.mkdir(Tessera._tesserae)

    files = []
    t = "%s/template"%Tessera._tesserae
    shutil.copyfile("%s/template"%os.path.dirname(os.path.realpath(__file__)), t)
    files.append(t)

    t = "%s/status"%Tessera._tesserae
    shutil.copyfile("%s/status"%os.path.dirname(os.path.realpath(__file__)), t)
    files.append(t)

    self.git_add(files, "tessera: initialized")
    return True


  def cmd_ls(self, args):
    # FIXME: check args
    if not os.path.exists(Tessera._tesserae):
      stderr.write("git tesserae directory does not exist\n")
      return False

    contents = [ Tessera._tesserae + "/" + x for x in os.listdir(Tessera._tesserae) if stat.S_ISDIR(os.lstat(Tessera._tesserae + "/" + x).st_mode)]
    sorted(contents, cmp = cmp_tessera)
    for tessera_path in contents:
      t = Tessera(tessera_path)
      print t.summary()
    return True


  def cmd_show(self, args):
    if len(args) != 1:
      stderr.write("git tessera show takes identifier as argument\n")
      return False

    key = args[0]
    tessera_file = None
    for i in os.listdir(Tessera._tesserae):
      tessera_path = "%s/%s"%(Tessera._tesserae, i)
      if not stat.S_ISDIR(os.lstat(tessera_path).st_mode):
        continue
      if i.split('-')[0] == key or i == key:
        break
    if not tessera_path:
      stderr.write("git tessera %s not found\n"%key)
      return False

    t = Tessera(tessera_path)
    short = t.summary()
    length = len(short)
    print "=" * length
    print short
    print "=" * length
    print t.get_body()
    return True


  def cmd_edit(self, args):
    if len(args) < 1:
      stderr.write("git tessera edit takes one or more identifier as argument\n")
      return False

    #if self.git.is_dirty():
      #stderr.write("repo is dirty\n")
      #return False

    tessera_paths = []
    for key in args:
      tessera_path = None
      found = False
      for i in os.listdir(Tessera._tesserae):
        tessera_path = "%s/%s"%(Tessera._tesserae, i)
        if not stat.S_ISDIR(os.lstat(tessera_path).st_mode):
          continue
        if i.split('-')[0] == key or i == key:
          found = True
          break
      if not found:
        stder.write("git tessera %s not found\n"%key)
        return False

      tessera_paths.append(tessera_path)

    tessera_files = [ "%s/tessera"%x for x in tessera_paths ]
    p = Popen( ["sensible-editor"] + tessera_files )
    p.communicate( )
    p.wait()

    #if self.git.is_dirty():
    for tessera_path in tessera_paths:
      t = Tessera(tessera_path)
      self.git_add(["%s/tessera"%tessera_path], "tessera updated: %s"%t.title)
    return True

  def cmd_create(self, args):
    if len(args) < 1:
      stderr.write("git tessera create needs arguments\n")
      return False

    #if self.git.is_dirty():
    #  stderr.write("repo is dirty\n")
    #  return False

    if args:
      title = " ".join(args)
    else:
      title = "tessera title goes here"
    uuid = uuid1()
    tessera_path = "%s/%s"%(Tessera._tesserae, uuid)
    tessera_file = "%s/tessera"%tessera_path
    os.mkdir(tessera_path)
    fin = open("%s/template"%Tessera._tesserae, "r")
    fout = open(tessera_file, "w")
    for line in fin.readlines( ):
      if line == "@title@\n":
        line = "# %s\n"%title
      fout.write(line)
    fin.close()
    fout.close()

    p = Popen( ["sensible-editor", tessera_file])
    p.communicate( )
    p.wait()

    t = Tessera(tessera_path)
    self.git_add([tessera_file], "tessera created: %s"%t.title)
    return True

  def cmd_remove(self, args):
    if len(args) != 1:
      stderr.write("git tessera remove takes identifier as argument\n")
      return False

    #if self.git.is_dirty():
      #stderr.write("repo is dirty\n")
      #return False

    key = args[0]
    tessera_file = None
    tessera_path = None
    for i in os.listdir(Tessera._tesserae):
      tessera_path = "%s/%s"%(Tessera._tesserae, i)
      if not stat.S_ISDIR(os.lstat(tessera_path).st_mode):
        continue
      if i.split('-')[0] == key or i == key:
        tessera_file = "%s/tessera"%tessera_path
        break
    if not tessera_file:
      stderr.write("git tessera %s not found\n"%key)
      return False

    t = Tessera(tessera_path)
    stdout.write("remove tessera %s: %s ? [Y/n] "%(key, t.title))
    try:
      answer = stdin.readline().strip()
    except KeyboardInterrupt:
      return False
    if not answer or answer.lower() == "y":
      files = [ "%s/%s"%(tessera_path, x) for x in os.listdir(tessera_path)]
      self.git_rm(files, "tessera removed: %s"%t.title)

      from shutil import rmtree
      rmtree(tessera_path)


  def git_add(self, files, message):
    self.git.stage(files)
    self.git.commit(message=message)

  def git_rm(self, files, message):
    self.git.rm(files)
    self.git.commit(message=message)

def main():
  cmd = "ls"
  if len(argv) > 1:
    cmd = argv[1]

  #try:
  t = GitTessera()
  #except git.exc.InvalidGitRepositoryError:
    #stderr.write("not a git repo\n")
    #exit(1)
  if hasattr(t, "cmd_%s"%cmd):
    if not getattr(t, "cmd_%s"%cmd)(argv[2:]):
      exit( 1 )
    exit( 0 )
  else:
    stderr.write("unknown command: %s\n"%cmd)
    exit(2)

if __name__ == "__main__":
    main()

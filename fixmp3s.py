import sys, os, inspect, time, re

from os import walk
from subprocess import call

def fix():
  base_path = os.getcwd()
  path = base_path# + "/eminem - marshall mathers LP"
  for (dirpath, dirnames, filenames) in walk(path):
    path_printed = False
    best_match = match_start(filenames)
    if best_match:
      mp3s, best_match = best_match
      if not re.match(r'.*[a-zA-Z].*', best_match):
        continue
      if best_match[-1] == "0":
        best_match = best_match[:-1]
      if not best_match:
        continue
      print dirpath
      print best_match
      triml = len(best_match)
            
      for fname in mp3s:
        new_name = fname[triml:]
        print "%s -> %s" % (fname, new_name)
        call(["mv", dirpath + "/" + fname, dirpath + "/" + new_name])

    second_best = get_second_match(filenames)
    if second_best:
      mp3s, best_match = second_best
      if not re.match(r'.*[a-zA-Z].*', best_match):
        continue
      if not best_match:
        continue
      print dirpath
      best_match = re.sub(r'\(', r'\(', best_match)
      print best_match
            
      for fname in mp3s:
        new_name = re.sub(r'([0-9]{2})'+best_match+r'(.*)', r'\1 \2', fname)
        new_name = re.sub(r'\s+', r' ', new_name)
        print "%s -> %s" % (fname, new_name)
        call(["mv", dirpath + "/" + fname, dirpath + "/" + new_name])


#eg "01 - Artist Name - Track.mp3
def get_second_match(filenames):
  first = None
  best_match = ""
  mp3s = []
  for fname in filenames:
    if fname[-3:] != "mp3":
      continue
    if not re.match(r'^[0-9]{2}.*', fname):
      return False
    mp3s.append(fname)
    without_number = re.sub(r'^[0-9]{2}', '', fname)
    if not first:
      first = without_number
    else:
      best_match = get_best_match(first, best_match, without_number)
      if not best_match:
        return None
  if best_match:
    return mp3s, best_match
      

# eg "Artist Name - 01 - Track Title.mp3
def match_start(filenames):
    first = None
    best_match = ""
    mp3s = []
    for fname in filenames:
      if fname[-3:] != "mp3":
        continue
      mp3s.append(fname)
      if not first:
        first = fname
      else:
        best_match = get_best_match(first, best_match, fname)
        if not best_match:
          return None
    if best_match:
      return mp3s, best_match
  

def get_best_match(first, best_match, fname):
  for i, l in enumerate(fname):
    if i < len(first) and l != first[i]:
      match = fname[:i]
      if not best_match or not match or len(match) < len(best_match):
        best_match = match
        if not match:
          return None
      break
  return best_match


fix()
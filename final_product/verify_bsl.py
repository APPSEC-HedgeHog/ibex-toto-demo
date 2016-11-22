import sys
import json

if __name__ == '__main__':
  c = open('allowed_committers.json', 'r')
  data = c.read()
  c.close()
  committers = json.loads(data)
  f =  open('bsl.json', 'r')
  data = f.read()
  f.close()
  data = json.loads(data)
  for idx, i in enumerate(data):
    r = json.loads(i)
    if r['committer_name'] not in committers['allowed_committers']:
      print('ERROR: Committer name {} for commit {} is not in an allowed committer'
            .format(r['committer_name'], idx))
      sys.exit(1)
  print('All commiters verification passed')
  sys.exit(0)

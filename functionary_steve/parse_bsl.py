from git import Repo

repo = Repo('.')
commits = list(repo.iter_commits('bsl'))

f = open('bsl.log', 'w')
for i in commits:
  f.write('===\n\n\n')
  f.write(str(i.hexsha + '\n'))
  f.write(str(i.author.name + '\n'))
  f.write(str(i.committer.name) + '\n')
  f.write(str(i.authored_date) + '\n')
  f.write(str(i.committed_date) + '\n')
  f.write(str(i.message) + '\n')
  f.write(str(i.tree.blobs[0].data_stream.read()))
  f.write('===\n\n\n')

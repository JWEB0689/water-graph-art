import os
import subprocess
from datetime import datetime, timedelta
import random

# Re-init repository safely
subprocess.run(['rm', '-rf', '.git'])
subprocess.run(['git', 'init'])
subprocess.run(['git', 'config', 'gc.auto', '0'])

tree_proc = subprocess.run(['git', 'write-tree'], capture_output=True, text=True, check=True)
tree = tree_proc.stdout.strip()

start_date = datetime.now().replace(hour=12, minute=0, second=0) - timedelta(days=365)
date_str = start_date.strftime("%Y-%m-%dT12:00:00 %z")

env = os.environ.copy()
env['GIT_AUTHOR_NAME'] = 'Jeremy Weber'
env['GIT_AUTHOR_EMAIL'] = 'jeremyweber@Jeremys-MacBook-Pro.local'
env['GIT_COMMITTER_NAME'] = 'Jeremy Weber'
env['GIT_COMMITTER_EMAIL'] = 'jeremyweber@Jeremys-MacBook-Pro.local'
env['GIT_AUTHOR_DATE'] = date_str
env['GIT_COMMITTER_DATE'] = date_str

commit_proc = subprocess.run(['git', 'commit-tree', tree, '-m', 'Initial commit'], env=env, capture_output=True, text=True, check=True)
current_commit = commit_proc.stdout.strip()
subprocess.run(['git', 'update-ref', 'refs/heads/master', current_commit])

total = 0
grid = [[0 for _ in range(7)] for _ in range(53)]

# Generate Rain Drops in Grid (Matrix style)
# Rain is heavy at the bottom of the drop, lighter at the top
for _ in range(70): 
    x = random.randint(0, 52)
    y_start = random.randint(-4, 6)
    length = random.randint(3, 7)
    for j in range(length):
        y = y_start + j
        if 0 <= y < 7:
            # intensity increases as j increases (bottom of drop is heaviest)
            intensity = int(((j + 1) / length) * 12)
            grid[x][y] += intensity

for days_ago in range(364, -1, -1):
    d = datetime.now().replace(hour=12, minute=0, second=0) - timedelta(days=days_ago)
    date_str = d.strftime("%Y-%m-%dT12:00:00 %z")
    
    x = 52 - (days_ago // 7)
    if x > 52: x = 52
    y = days_ago % 7
    
    commits = grid[x][y]
    if commits > 25: commits = 25
    
    if commits > 0:
        for _ in range(commits):
            env['GIT_AUTHOR_DATE'] = date_str
            env['GIT_COMMITTER_DATE'] = date_str
            proc = subprocess.run(['git', 'commit-tree', tree, '-p', current_commit, '-m', 'rain'], env=env, capture_output=True, text=True)
            current_commit = proc.stdout.strip()
            total += 1

subprocess.run(['git', 'update-ref', 'refs/heads/master', current_commit])
subprocess.run(['git', 'gc', '--prune=now'])
print(f"Generated {total} commits via python commit-tree.")

import math
import os
from datetime import datetime, timedelta
import subprocess

today = datetime.now().replace(hour=12, minute=0, second=0)
env = os.environ.copy()

# Git should already be initialized


total_commits = 0
for days_ago in range(365):
    date = today - timedelta(days=days_ago)
    y = (date.weekday() + 1) % 7
    weeks_ago = days_ago // 7
    x = 51 - weeks_ago
    
    # Interference pattern with two drops
    d1 = math.sqrt((x - 15)**2 + (y - 3)**2)
    d2 = math.sqrt((x - 40)**2 + (y - 3)**2)
    
    v1 = math.sin(d1 * 0.8)
    v2 = math.sin(d2 * 0.8)
    v = (v1 + v2) / 2
    
    commits = int(((v + 1) / 2) * 15)
    
    date_str = date.strftime('%Y-%m-%dT%H:%M:%S')
    env['GIT_AUTHOR_DATE'] = date_str
    env['GIT_COMMITTER_DATE'] = date_str
    
    for _ in range(commits):
        subprocess.run(
            ['git', 'commit', '--allow-empty', '-m', 'ripple'],
            env=env,
            stdout=subprocess.DEVNULL
        )
        total_commits += 1

print(f"Generated {total_commits} commits.")

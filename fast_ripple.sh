#!/bin/bash
rm -rf .git
git init
git config gc.auto 0

TREE=$(git write-tree)
export GIT_AUTHOR_NAME="Jeremy Weber"
export GIT_AUTHOR_EMAIL="jeremyweber@Jeremys-MacBook-Pro.local"
export GIT_COMMITTER_NAME="Jeremy Weber"
export GIT_COMMITTER_EMAIL="jeremyweber@Jeremys-MacBook-Pro.local"

# Initial commit
d=$(date -v-365d "+%Y-%m-%dT12:00:00 %z")
export GIT_AUTHOR_DATE="$d"
export GIT_COMMITTER_DATE="$d"
COMMIT=$(git commit-tree $TREE -m "Initial commit")
git update-ref refs/heads/master $COMMIT

git remote add origin https://github.com/JWEB0689/water-graph-art.git
# Push manually after the script runs using standard git credentials
echo "Done. Run 'git push origin master --force' to update."

total=0
for (( days_ago=364; days_ago>=0; days_ago-- )); do
    d=$(date -v-${days_ago}d "+%Y-%m-%dT12:00:00 %z")
    
    # Calculate ripple pattern using bash math
    # x = 52 - days_ago/7
    # y = days_ago % 7
    # To make concentric ripples, we vary intensity based on distance from center (26, 3)
    x=$(( 52 - days_ago/7 ))
    y=$(( days_ago % 7 ))
    
    dx=$(( x - 26 ))
    dy=$(( y - 3 ))
    
    # distance squared
    dist_sq=$(( dx*dx + dy*dy ))
    
    # We can use modulo to simulate sine wave ripples (concentric rings)
    # A ring occurs every 20 units of dist_sq roughly
    ring=$(( dist_sq % 25 ))
    
    commits=0
    if [ $ring -lt 5 ]; then commits=12;
    elif [ $ring -lt 10 ]; then commits=8;
    elif [ $ring -lt 15 ]; then commits=4;
    elif [ $ring -lt 20 ]; then commits=1;
    fi
    
    for ((i=0; i<commits; i++)); do
        export GIT_AUTHOR_DATE="$d"
        export GIT_COMMITTER_DATE="$d"
        COMMIT=$(git commit-tree $TREE -p $COMMIT -m "ripple")
        total=$((total+1))
    done
done

git update-ref refs/heads/master $COMMIT
echo "Generated $total commits via commit-tree."

git gc --prune=now
git push -u origin master --force

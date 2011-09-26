import userconfig
from collections import deque

targets = []

pending_targets = [userconfig.main_target]

while len(pending_targets) != 0:
    t = pending_targets[0];
    pending_targets.remove(t)
    try:
        for i in t["depends"]:
            pending_targets.insert(0, i)
    except KeyError:
        pass
    if targets.count(t) != 0:
        targets.remove(t)
    targets.append(t)

targets.reverse()

from typing import List


def minNumberOperations(self, target: List[int]) -> int:
    incr = target[0]
    for i in range(len(target) - 1):
        if target[i] < target[i + 1]:
            incr += target[i + 1] - target[i]
    return incr

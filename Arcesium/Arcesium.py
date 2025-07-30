'''
There is a bug bash going on within a dev team.
Each engineer is fixing bugs by submitting bug fixes as commits.
There is a leaderboard for number of commits been submitted.
If the bug fix is correct, engineer earns 10 points.
If the bug fix is incorrect, engineer loses 10 points.
Build an in-memory tool that will:
1. Add Points to an Engineer.
2. Remove Points to an Engineer.
3. Get the top K Engineers in terms of points.
'''
import heapq
from collections import defaultdict
import threading
import time

class Solution:

    def __init__(self, pointsToIncrease, pointsToDecrease):
        self.pointsToIncrease = pointsToIncrease
        self.pointsToDecrease = pointsToDecrease
        self.heap = []
        self.pointsMap = defaultdict(int)
        self.lock = threading.Lock()

    def increasePoint(self, engineer):
        time.sleep(1)
        self.lock.acquire()
        print("Increasing for engineer", engineer)
        self.pointsMap[engineer] = self.pointsMap.get(engineer, 0) + self.pointsToIncrease
        self.lock.release()

    def decreasePoint(self, engineer):
        self.lock.acquire()
        print("Decreaing for engineer", engineer)

        self.pointsMap[engineer] = self.pointsMap.get(engineer, 0) - self.pointsToDecrease
        self.lock.release()

    def updateHeap(self):
        self.heap = []

        for engineer, points in self.pointsMap.items():
            heapq.heappush(self.heap, (-1 * points, engineer))

    def queryTopK(self, k):
        self.updateHeap()
        size = len(self.heap)
        i = 0
        result = []
        while i < size and i < k:
            points, engineer = heapq.heappop(self.heap)
            i += 1
            result.append((engineer, points))
            print("Engineer", engineer, "ranked", i)
        return result


solution = Solution(10, 10)

threads = []
i = 0
threads.append(threading.Thread(target=solution.increasePoint(i + 1), args=()))
threads.append(threading.Thread(target=solution.decreasePoint(i+11), args=()))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
#
# solution.increasePoint(8)
# solution.increasePoint(9)
# solution.increasePoint(10)
# solution.decreasePoint(6)
# solution.decreasePoint(6)
# solution.decreasePoint(6)

solution.queryTopK(100)

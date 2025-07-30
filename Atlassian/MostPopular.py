from collections import defaultdict


class MostPopular:
    def __init__(self):
        self.contentMap = defaultdict(int)
        self.mostPopularStack = []
        self.topPopularity = 0
        self.topPopularContent = None

    def mostPopular(self):
        if not self.mostPopularStack:
            return -1
        contentId, popularity = self.mostPopularStack[-1]
        if popularity == 0:
            return -1
        return contentId

    def increasePopularity(self, contentId):
        self.contentMap[contentId] = self.contentMap.get(contentId, 0) + 1
        popularity = self.contentMap[contentId]
        
        # If this content is now more popular than current top
        if popularity > self.topPopularity:
            self.mostPopularStack.append((contentId, popularity))
            self.topPopularity = popularity
            self.topPopularContent = contentId
        # If this content is now equally popular as current top
        elif popularity == self.topPopularity:
            self.mostPopularStack.append((contentId, popularity))

    def decreasePopularity(self, contentId):
        if contentId not in self.contentMap:
            return
            
        self.contentMap[contentId] -= 1
        popularity = self.contentMap[contentId]
        
        # If this was the most popular content
        if contentId == self.topPopularContent:
            # Remove it from stack
            while self.mostPopularStack and self.mostPopularStack[-1][0] == contentId:
                self.mostPopularStack.pop()
            
            # Update top popularity if stack is not empty
            if self.mostPopularStack:
                self.topPopularContent, self.topPopularity = self.mostPopularStack[-1]
            else:
                self.topPopularity = 0
                self.topPopularContent = None
        
        # If popularity became 0, remove from map
        if popularity == 0:
            del self.contentMap[contentId]

popularityTracker = MostPopular()
print("\nTest Case 1: Initial increases")
popularityTracker.increasePopularity(7)
print("Increased popularity of 7")

popularityTracker.increasePopularity(7)
print("Increased popularity of 7")

popularityTracker.increasePopularity(8)
print("Increased popularity of 8")

print("Most popular:", popularityTracker.mostPopular())        # should return 7

print("\nTest Case 2: More increases")
popularityTracker.increasePopularity(8)
print("Increased popularity of 8")

popularityTracker.increasePopularity(8)
print("Increased popularity of 8")

print("Most popular:", popularityTracker.mostPopular())        # should return 8

print("\nTest Case 3: Decreases")
popularityTracker.decreasePopularity(8)
print("Decreased popularity of 8")

popularityTracker.decreasePopularity(8)
print("Decreased popularity of 8")

print("Most popular:", popularityTracker.mostPopular())        # should return 7

print("\nTest Case 4: More decreases")
popularityTracker.decreasePopularity(7)
print("Decreased popularity of 7")

popularityTracker.decreasePopularity(7)
print("Decreased popularity of 7")

popularityTracker.decreasePopularity(8)
print("Decreased popularity of 8")

print("Most popular:", popularityTracker.mostPopular())        # should return -1
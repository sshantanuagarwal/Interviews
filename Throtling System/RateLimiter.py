

class RateLimiter():
    
    def __init__( self, limitMap ):
        self.limitMap = limitMap
        self.sec = None
        self.min = None
        self.hour = None
        self.week = None
        self.month = None
        for time, limit in limitMap.items():
            if time == "sec":
                self.sec = limit
            elif time == "min":
                self.min = limit
            elif time == "hour":
                self.hour = limit
            elif time == "week":
                self.week = limit
            elif time == "month":
                self.month = limit
            else:
                assert False, "Unhandle time %s" % time
    
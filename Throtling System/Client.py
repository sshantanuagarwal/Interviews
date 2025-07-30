from RateLimiter import *


globalLimit = { "hour" : 100,
                "week" : 900,
                "month" : 10000,
                }
getLimit = {
             "sec" : 10,
             "min" : 50,
             "week" : 700
          }
postLimit = {
             "sec" : 20,
             "hour" : 40,
             "week" : 900,
             "month" : 1000
            }
statusLimit = {
             "sec" : 20,
             "hour" : 40,
             "week" : 900,
             "month" : 1000
            }

payLimit = {
             "sec" : 10,
             "hour" : 50,
             "week" : 1000,
             "month" : 5000
            }

class Client( object ):
    clientId = None
    globalLimit = None
    methodLimits = {}
    apiLimits = {}
    
    def __init__( self, clientId ):
        self.clientId = clientId
        self.setGlobalLimits()
        self.setMethodLimits()
        self.setApiLimits()
        
    def setGlobalLimits( self ):
        self.globalLimit = RateLimiter( globalLimit )
        
    def setMethodLimits( self ):
        self.methodLimits = {
            "GET" : RateLimiter( getLimit ),
            "POST" : RateLimiter( postLimit ),
            }
        
    def setApiLimits( self ):
        self.apiLimits = {
            "status" : RateLimiter( statusLimit ),
            "pay" : RateLimiter( payLimit ),
            }
        
    def createLimitDict( self, sec=None, min=None, hour=None, week=None, month=None ):
        lim = {}
        if sec is not None:
            lim[ "sec" ] = sec
            
        if min is not None:
            lim[ "min" ] = min
            
        if hour is not None:
            lim[ "hour" ] = hour
            
        if week is not None:
            lim[ "week" ] = week
            
        if month is not None:
            lim[ "month" ] = month
        
        return lim;

    def addNewMethodLimits( self, method, sec=None, min=None, hour=None, week=None ):
       lim  = self.createLimitDict( sec, min, hour, week, month )
       self.methodLimits[ method ] = RateLimiter( lim )
    
    def addNewApiLimits( self, method, sec=None, min=None, hour=None, week=None ):
       lim  = self.createLimitDict( sec, min, hour, week, month )
       self.apiLimits[ method ] = RateLimiter( lim )
    
    
class Throttle( object ):
    
    clientList = {}
    
    def __init__( self ):
        pass
    
    def request( self, client, method=None, api=None ):
        c = None
        if not client in clientList:
            c = Client( client )
            self.clientList[ client ] = c
            
        else:
            c = self.clientList[ client ]
            
            
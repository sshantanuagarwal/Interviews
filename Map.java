/* package codechef; // don't place package name! */

import java.util.*;
import java.lang.*;
import java.io.*;

/* Name of the class has to be "Main" only if the class is public. */
class Codechef
{
    void print( String, k, String v ) {
        System.out.println( "Key:" + entry.getKey() + " = " + " value: " + entry.getValue() );
    }
	public static void main (String[] args) throws java.lang.Exception
	{
		// your code goes here
		
		
		
		Map <String, String> m = new HashMap<String,String>();
		m.put( "a", "z" );
		m.put( "b","y" );
		
		for( Map.Entry<String, String> entry : m.entrySet() ) {
		    
		}
		m.forEach( (k,v) -> print( k,v) );
	}
}

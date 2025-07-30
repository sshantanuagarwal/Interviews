Hi

A 
B 
C

a+b+c = k



Int l = arr.size();
For I in 0 to l:
	for j in I + 1 to l:
		for k in j+1 to l:
			if( ar[ I ] + ar[ j ] + ar[ k ] == k )
		

O( n^3 ) 



a+b = k - c 

Int I = arr.size();

while( I < l )  {
	

/* package codechef; // don't place package name! */

import java.util.*;
import java.lang.*;
import java.io.*;

/* Name of the class has to be "Main" only if the class is public. */
class Codechef
{
    public static void solve(int[] input, int sum){
        Map<Integer, ArrayList<Integer>> pairSum = new HashMap<Integer, ArrayList<Integer> >();
        int l = input.length;
        for( int i = 0; i  < l; i++ ) {
	        for( int  j = i+1; j < l; j ++) {
	            ArrayList<Integer> list =  new ArrayList<Integer>();
	            list.add(  i );
	            list.add(  j );
	            
	            pairSum.put( input[ i ] + input[ j ], list  );
	        }
        }
        
        for( int k = 0; k < l; k++ ) {
            if( pairSum.containsKey( sum - input[ k ] ) ) {
                List<Integer> list = pairSum.get( sum-input[ k ] ); 
                if( k == list.get( 0 ) || k == list.get( 1 ) )
                    continue;
                
                System.out.println( "Sum exists:" + input[ list.get( 0 ) ] + " " + input[ list.get( 1 ) ] + " " + input[ k ] );
                return;
            }
        }
        System.out.println("NO such triplet");

    }
    
	public static void main (String[] args) throws java.lang.Exception
	{
	    int[] input = new int[]{3, -1, 0, 0, 2, 4, 2, 3}; // 3 -1 -3, 
        int k = -1;
        solve(input, k);
	    
		// your code goes here
	}
}

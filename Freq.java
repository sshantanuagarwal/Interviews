import java.util.*;
import java.lang.*;
import java.io.*;

class Codechef
{
	public static void main (String[] args) throws java.lang.Exception
	{
		int[] arr = { 2, 1, 3, 3, 1, 2, 2, 2, 4 };
		int l = arr.length, i = 0;
		while( i < l ) {
		    if( arr[ i ] <= 0 ) {
		        i++;
		        continue;
		    }
		    int index = arr[ i ] - 1;
		    if( arr[ index ] > 0 ) {
		        arr[ i ] = arr[ index ];
		        arr[ index ] = -1;
		    } else {
		        arr[ index ]--;
		        arr[ i ] = 0;
		        i++;
		    }
		}
		for(  i = 0; i < l; i++ ) {
		    if( arr[ i ]  != 0 )
		        System.out.println( i + 1 + " : " + Math.abs( arr[ i ] ) );
		}
	}
}

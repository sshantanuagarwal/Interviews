/* package codechef; // don't place package name! */

import java.util.*;
import java.lang.*;
import java.io.*;
import java.util.concurrent.*;

/*
class ThreadPool extends Thread {
    
     public void run() {
        String s = "";
	    Thread[] t = {
	        new Thread( "t1" ) {
	            public void run() {
	                try {
        	            this.sleep(1);
        	            s += "a";
	                } catch (Exception e){
	                
	                }
	            }
	        },
	        new Thread( "t2" ) {
	            public void run() {
	                try {
        	            this.sleep(2);
        	            s += "b";
	                } catch (Exception e){
	                    
	                }
	            }
	        },
	        new Thread( "t3" ) {
	            public void run() {
	                try {
        	            this.sleep(3);
        	            s += "c";
	                }catch( Exception e ){
	                }
	            }
	        }
	    };
	    
	    for( int i = 0; i < 3; i++ ) {
	        t[ i ].start();
	    }
	    System.out.println( s );
     }
}
*/
/* Name of the class has to be "Main" only if the class is public. */
class Codechef
{
    int count = 0;
	String s = "";
	public synchronized void append() {
	    try {
    	    System.out.println( s );
    	    Thread.sleep(1);
    	    s += ++count;
	    } catch( Exception e ){
	    
	    }
	}    
	
	public static void main (String[] args) throws java.lang.Exception
	{
	    /*
	    ThreadPool tp = new ThreadPool();
	    tp.start();*/
	    
	    
	    ExecutorService es = Executors.newFixedThreadPool( 3 );
	    Codechef c = new Codechef();
	    for( int i = 0; i < 3; i++ ) {
	        
    	    es.execute( new Runnable() {
    	        public void run() { 
    	            c.append();
    	        }
    	    }
    	   );
	    }
	    //while( !es.terminated() ) {}
	    
	    
	    
	    System.out.println( c.s );
	}
}

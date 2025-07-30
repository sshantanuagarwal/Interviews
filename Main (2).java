/******************************************************************************

                            Online Java Compiler.
                Code, Compile, Run and Debug java program online.
Write your code in this editor and press "Run" button to execute it.

*******************************************************************************/

public class Main
{

  static class StackNode
  {
    int n;
    StackNode next;
  }


  int top = -1;
  StackNode head = null;

  StackNode newNode (int n)
  {
    StackNode tmp = new StackNode ();
      tmp.n = n;
      tmp.next = null;
      return tmp;
  }

  boolean isEmpty ()
  {
    return top == -1;
  }

  void push (int n)
  {
    StackNode node = newNode (n);
    node.next = head;
    head = node;
    top += 1;
  }

  StackNode pop ()
  {
    if (isEmpty ())
    {
        //throw Exception( "Stack is empty");
	    return null;
    }
    StackNode tmp = head;
    head = head.next;
    top -= 1;
    return tmp;
  }

  StackNode peek ()
  {
    return head;
  }

  void print ()
  {
    StackNode tmp = head;
    System.out.print ("Elements: " );
    
    while (tmp != null) {
        System.out.print (tmp.n + " ");
        tmp = tmp.next;
        
    }
    System.out.println ();
      
  }
  public static void main (String[]args)
  {

      System.out.println ("Hello World");
      Main m = new Main ();
      m.push (1);
      m.push (2);
      m.push (3);
      m.print ();
      m.pop (); m.print (); m.pop (); m.pop (); m.print ();
      
  }
  }

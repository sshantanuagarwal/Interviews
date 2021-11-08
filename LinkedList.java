class Node {
    int data;
    Node next;
    Node(int d) {
        this.data = d;
        this.next = null;
    }
}
/*
1->2->3->4->5
2->1->4->3->5
 */
public class LinkedList {
    Node head;
    LinkedList () {
        this.head = null;
    }

    public static Node reverse(Node head) {
        if(head == null || head.next == null) {
            return head;
        }
        Node curr = head;
        Node next = null;
        Node prev = null;

        for(int i = 0; i < 2; i++) {
            if(curr != null) {
                next = curr.next;
                curr.next = prev;
                prev = curr;
                curr = next;
            }
        }

        if(next != null) {
            head.next = reverse(next);
        }
        return prev;
    }

    public static void print( Node head) {
        Node tmp = head;
        while(tmp != null) {
            System.out.print( tmp.data + "->");
            tmp = tmp.next;
        }
        System.out.println("NULL");
    }
    public static void main(String[] args) {
        Node head = new Node(1);
        /*head.next = new Node(2);

        head.next.next = new Node(3);
        head.next.next.next = new Node(4);
        head.next.next.next.next = new Node(5);
        head.next.next.next.next.next = new Node(6);
*/
        print(head);
        head = reverse(head);
        print(head);
    }
}

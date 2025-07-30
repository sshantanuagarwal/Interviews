public class ThreadPoolClass {
    private int n;
    private TaskAssignment[] threads;
    private LinkedBlockingQueue queue;
 
    public ThreadPoolClass(int n) {
        this.n = n;
        queue = new LinkedBlockingQueue();
        threads = new TaskAssignment[nThreads];
 
        for (int i = 0; i < n; i++) {
            threads[i] = new TaskAssignment();
            threads[i].start();
        }
    }
 
    public void execute(Runnable task) {
        queue.add(task);
        queue.notify();
    }
 
    private class TaskAssignment extends Thread {
        public void run() {
            Runnable task;
            while (true) {
                task = queue.poll();
                task.run();
            }
        }
    }
}

public class Main {
 
    public static void main(String[] args) {
        ThreadPoolClass pool = new ThreadPoolClass(3);
 
        for (int i = 0; i < 100; i++) {
            Task task = new Task(i);
            pool.execute(task);
        }
}
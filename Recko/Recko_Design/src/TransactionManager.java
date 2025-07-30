import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReadWriteLock;

public class TransactionManager {
    List<User> users;
    List<Transaction> transactions;
    Map<User,Map<User, Double>> userMapping;

    ReadWriteLock rwLock = new ReadWriteLock() {
        @Override
        public Lock readLock() {
            return null;
        }

        @Override
        public Lock writeLock() {
            return null;
        }
    }
    TransactionManager () {
        users = new ArrayList<>();
        transactions = new ArrayList<>();
        userMapping = new ConcurrentHashMap<>();
    }

    public void addUser(User user) {
        this.users.add(user);

    }

    public void AddExpense(User paid, Integer nOfUsers, List<User> user, String action,
                            Double amount, List<Double> expenses ) {

        Action act = new Action();
        Transaction transaction = act.addExpenseFactory(paid, nOfUsers,user,action,amount,expenses);
        transactions.add(transaction);

        this.rwLock.writeLock().lock();
        Map<User, Double> owner;
        if(!userMapping.containsKey(paid)) {
            owner = new ConcurrentHashMap<>();
            for (int i = 0; i < nOfUsers; i++) {
                owner.put(transaction.userList.get(i), transaction.expenses.get(i));
            }
        } else {
            owner = this.userMapping.get(paid);
            for (int i = 0; i < nOfUsers; i++) {
                User owe = transaction.userList.get(i);
                if(owner.containsKey(owe)) {
                    owner.put(owe, owner.get(owe) + transaction.expenses.get(i));
                } else {
                    owner.put(owe, transaction.expenses.get(i));
                }
            }
        }
        userMapping.put(paid, owner);
        this.rwLock.writeLock().unlock();

    }
    public  void ShowExpense( User paid ) {
        if(userMapping.containsKey(paid)) {

            Map<User, Double> owner = userMapping.get(paid);
            for(Map.Entry<User, Double> entry : owner.entrySet()) {
                System.out.println(entry.getKey().name + " owes user " + paid.name + " :" + entry.getValue());
            }
        }
        System.out.println("User does not exist");
    }
    public  void ShowAllExpense( ) {

    }
    public  void  CreateGroup( User owner, List<> Users ) {

    }

}

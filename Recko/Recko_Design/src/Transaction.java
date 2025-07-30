import java.util.*;

public class Transaction {
    Integer transactionId;
    User paid;
    Integer nOfUsers;
    List<User> userList;
    Double amount;
    List<Double> expenses;

    Integer generateRandomId() {
        return 1;
    }
    Transaction(User paid, Integer nOfUsers, List<User> user, Double amount, List<Double> expenses) {
        this.transactionId = generateRandomId();
        this.paid = paid;
        this.nOfUsers = nOfUsers;
        this.userList = user;
        this.amount = amount;
        this.expenses = expenses;
    }
}

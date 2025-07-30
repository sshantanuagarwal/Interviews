import java.time.Clock;
import java.util.*;

public class Action {

    String[] actions = new String[]{"Exact", "Equal", "Percentage"};

    public boolean validateExactSplit(List<Double> expenses, Double amount) {
        double sum = 0.0;
        for(int i = 0; i < expenses.size();i++) {
            sum += expenses.size();
        }
        return sum == amount;
    }

    public boolean validatePercentSplit(List<Double> expenses, Double amount) {
        double sum = 0.0;
        for(int i = 0; i < expenses.size();i++) {
            sum += expenses.size();
        }
        return sum == 100;
    }

    public Transaction addExpenseFactory(User paid, Integer nOfUsers, List<User> user, String action,
                                         Double amount, List<Double> expenses) {
        if(action == this.actions[0]) {
            if(this.validateExactSplit(expenses, amount)) {
                return new Transaction(paid, nOfUsers, user, amount, expenses);
            }
        } else if(action == this.actions[1]) {
            List<Double> expense = new ArrayList<>();
            for(int i = 0; i < nOfUsers; i++) {
                expense.add(amount/nOfUsers);
            }
            return new Transaction(paid, nOfUsers, user, amount, expense);

        } else if(action == this.actions[2]) {
            if(this.validatePercentSplit(expenses, amount)) {
                List<Double> expense = new ArrayList<>();
                for(int i = 0; i < nOfUsers; i++) {
                    expense.add(expenses.get(i) * amount / 100);
                }
                return new Transaction(paid, nOfUsers, user, amount, expenses);
            }

        } else {
            System.out.println("Invalid Action");
        }
        return null;
    }


}

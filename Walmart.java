
/*

You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.
[7,1,5,3,6,4]
*/

import javafx.util.Pair;

import java.util.ArrayList;

public class Walmart {

    public static void stocks(int price[]) {
        int i = 0;
        int n = price.length;
        int min = Integer.MAX_VALUE;
        int minIndex = 0,minIndex1 = 0,maxIndex = 0;
        int maxProfit = 0;
        while(i < n) {
            if(min > price[i]) {
                if(price[i] < min) {
                    minIndex1 = i;
                }
                min = Math.min(min, price[i]);

            }
            else if(price[i] - min > maxProfit) {
                if(price[i] - min > maxProfit) {
                    minIndex = minIndex1;
                    maxIndex = i;
                }
                maxProfit = Math.max(maxProfit, price[i] - min);

            }
            i++;
            /*
            while (i < n - 1 && price[i + 1] <= price[i]) {
                i++;
            }
            if (i == -1) {
                System.out.println("No minimum value");
                return;
            } else {
                System.out.println("Minima at" + i);
            }
            int j = i;
            while (j < n && price[j + 1] > price[j]) {
                j++;
            }
            if (j == -1) {
                System.out.println("No maximum value");
                return;
            }*/
        }
        System.out.println("Buy at price " + price[minIndex] + " sell at "  + price[maxIndex] + " with profit " + maxProfit);

    }

    public static void main(String[] args) {
        int[] price = {7,5,3,8,5,2,5};
        stocks(price);
    }
}

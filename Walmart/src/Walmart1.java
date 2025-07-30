import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.Set;

/* There is a dictionary containing words from an alien language for which we don’t know the ordering of the alphabets.
Write a method to find the correct order of the alphabets in the alien language.
It is given that the input is a valid dictionary and there exists an ordering among its alphabets.

Input: Words: ["ba", "bc", "ac", "cab"]

*/
public class Walmart1 {
    public static void main(String[] args) {
        String[] words = {"ywx", "wz", "xww", "xz", "zyy", "zwz"};//{"ba", "bc", "ac", "cab"};
        int l = words.length;
        Set<Character> output_list = new LinkedHashSet<>();
        for(int k = 0 ; k < l-1; k++) {
            String word1 = words[k];
            String word2 = words[k+1];
            int i = 0;
            int j = 0;
            int n = word1.length();
            int m = word2.length();

            while(i < n && j < m) {
                if(word1.charAt(i) == word2.charAt(j)) {
                    output_list.add(word1.charAt(i));
                } else {
                    output_list.add(word1.charAt(i));
                    output_list.add(word2.charAt(j));
                }
                i++;
                j++;
            }

        }
        System.out.println(output_list);
    }
}

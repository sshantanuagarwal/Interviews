/*
Given a string s and an array of strings words, return the number of words[i] that is a subsequence of s.

s = "abcde", words = ["a","bb","acd","ace"]
Output: 3
"a", "acd", "ace"

"ahjpjau","ja","ahbwzgqnuk","tnmlanowax"
 */

import java.util.HashMap;
import java.util.LinkedHashMap;

public class Walmart2 {

    public static void main(String[] args) {
        String s = "dsahjpjauf";//"abcde";
        HashMap<Character,Integer> map = new LinkedHashMap<>();
        for(int i = 0; i < s.length(); i++) {
            Character c = s.charAt(i);
            map.put(c, map.getOrDefault(c,0) + 1 );
        }
        String[] words = {"ahjpjau","ja","ahbwzgqnuk","tnmlanowax"};//{"a","bb","cd","ce"};
        int count = 0;
        for(String word : words) {
            HashMap<Character,Integer> local_map = (HashMap<Character,Integer>) map.clone();
            boolean wordFound = true;
            for(int i = 0; i < word.length(); i++) {
                Character c = word.charAt(i);
                if(local_map.containsKey(c) && local_map.get(c) > 0) {
                    local_map.put(c, local_map.get(c) - 1);
                } else {
                    wordFound = false;
                    break;
                }
            }
            //System.out.println(word + local_map);
            count += wordFound ? 1 : 0;
        }
        System.out.println(count);
    }
}

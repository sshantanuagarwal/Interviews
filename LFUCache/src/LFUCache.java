/*

LinkedHashMap<Integer, DataObject>

DataObject {
    Integer data;
    Integer frequency;
}



 */

//import java.util.LinkedHashMap; LinkedHashMap<Integer, DataObject>

import java.net.Inet4Address;
import java.util.HashMap;
import java.util.*;

class DataObject {
    Integer data;
    Integer frequency;

    DataObject() {
        this.data = null;
        this.frequency = 0;
    }
}

public class LFUCache {
    LinkedHashMap<Integer, DataObject> cache;
    TreeMap<Integer,Set<Integer>> freqMap;
    int capacity;
    int minKey;
    LFUCache(int capacity) {
        this.capacity = capacity;
        this.cache = new LinkedHashMap<>();
        this.minKey = Integer.MAX_VALUE;
        this.freqMap = new TreeMap<>();
    }

    public boolean isFull() {
        return this.cache.size() >= this.capacity;
    }

    public void updateFreqMap(Integer newFreq, Integer key ) {
        Set<Integer> newSet = freqMap.getOrDefault(newFreq, new HashSet<>());
        newSet.add(key);
        freqMap.put(newFreq, newSet);

        Integer oldFreq = newFreq-1;
        Set<Integer> oldSet = freqMap.getOrDefault(oldFreq, new HashSet<>());
        oldSet.remove(key);
        if(oldSet.isEmpty()) {
            freqMap.remove(oldFreq);
        } else {
            freqMap.put(oldFreq,oldSet);
        }
    }

    public Integer getLeastFrqKey() {

        /*
        Integer key = null;
        int minFreq = Integer.MAX_VALUE;
        for(Map.Entry<Integer,DataObject> entry : map.entrySet()) {
            if(entry.getValue().frequency < minFreq) {
                key = entry.getKey();
                minFreq = entry.getValue().frequency;
            }
        }*/
        int key = freqMap.firstKey();
        Set<Integer> set = freqMap.get(key);
        return set.stream().findFirst().get();
    }

    public void put(Integer key, Integer value) {
        if(this.isFull() && !cache.containsKey(key)) {
            Integer removedKey = this.getLeastFrqKey();
            System.out.println("Key to be removed:" + removedKey);
            cache.remove(removedKey);
        }

        DataObject obj = cache.getOrDefault(key, new DataObject());
        obj.data = value;
        obj.frequency++;

        // Put into cache
        cache.put(key, obj);

        // Update frequency
        updateFreqMap(obj.frequency, key);

    }


    public Integer get(Integer key) {
        if(cache.containsKey(key)) {

            System.out.println("Cache Hit" + key);

            DataObject obj = cache.get(key);
            obj.frequency++;

            // Put into cache
            cache.put(key,obj);

            // Update frequency
            updateFreqMap(obj.frequency, key);
            return obj.data;
        }

        System.out.println("Cache Miss" + key);
        return null; // Miss
    }

    public static void main(String[] args) {
        LFUCache cache = new LFUCache(5);
        cache.put(1,1);
        cache.put(2,2);
        cache.put(3,3);
        cache.put(4,4);
        cache.put(5,5);

        cache.get(1);
        cache.get(1);
        cache.get(1);
        cache.get(1);
        cache.get(1);

        cache.get(2);
        cache.get(2);
        cache.get(2);

        cache.get(2);
        cache.get(2);
        cache.get(2);

        cache.get(6);

        cache.put(6,6);
        cache.get(6);
    }
}

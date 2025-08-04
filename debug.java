import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class debug {

    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> ans = new ArrayList<>();
        //维护一个存放目标值的set
        Map<Character,Integer> target = new HashMap<>();
        for(int i = 0;i<p.length();i++){
           target.put(p.charAt(i), target.getOrDefault(p.charAt(i), 1) + 1);
        }

        //维护一个滑动窗口和一个set存放当前窗口里的值
        Map<Character,Integer> curr = new HashMap<>();
        for(int i = 0;i<p.length();i++){
            curr.put(s.charAt(i), curr.getOrDefault(s.charAt(i), 1) + 1);
        }
        //滑动窗口
        int start = 0;
        int end = p.length()-1;
        while(end<s.length()){
            if(curr.equals(target)){
                ans.add(start);
            }
            //移除start
            char c = s.charAt(start);
            curr.put(c, curr.get(c) - 1);
            if (curr.get(c) == 0) {
                curr.remove(c);
            }
            //添加end的下一个 
            if(end<s.length()-1){
                curr.put(s.charAt(end+1), curr.getOrDefault(s.charAt(end+1), 0) + 1);
            }
            start++;
            end++;
            
        }
        return ans;
    }
    public static void main(String[] args) {
        String s = "baa";
        String p = "aa";
        debug d = new debug();
        System.out.println(d.findAnagrams(s,p));
    }
}
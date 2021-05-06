"""
Student ID: 31164110
Name: Adeline Chew Yao Yi
"""
import math

class SequenceDatabase:
    """
    A class stores DNA data in database. 
    This class has two main functions: addSequence and query.
    """
    def __init__(self):
        """
        Constructor method, create a node on the root.
        Complexity: O(1)
        """
        self.root = Node()
    
    def addSequence(self, s):
        """
        Stores string in the class using tries.
        Complexity: O(len(s)) where s is the input string
        Args:
            s ([String]): [Input string that contains only A,B,C,D]
            level([Int]): [Indicates the level of current node]
        """
        current = self.root
        freq, node = self.addSequence_aux(current, s)
        if current.most_freq[1] < freq:
            current.most_freq = (node, freq)
        elif current.most_freq[1] == freq:
            if s[0] < current.most_freq[0].data[0] or \
                (s[0] == current.most_freq[0].data[0] and len(s[0]) < len(current.most_freq[0].data[0])):
                current.most_freq = (node, freq)
            
    
    def addSequence_aux(self, current, s, i=0, value=1):
        """ 
        Use recursion to form a tries, base case when i reach terminal node $.
        Each node stores the frequency of the time it has been added in,
        each node also stores a links to its most frequent child node.
        Complexity: O(len(s)) where s is the input string
        Args:
            current ([Node]): [Current node]
            s ([String]): [Input string that contains only A,B,C,D]
            i (int, optional): [Index points to s]. Defaults to 0.
        Returns:
            [(Int, Node)]: [Return the most frequency count and the represented node]
        """
        pre = current
        if i == len(s): # means index i reach $
            if current.links[0] is not None: # the word exists
                current = current.links[0]
                current.freq += 1
                i += 1
                return current.freq, current
            else: # the word doesn't exist, create a new node for $
                current.links[0] = Node(s)
                current = current.links[0]
                current.most_freq = (current, 1)
                i += 1
            return 1, current
        else:
            index = ord(s[i]) - ord('A') + 1
            # if path exists
            if current.links[index] is not None:
                current = current.links[index]
            # if path does not exists
            else:
                current.links[index] = Node()
                current = current.links[index]
            i += 1
            res = self.addSequence_aux(current, s, i)
            freq, node = res[0], res[1]
        # create a short path from current to the most freq leaf
        i -= 1
        if current.most_freq[1] < freq:
            current.most_freq = (node, freq)
        if i > 0 and pre.most_freq[1] == freq and i < len(pre.most_freq[0].data):
            if s[i] <= pre.most_freq[0].data[i]:
                pre.most_freq = (node, freq)
        elif i == 0 and current.most_freq[1] == freq and i < len(current.most_freq[0].data):
            if s[i] <= current.most_freq[0].data[i]:
                current.most_freq = (node, freq)
        return freq, node
    
    def query(self, q):
        """
        This method returns the string stored in database which have the
        highest frequency than other string with q as the prefix.
        Complexity: O(len(q)) where q is the input query string
        Args:
            q ([String]): [Input prefix string]
        Returns:
            [String]: [Most frequent string that has q as prefix]
        """
        res = self.query_aux(q)
        if res is not None:
            return res
        return None
        
    def query_aux(self, q):
        current = self.root
        if len(q) == 0:
            return current.most_freq[0].data
        for char in q:
            index = ord(char) - ord('A') + 1
            # if path exists
            if current.links[index] is not None:
                current = current.links[index]
            # if path doesn't exist
            else:
                return None
        highest, h_index = 0, 0
        for i in range(5):
            if current.links[i] is not None:
                freq = current.links[i].most_freq[1]
                if freq > highest:
                    highest = freq
                    h_index = i
        current = current.links[h_index]
        return current.most_freq[0].data

    
    # def query(self, q):
    #     """
    #     This method returns the string stored in database which have the
    #     highest frequency than other string with q as the prefix.
    #     Complexity: O(len(q)) where q is the input query string
    #     Args:
    #         q ([String]): [Input prefix string]
    #     Returns:
    #         [String]: [Most frequent string that has q as prefix]
    #     """
    #     current = self.root 
    #     for char in q:
    #         index = ord(char) - ord('A') + 1
    #         # if path exists
    #         if current.links[index] is not None:
    #             current = current.links[index]
    #         # if path doesn't exist
    #         else:
    #             return None
    #     # path doesn't exist
    #     if current == None or current.most_freq[0] == None :
    #         return None
    #     else:
    #         return current.most_freq[0].data
            
            
class Node:
    """
    Node in every tries, stores frequency of the node, link to the highest frequency
    child node, and any data needed. 
    """
    def __init__(self, data=[], freq=1, size=5, val=0):
        """Constructor of class Node.
        Complexity: O(1)
        """
        self.freq = freq
        self.most_freq = (None, 0, 0) # (Node, frequency, val)
        self.data = data
        self.links = [None] * size
        self.val = val
     
     
class OrfFinder:
    """Class OrfFinder stores a genome string, and contains a suffix tries of the genome.
    """
    def __init__(self, genome):
        """Constructor of class OrfFinder.
        Complexity: O(1)
        Args:
            genome ([String]): [Input string that contains only A,B,C,D]
        """
        self.genome = genome
        self.root = Node()
        self._addSuffixes(genome)

    def _addSuffixes(self, genome):
        """Method that creates a suffix tries for all the substrings of genome.
        Complexity: O(N^2) where N is the length of string genome.
        Args:
            genome ([String]): [Input string that contains only A,B,C,D]
        """
        index = 0
        while index <= len(genome): 
            current = self.root
            self._addSuffixes_aux(current, index, index)
            index += 1
            
    def _addSuffixes_aux(self, current, i, ori_index):
        """Auxiliary function to store each substring of genome into suffix tries,
        each node represents an alphabet and store the index of their parent's first prefix,
        or index of their child's first prefix.
        Complexity: O(m) where m is the length of self.genome[ori_index:]
        Args:
            current ([Node]): [Current node]
            i ([Int]): [Index points to genome string]
            ori_index ([Int]): [Index points to genome, stay unchanged]
        """
        if i == len(self.genome): # means index i reach $
            if current.links[0] is None: # the word doesn't exist, create a new node for $
                current.links[0] = Node()
            current = current.links[0]
        else:
            index = self.indexing(i)
            # if path exists
            if current.links[index] is not None:
                current = current.links[index]
            # if path does not exists
            else:
                current.links[index] = Node()
                current = current.links[index]
            i += 1
            self._addSuffixes_aux(current, i, ori_index)
        # Store the index of the prefix of each string that pass through current node
        current.data = current.data + [ori_index]
        return 

    
    def indexing(self, x, isGenome=True):
        """ Return the index of alphabet: A = 1, B = 2, C = 3 and D = 4
        Complexity: O(1)
        Args:
            x ([Char | index]): [Single character input or index pointed to genome]
            isGenome (bool, optional): [Get char from genome]. Defaults to True.
        Returns:
            [Int]: [Index]
        """
        if isGenome:
            return ord(self.genome[x]) - ord('A') + 1 
        return ord(x) - ord('A') + 1 

    def find_indices(self, str1):
        """Traverse until the end of the string, return the data stored in the node,
        return None if str1 is not in suffix tries
        Complexity: O(len(str1)) where str1 is the input string
        Args:
            str1 ([String]): [Prefix or suffix]
        Returns:
            [Node]: [Node that store the index of prefix or suffix in genome string]
        """
        current = self.root
        # Traverse until the end of the string
        for i in range(len(str1)):
            index = self.indexing(str1[i], False)
            if current.links[index] is not None:
                current = current.links[index]
            else:
                return None
        return current
            
    def find(self, start, end):
        """Finds all the substrings of string genome which have 'start' as prefix
        and 'end' as suffix, first lists all possible indices of start and end,
        then combines all possible combination in a tuple. Finally slice into substrings
        based on each tuple.
        Complexity: O(len(start) + len(end) + U) where start is the prefix, end is the suffix
                    and U is all the number of characters in the output list.
        Args:
            start ([String]): [Prefix that contains only ABCD]
            end ([String]): [Suffix that contains only ABCD]
        Returns:
            [List]: [List contains all the substrings in genome which have start as prefix
                    and end as suffix]
        """
        current = self.find_indices(start)
        s_subs = sorted(current.data) if current is not None else []
        current = self.find_indices(end)
        temp = sorted(current.data) if current is not None else []
        if len(s_subs) == 0 or len(temp) == 0 or current.data is None:
            return []
        e_subs = []
        for index in temp: # append the index of the prefix of the 'end' in the genome
            e_subs.append(index + len(end) - 1)
        i, k = 0, 0
        indices = []
        # Create possible combination of start and end
        while i < len(s_subs) and k < len(e_subs): 
            if s_subs[i] + len(start) - 1 < e_subs[k] and s_subs[i] + len(start) - 1 < e_subs[k] - len(end) + 1:
                indices.append((s_subs[i], e_subs[k]))
            k += 1
            if k == len(e_subs):
                if s_subs[i] > e_subs[-1]: # terminate earlier
                    break
                k = 0
                i += 1
        res = []
        for s, e in indices: # Append all the substrings into list
            res.append(self.genome[s:e + 1])
        
        return res 
    
db = SequenceDatabase()
# ls = ['DADDCCD', 'AACABDB', 'BCBBDAB', 'CBA', 'A', 'CDBBDCCCC', 'ABADBCDACB', 'CAAAAAADDB', 'CBBDA', 'BCCD', 'BDDBDABABC', 'DD', 'BADCCADBD', 'C', 'AD', 'ADDCDACBC', 'DABCD']
ls = ['CBCBB', 'CBBDCB']
for i in ls:
    db.addSequence(i)
print(db.query("")) # ans = 

# inp: [['BACA', 'BCDD', 'BACDCAC', 'ABAD', 'DAAACBC', 'CCBCDBCCCB', 'DDCCBDC', 'AB', 'AC', 'BCBCAC', 'ABD', 'C', 'BAC', 'ADBBDCACA'], '']
# out: AB
# got: ADBBDCACA

# inp: [['DBDDDA', 'AAADCDCC', 'CCBDBBCBCC', 'ABCBDCDB', 'DBCCACCCB', 'ADAC', 'CD', 'BBDCCBCAAC', 'DBBADAAACA', 'DADADDC', 'CABBCBCCB'], '']
# out: AAADCDCC
# got: ADAC

# inp: [['DAC', 'AAADBDBDBC', 'B', 'BCDD', 'BB', 'DCCDA', 'D', 'ACAB', 'DCBCCDADDC', 'CCADBDB'], '']
# out: AAADBDBDBC
# got: ACAB
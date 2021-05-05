"""
Student ID: 31164110
Name: Adeline Chew Yao Yi
"""


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
        """
        current = self.root
        freq, node = self.addSequence_aux(current, s)
        if current.most_freq[1] <= freq or (current.most_freq[1] == freq and node.data < current.most_freq[0].data):
            current.most_freq = (node, freq)
    
    def addSequence_aux(self, current, s, i=0):
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
        if i == len(s): # means index i reach $
            if current.links[0] is not None: # the word exists
                current = current.links[0]
                current.freq += 1
                return current.freq, current
            else: # the word doesn't exist, create a new node for $
                current.links[0] = Node(s)
                current = current.links[0]
            return 1, current
        else:
            index = ord(s[i]) - ord('A') + 1
            # if path exists
            if current.links[index] is not None:
                current = current.links[index]
            # if path does not exists
            else:
                current.links[index] = Node(s)
                current = current.links[index]
            i += 1
            freq, node = self.addSequence_aux(current, s, i)
        # create a short path from current to the most freq leaf
        if current.most_freq[1] <= freq or (current.most_freq[1] == freq and node.data < current.most_freq[0].data):
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
        current = self.root 
        for char in q:
            index = ord(char) - ord('A') + 1
            # if path exists
            if current.links[index] is not None:
                current = current.links[index]
            # if path doesn't exist
            else:
                return None
        # path doesn't exist
        if current == None or current.most_freq[0] == None :
            return None
        else:
            return current.most_freq[0].data
            
            
class Node:
    """
    Node in every tries, stores frequency of the node, link to the highest frequency
    child node, and any data needed. 
    """
    def __init__(self, data=[], freq=1, size=5):
        """Constructor of class Node.
        Complexity: O(1)
        """
        self.freq = freq
        self.most_freq = (None, 0) # (Node, frequency)
        self.data = data
        self.links = [None] * size
     
     
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
            if current.links[0] is not None: # the word exists
                current = current.links[0]
                return 
            else: # the word doesn't exist, create a new node for $
                current.links[0] = Node()
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
        """[summary]
        Complexity: TODO
        Args:
            start ([type]): [description]
            end ([type]): [description]

        Returns:
            [type]: [description]
        """
        current = self.find_indices(start)
        s_subs = sorted(current.data) if current is not None else []
        current = self.find_indices(end)
        e_subs = sorted(current.data) if current is not None else []
        if len(s_subs) == 0 or current == None or current.data == []:
            return []
        for index in current.data:
            e_subs.append(index + len(end) - 1)
        i, k = 0, 0
        indices = []
        while i < len(s_subs) and k < len(e_subs): # O(i + k)
            if s_subs[i] + len(start) - 1 < e_subs[k] and s_subs[i] + len(start) - 1 < e_subs[k] - len(end) + 1:
                indices.append((s_subs[i], e_subs[k]))
            k += 1
            if k == len(e_subs):
                if s_subs[i] > e_subs[-1]:
                    break
                k = 0
                i += 1
        res = []
        for s, e in indices: # O(u)
            res.append(self.genome[s:e + 1])
        return res 
    


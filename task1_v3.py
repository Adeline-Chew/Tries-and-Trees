class SequenceDatabase:
    def __init__(self):
        self.root = Node()
        pass
    
    def addSequence(self, s):
        current = self.root
        freq, node = self.addSequence_aux(current, s)
        index = ord(s[0]) - ord('A') + 1
        if freq > current.most_freq[1]:
            current.most_freq = (node, freq)
        elif freq == current.most_freq[1]:
            for x in range(5):
                if x == index:
                    pass
                if current.links[x] is not None:
                    h_index = x
                    break
            if h_index is not None:
                current.most_freq = current.links[h_index].most_freq

    def addSequence_aux(self, current, s, i=0):
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
            pre = current
            # if path exists
            if current.links[index] is not None:
                current = current.links[index]
            # if path does not exists
            else:
                current.links[index] = Node()
                current = current.links[index]
            i += 1
            freq, node  = self.addSequence_aux(current, s, i)
        # create a short path from current to the most freq leaf
        h_index = None
        if freq > current.most_freq[1]:
            current.most_freq = (node, freq)
        elif freq == current.most_freq[1]:
            for x in range(5):
                if x == index:
                    pass
                if current.links[x] is not None:
                    h_index = x
                    break
            if h_index is not None:
                current.most_freq = current.links[h_index].most_freq
        return freq, node
    
    def indexing(self, x):
        """ Return the index of alphabet: A = 1, B = 2, C = 3 and D = 4
        Complexity: O(1)
        Args:
            x ([Char | index]): [Single character input or index pointed to genome]
            isGenome (bool, optional): [Get char from genome]. Defaults to True.
        Returns:
            [Int]: [Index]
        """
        if x == '$':
            return 0
        return ord(x) - ord('A') + 1             
    
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
    def __init__(self, data=None, freq=1, size=5):
        self.freq = freq
        self.most_freq = (None, 0) # (str, frequency)
        self.data = data
        self.links = [None] * size
     
db = SequenceDatabase()
# ls = ['DADDCCD', 'AACABDB', 'BCBBDAB', 'CBA', 'A', 'CDBBDCCCC', 'ABADBCDACB', 'CAAAAAADDB', 'CBBDA', 'BCCD', 'BDDBDABABC', 'DD', 'BADCCADBD', 'C', 'AD', 'ADDCDACBC', 'DABCD']
ls = ['CBCBB', 'CBBDCB']
for i in ls:
    db.addSequence(i)
print(db.query("")) # ans = 

db1 = SequenceDatabase()
ls = ['A', 'BC', 'DDAD', 'AAD', 'BDCBBAAB', 'ADBD', 'B', 'ABDBBBA', 'DACCCCBBD']
for i in ls:
    db1.addSequence(i)
print(db1.query("")) # ans = A

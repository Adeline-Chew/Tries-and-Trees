
class SequenceDatabase:
    def __init__(self):
        self.root = Node()
        pass
    
    def addSequence(self, s):
        current = self.root
        freq, node = self.addSequence_aux(current, s)
        if current.most_freq[1] < freq:
            current.most_freq = (node, freq)
        elif current.most_freq[1] == freq:
            if s[0] < current.most_freq[0].data[0] or \
                (s[0] == current.most_freq[0].data[0] and len(s[0]) < len(current.most_freq[0].data[0])):
                current.most_freq = (node, freq)

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
    
    # def checkFreq(self, node, current, s, i=0):
        
                
        

    
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
        return current.links[h_index].most_freq[0].data
            
            
    
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

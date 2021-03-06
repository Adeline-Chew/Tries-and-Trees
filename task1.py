

class SequenceDatabase:
    def __init__(self):
        self.root = Node()
        pass
    
    def addSequence(self, s):
        current = self.root
        freq, node = self.addSequence_aux(current, s)
        if current.most_freq[1] < freq:
            current.most_freq = (node, freq)
        res = self.checkFreq(node, self.root, s)
        # if current.most_freq[1] < freq:
        #     current.most_freq = (node, freq)
        if node.data[0] < current.most_freq[0].data[0] and freq > current.most_freq[1]:
            current.most_freq = (node, freq)
        elif res is not None and res[0].data[0] <= current.most_freq[0].data[0]:
            if res[1] >= current.most_freq[1]:
                current.most_freq = res

    def addSequence_aux(self, current, s, i=0):
        if i == len(s): # means index i reach $
            if current.links[0] is not None: # the word exists
                current = current.links[0]
                current.freq += 1
                i += 1
                return current.freq, current
            else: # the word doesn't exist, create a new node for $
                current.links[0] = Node(s)
                current = current.links[0]
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
        if current.most_freq[1] < freq:
            current.most_freq = (node, freq)
        return freq, node
    
    def checkFreq(self, node, current, s, i=0):
        if i == len(s):
            current.most_freq = (node, node.freq)
            return (node, node.freq)
        index = ord(s[i]) - ord('A') + 1
        if i == len(current.most_freq[0].data):
            return current.most_freq
        elif node.freq == current.most_freq[1]:
            current = current.links[index]
            if node.data[i] == current.most_freq[0].data[i]:
                if i == len(s):
                    current.most_freq = (node, node.freq)
                    return (node, node.freq)
                else:
                    res = self.checkFreq(node, current, s, i + 1)
                    if res is not None:
                        current.most_freq = res
                    return res
        elif node.data[i] < current.most_freq[0].data[i]:
            current.most_freq = (node, node.freq)
            return (node, node.freq)
        else:
            res = self.checkFreq(node, current, s, i + 1)
            if res is not None:
                current.most_freq = res
            return res
                
        

    
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
ls = ['ABCACDBBD', 'BDDBAD', 'ACDDC', 'DDACCCABDB', 'DCADC', 'DDDABAABD', 'ACCAB', 'BBACBBDBAB', 'CBAADBAABC']
for i in ls:
    db.addSequence(i)
print(db.query("AC")) # ans = ACCAB 



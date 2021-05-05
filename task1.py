

class SequenceDatabase:
    def __init__(self):
        self.root = Node()
        pass
    
    def addSequence(self, s):
        current = self.root
        self.addSequence_aux(current, s)
    
    def addSequence_aux(self, current, s, i=0):
        if i == len(s): # means index i reach $
            if current.links[0] is not None: # the word exists
                current = current.links[0]
                current.freq += 1
                return current.freq, current
            else: # the word doesn't exist, create a new node for $
                current.links[0] = Node(s)
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
            res = self.addSequence_aux(current, s, i)
            freq, node = res[0], res[1]
        # create a short path from current to the most freq leaf
        if current.most_freq[1] < freq:
            current.most_freq = (node, freq)
        return freq, node
    
    def query(self, q):
        current = self.root 
        if len(q) == 0:
            return None
        for char in q:
            index = ord(char) - ord('A') + 1
            # if path exists
            if current.links[index] is not None:
                current = current.links[index]
            # if path doesn't exists
            else:
                print(None)
                return None

        print(current.most_freq[0].data)
        return current.most_freq[0].data
            
            
    
class Node:
    def __init__(self, data=None, freq=1, size=5):
        self.freq = freq
        self.most_freq = (None, 0) # (str, frequency)
        self.data = data
        self.links = [None] * size
     
        
if __name__ == '__main__':
    # db = SequenceDatabase()
    # db.addSequence("ABCD") 
    # db.addSequence("ABC") 
    # db.addSequence("ABC") 
    # db.query("A")
    # db.addSequence("ABCD") 
    # db.query("A")
    # db.addSequence("ABCD") 
    # db.query("A")
    # db.query("B")
    # db.addSequence("B") 
    # db.addSequence("B") 
    # db.addSequence("B") 
    # db.query("B")
    # db.addSequence("BC") 
    # db.addSequence("BC") 
    # db.addSequence("BC") 
    # db.query("B")
    
    SequenceDatabase().query("")
    
    failures = []
        # SequenceDatabase
    db = SequenceDatabase()
    tests = [
        [SequenceDatabase().query(""), None],  # empty database, empty query
        [SequenceDatabase().query("A"), None],  # empty database, non-empty query
        [SequenceDatabase().query("D"), None],  # empty databse, non-empty query
        [db.addSequence("A"), None],  # single letter database queries
        [db.query("A"), "A"],         #  |
        [db.query("B"), None],        #  |
        [db.query("C"), None],        #  |
        [db.query("D"), None] ,       #  |
        [db.addSequence("AA"), None],    # Prefixed database queries
        [db.addSequence("AAA"), None],   # |
        [db.addSequence("AAAA"), None],  # |
        [db.query("A"), "A"] ,           # |
        [db.query("AA"), "AA"] ,         # |
        [db.addSequence("AAA"), None],   # |
        [db.query("A"), "AAA"]           # |
    ]
    for i, t in enumerate(tests):
        if t[0] != t[1]:
            print(i)
    


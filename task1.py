

class SeqeunceDatabase:
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
                return current.freq
            else: # the word doesn't exist, create a new node for $
                current.links[0] = Node()
            return 1
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
            freq = self.addSequence_aux(current, s, i)
        # create a short path from current to the most freq leaf
        if current.most_freq[1] < freq:
            current.most_freq = (s, freq)
        return freq
    
    def query(self, q):
        current = self.root 
        for char in q:
            index = ord(char) - ord('A') + 1
            # if path exists
            if current.links[index] is not None:
                current = current.links[index]
            # if path doesn't exists
            else:
                print(None)
                return None

        print(current.most_freq[0])
        return current.most_freq[0]
            
            
    
class Node:
    def __init__(self, freq=1, size=5):
        self.freq = freq
        self.most_freq = (None, 0) # (str, frequency)
        self.links = [None] * size
     
        
if __name__ == '__main__':
    db = SeqeunceDatabase()
    db.addSequence("ABCD") 
    db.addSequence("ABC") 
    db.addSequence("ABC") 
    db.query("A")
    db.addSequence("ABCD") 
    db.query("A")
    db.addSequence("ABCD") 
    db.query("A")
    db.query("B")
    db.addSequence("B") 
    db.addSequence("B") 
    db.query("B")
    db.addSequence("BC") 
    db.addSequence("BC") 
    db.addSequence("BC") 
    db.query("B")
    

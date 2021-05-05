class OrfFinder:
    def __init__(self, genome):
        self.genome = genome
        self.root = Node()
        self._addSuffixes(genome)

    def _addSuffixes(self, genome):
        index = 0
        while index <= len(genome): 
            current = self.root
            self._addSuffixes_aux(current, index, index)
            index += 1
            
    def _addSuffixes_aux(self, current, i, ori_index):
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
        current.data = current.data + [ori_index]
        return 

    
    
    def indexing(self, x, isGenome=True):
        if isGenome:
            return ord(self.genome[x]) - ord('A') + 1 
        return ord(x) - ord('A') + 1 

    def find(self, start, end):
        current = self.root
        for i in range(len(start)):
            index = self.indexing(start[i], False)
            current = current.links[index]
        # s_subs = list(set(current.data)) # delete set
        s_subs = list(set(current.data)) if current is not None else []
        # print(s_subs)
        current = self.root
        for k in range(len(end)):
            index = self.indexing(end[k], False)
            current = current.links[index]
        e_subs = []
        if len(s_subs) == 0 or current == None or current.data == []:
            print("[]")
            return []
        for index in current.data:
            e_subs.append(index + len(end) - 1)
        e_subs = list(set(e_subs))
        # print(e_subs)
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
        # print(indices)
        res = []
        for s, e in indices: # O(u)
            res.append(self.genome[s:e + 1])
        print(res)
        return sorted(res)

class Node:
    def __init__(self, data=[], leaves = None, size=5):
        self.data = data
        self.leaves = leaves
        self.links = [None] * size


if __name__ == '__main__':
    # genome1 = OrfFinder("AABBCC")
    # genome1 = OrfFinder("AAABBBCCC")
    # genome1.find("AAA", "BB")
    # genome1.find("BB","A")
    # genome1.find("AA","BC") 
    # genome1.find("A","B")
    # genome1.find("AA","A") 
    # genome1.find("AAAB","BBB") 
    # genome2= OrfFinder("ABAABAA")
    # genome2.find("A", "B")
    # genome2 = OrfFinder("AAAAA")
    # genome2.find("A", "B")
    
    genome1 = OrfFinder("AAAAA")
    genome1.find("B", "B")
    genome1 = OrfFinder("AAAAA")
    tests = [
        [OrfFinder("A").find("A", "A"), []],  # single letter genome has no adfixes
        [OrfFinder("AA").find("A", "A"), ["AA"]],  # len(genome) = len(start) + len(end) = 0 or 1 prefixes
        [genome1.find("A", "A"), ["A"*i for i in range(2, 6) for _ in range(6-i)]],  # single repeating letter genome has N^2 adfixes
        [genome1.find("A", "B"), []],  # no adfixes if start or end not in genome
        [genome1.find("A", "C"), []],  # no adfixes if start or end not in genome
        [genome1.find("A", "D"), []],  # no adfixes if start or end not in genome
        [genome1.find("B", "B"), []],  # no adfixes if start or end not in genome
        [genome1.find("C", "B"), []],  # no adfixes if start or end not in genome
    ]
    for i, t in enumerate(tests):
        if t[0] != t[1]:
            print(i)
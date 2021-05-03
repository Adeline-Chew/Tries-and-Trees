
class OrfFinder:
    def __init__(self, genome):
        self.genome = genome
        self.root = Node()
        self._addSuffixes(genome)

    def _addSuffixes(self, genome):
        index = 0
        while index < len(genome): 
            current = self.root
            self._addSuffixes_aux(current, index, len(genome))
            index += 1

    def _addSuffixes_aux(self, current, start, end):
        index = self.indexing(start)
        # if path does not exist, create a new nodes
        if current.links[index] is None:
            current.links[index] = Node()
            current.links[index].data = [start, end]
            return
        current = current.links[index]
        i, k = start, current.data[0]
        while self.indexing(i) == self.indexing(k):
            if k == current.data[1] and k + 1 <= end:
                current = current.links[self.indexing(k + 1)]
                k = current.data[0]
            i += 1
            k += 1
            if i == end:
                break
        alpha_index_i = self.indexing(i) if i < end else 0
        alpha_index_k = self.indexing(k) if k < end else 0
        new_k_node = Node([k, end])
        new_links = current.links
        current.links = [None] * 5
        current.links[alpha_index_k] = new_k_node
        current.links[alpha_index_k].data = [k, current.data[1]]
        current.links[alpha_index_k].links = new_links

        current.links[alpha_index_i] = Node([i, end])
        current.data[1] = k - 1
        return
        
        
                
    def indexing(self, x):
        return ord(self.genome[x]) - ord('A') + 1

    def find(self, start, end):
        pass


class Node:
    def __init__(self, data=None, size=5):
        self.data = data
        self.links = [None] * size


if __name__ == '__main__':
    genome1 = OrfFinder("AAABBBCCC")
    genome1.find("AAA", "BB")



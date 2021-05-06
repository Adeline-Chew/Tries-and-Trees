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
        freq, node, alp = self.addSequence_aux(current, s)
        self.compare(current, freq, node, alp)

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
        if i == len(s):  # means index i reach $
            if current.links[0] is not None:  # the word exists
                current = current.links[0]
                current.freq += 1
                current.storage = (current, current.freq)
            else:  # the word doesn't exist, create a new node for $
                current.links[0] = Node(s)
                current = current.links[0]
                current.storage = (current, 1)
            i += 1
            return current.freq, current, 0
        else:
            index = ord(s[i]) - ord('A') + 1
            # if path does not exist
            if current.links[index] is None:
                current.links[index] = Node()
            current = current.links[index]
            i += 1
            freq, node, alp = self.addSequence_aux(current, s, i)
        # create a short path from current to the most freq leaf
        self.compare(current, freq, node, alp)
        return freq, node, index

    def compare(self, current, freq, node, alp):
        """Compare the most frequent node that stored in current node
        with current string. Current node also stores the next character
        after this node for the most frequent string, this is used for comparison.add()
        Complexity: O(1)
        Args:
            current (Node): [Current node]
            freq (Int): [Frequency of this string]
            node (Node): [The reference link of current terminal node]
            alp (Int): [Value of the character after this node]
        """
        if freq > current.storage[1]:
            current.storage = (node, freq)
            current.best_char = alp
        elif freq == current.storage[1] and alp < current.best_char: # the next alphabet has lower value
            current.storage = (node, freq)
            current.best_char = alp
        elif freq == current.storage[1] and alp == current.best_char: # same freq and same next alphabet
            current.storage = current.links[alp].storage # get the same best node as the child
            current.best_char = alp

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
        if current is None or current.storage[0] is None:
            return None
        else:
            return current.storage[0].data


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
        self.storage = (None, 0)  # (node, frequency)
        self.best_char = 0 # lowest available next node
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
        if i == len(self.genome):  # means index i reach $
            if current.links[0] is None:  # the word doesn't exist, create a new node for $
                current.links[0] = Node()
            current = current.links[0]
        else:
            index = self.indexing(i)
            # if path does not exist
            if current.links[index] is None:
                current.links[index] = Node()
            current = current.links[index]
            i += 1
            self._addSuffixes_aux(current, i, ori_index)
        # Store the index of the prefix of each string that pass through current node
        current.data = current.data + [ori_index]
        return

    def indexing(self, x, is_genome=True):
        """ Return the index of alphabet: A = 1, B = 2, C = 3 and D = 4
        Complexity: O(1)
        Args:
            x ([Char | index]): [Single character input or index pointed to genome]
            is_genome (bool, optional): [Get char from genome]. Defaults to True.
        Returns:
            [Int]: [Index]
        """
        if is_genome:
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
        s_subs = current.data if current is not None else []
        current = self.find_indices(end)
        temp = current.data if current is not None else []
        if len(s_subs) == 0 or len(temp) == 0 or current.data is None:
            return []
        e_subs = []
        for index in temp:  # append the index of the prefix of the 'end' in the genome
            e_subs.append(index + len(end) - 1)
        i, k = 0, 0
        indices = []
        # Create possible combination of start and end
        while i < len(s_subs) and k < len(e_subs):
            if s_subs[i] + len(start) - 1 < e_subs[k] and s_subs[i] + len(start) - 1 < e_subs[k] - len(end) + 1:
                indices.append((s_subs[i], e_subs[k]))
            k += 1
            if k == len(e_subs):
                if s_subs[i] > e_subs[-1]:  # terminate earlier
                    break
                k = 0
                i += 1
        res = []
        for s, e in indices:  # Append all the substrings into list
            res.append(self.genome[s:e + 1])
        return res


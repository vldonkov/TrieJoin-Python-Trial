# Returns index of x in arr if present, else index of least upper bound of x
def binary_search(arr, low, high, x):
    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if arr[mid] == x:
            return mid

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr[mid] > x:
            return binary_search(arr, low, mid - 1, x)

        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        return low


class TrieNode:
    """A node in the trie structure"""

    def __init__(self, number):
        # the number stored in this node
        self.number = number

        # stores the parent of the node
        self.parent = None

        # a dictionary of child nodes
        # keys are numbers, values are nodes
        self.children = {}

        # a counter indicating how many children the current node has
        self.counterChildren = 0

        # indicates the position of the node amongst its siblings
        self.numberInSiblings = 0

        # whether this can be the end of the number array
        self.isEnd = False


class Trie(object):
    """The trie object"""

    def __init__(self):
        """
        The trie has at least the root node.
        The root node does not store any number
        """
        self.root = TrieNode("")
        self.iterator = self.root

    def insert(self, numbArray):
        """Insert a number array into the trie"""
        node = self.root

        # Loop through each number in the number array
        # Check if there is no child containing the number, create a new child for the current node
        for number in numbArray:
            if number in node.children:
                node = node.children[number]
            else:
                # If a number is not found,
                # create a new node in the trie
                new_node = TrieNode(number)
                node.children[number] = new_node
                node.children[number].parent = node
                node.children[number].numberInSiblings = node.counterChildren
                node.counterChildren += 1
                node = new_node

        # Mark the end of a number array
        node.isEnd = True

    def key(self):
        return self.iterator.number

    def open(self):
        if not self.iterator.isEnd:
            self.iterator = self.iterator.children[list(self.iterator.children.keys())[0]]
        else:
            raise Exception('Cannot execute open(), already at a leaf node.')

    def up(self):
        if self.iterator.parent is not None:
            self.iterator = self.iterator.parent
        else:
            raise Exception('Cannot execute up(), already at the root.')

    def next(self):
        if self.key() is None:
            return
        currentPositionOnLevel = self.iterator.numberInSiblings
        nextPositionOnLevel = currentPositionOnLevel + 1
        if nextPositionOnLevel < self.iterator.parent.counterChildren:
            self.iterator = self.iterator.parent
            self.iterator = self.iterator.children[list(self.iterator.children.keys())[nextPositionOnLevel]]
        else:
            return 'next() - atEnd'

    def seek(self, seekKey):
        currentKey = self.key()
        if currentKey is None:
            return
        if currentKey <= seekKey:
            currentPositionOnLevel = self.iterator.numberInSiblings
            self.iterator = self.iterator.parent
            seekArray = list(self.iterator.children.keys())
            if seekArray[-1] < seekKey:
                self.iterator = self.iterator.children[seekArray[-1]]
                return 'seek() - atEnd'
            else:
                seekKeyIndex = binary_search(seekArray, currentPositionOnLevel, self.iterator.counterChildren - 1,
                                             seekKey)
                self.iterator = self.iterator.children[seekArray[seekKeyIndex]]
        else:
            raise Exception('seekKey must be >= key at current position')

    def position(self, context):
        """Given an input (a context), position iterator accordingly
        """
        node = self.root

        # Check if the context is in the trie
        for number in context:
            if number in node.children:
                node = node.children[number]
            elif [None] == list(node.children.keys()):
                node = node.children[None]
            else:
                # cannot find the context
                raise Exception('Context does not exist in trie.')

        self.iterator = node

    def payload(self):
        if self.iterator.isEnd:
            return 1
        else:
            raise Exception('payload() can only be called when iterator is positioned at a leaf node.')
        # tuple_context = []
        # node = self.iterator
        # tuple_context.append(node.number)
        # while node.parent is not None:
        #     node = node.parent
        #     tuple_context.append(node.number)
        # tuple_context = tuple_context[:-1]
        # tuple_context.reverse()


class TrieSemiring(object):
    """The trie object"""

    def __init__(self, factorMapping):
        """
        The trie has at least the root node.
        The root node does not store any number
        """
        self.root = TrieNode("")
        self.iterator = self.root
        self.factorMapping = factorMapping

    def insert(self, numbArray):
        """Insert a number array into the trie"""
        node = self.root

        # Loop through each number in the number array
        # Check if there is no child containing the number, create a new child for the current node
        for number in numbArray:
            if number in node.children:
                node = node.children[number]
            else:
                # If a number is not found,
                # create a new node in the trie
                new_node = TrieNode(number)
                node.children[number] = new_node
                node.children[number].parent = node
                node.children[number].numberInSiblings = node.counterChildren
                node.counterChildren += 1
                node = new_node

        # Mark the end of a number array
        node.isEnd = True

    def key(self):
        return self.iterator.number

    def open(self):
        if not self.iterator.isEnd:
            self.iterator = self.iterator.children[list(self.iterator.children.keys())[0]]
        else:
            raise Exception('Cannot execute open(), already at a leaf node.')

    def up(self):
        if self.iterator.parent is not None:
            self.iterator = self.iterator.parent
        else:
            raise Exception('Cannot execute up(), already at the root.')

    def next(self):
        if self.key() is None:
            return
        currentPositionOnLevel = self.iterator.numberInSiblings
        nextPositionOnLevel = currentPositionOnLevel + 1
        if nextPositionOnLevel < self.iterator.parent.counterChildren:
            self.iterator = self.iterator.parent
            self.iterator = self.iterator.children[list(self.iterator.children.keys())[nextPositionOnLevel]]
        else:
            return 'next() - atEnd'

    def seek(self, seekKey):
        currentKey = self.key()
        if currentKey is None:
            return
        if currentKey <= seekKey:
            currentPositionOnLevel = self.iterator.numberInSiblings
            self.iterator = self.iterator.parent
            seekArray = list(self.iterator.children.keys())
            if seekArray[-1] < seekKey:
                self.iterator = self.iterator.children[seekArray[-1]]
                return 'seek() - atEnd'
            else:
                seekKeyIndex = binary_search(seekArray, currentPositionOnLevel, self.iterator.counterChildren - 1,
                                             seekKey)
                self.iterator = self.iterator.children[seekArray[seekKeyIndex]]
        else:
            raise Exception('seekKey must be >= key at current position')

    def position(self, context):
        """Given an input (a context), position iterator accordingly
        """
        node = self.root

        # Check if the context is in the trie
        for number in context:
            if number in node.children:
                node = node.children[number]
            elif [None] == list(node.children.keys()):
                node = node.children[None]
            else:
                # cannot find the context
                raise Exception('Context does not exist in trie.')

        self.iterator = node

    def payload(self, mode):
        if self.iterator.isEnd:
            if mode == 'normal':
                return 1
            else:
                if self.factorMapping == 'normal':
                    return 1
                else:
                    tuple_context = []
                    node = self.iterator
                    tuple_context.append(node.number)
                    while node.parent is not None:
                        node = node.parent
                        tuple_context.append(node.number)
                    tuple_context = tuple_context[:-1]
                    tuple_context.reverse()
                    if mode == 'avgRating':
                        return tuple_context[-2]
                    elif mode == 'numVotes':
                        return tuple_context[-1]
        else:
            raise Exception('payload() can only be called when iterator is positioned at a leaf node.')


# Name: Roy Kim
# OSU Email: kimroy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/3/2022
# Description: Hash Map Separate Chaining Implementation


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        updates key/value pair in hash map.
        if given key already exists, associated value is replaced.
        if given key is not in hash map, key/value pair is added.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if not self._buckets.get_at_index(index).contains(key):
            self._buckets.get_at_index(index).insert(key, value)
            self._size += 1
        else:
            self._buckets.get_at_index(index).remove(key)
            self._buckets.get_at_index(index).insert(key, value)

    def empty_buckets(self) -> int:
        """
        returns number of empty buckets in hash table.
        """
        count = 0
        for i in range(self._capacity):
            if self._buckets.get_at_index(i).length() == 0:
                count += 1
        
        return count

    def table_load(self) -> float:
        """
        returns current hash table load factor.
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        clears the contents of the hash map.
        does not change hash table capacity.
        """
        for i in range(self._capacity):
            for node in self._buckets.get_at_index(i):
                self._buckets[i].remove(node.key)
                self._size -= 1

    def resize_table(self, new_capacity: int) -> None:
        """
        changes capacity of internal hash table.
        all existing key/value pairs remain in new hash map, and all hash table links are rehashed.
        if new_capacity is less than 1, method does nothing.
        """
        if new_capacity < 1:
            return

        node_list = LinkedList()
        rehashed_tbl = DynamicArray()

        for i in range(new_capacity):
            rehashed_tbl.append(LinkedList())

        for i in range(self._capacity):
            if self._buckets.get_at_index(i) != None:
                for node in self._buckets.get_at_index(i):
                    node_list.insert(node.key, node.value)
        
        self._buckets = rehashed_tbl
        self._capacity = new_capacity
        self._size = 0

        for node in node_list:
            self.put(node.key, node.value)

    def get(self, key: str) -> object:
        """
        returns the value associated with the given key.
        if the key is not in the hash map, returns None.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if not self._buckets.get_at_index(index).contains(key):
            return None

        for node in self._buckets.get_at_index(index):
            if node.key == key:
                return node.value

    def contains_key(self, key: str) -> bool:
        """
        returns True if given key is in hash map, otherwise returns False.
        empty hash map does not contain any keys.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets.get_at_index(index).contains(key):
            return True

        return False

    def remove(self, key: str) -> None:
        """
        removes the given key and associated value from hash map.
        if key is not in hash map, method does nothing.
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        
        if self._buckets.get_at_index(index).contains(key):
            self._buckets.get_at_index(index).remove(key)
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        returns a DynamicArray containing all keys stored in the hash map.
        order of keys does not matter.
        """
        keys = DynamicArray()
        for i in range(self._buckets.length()):
            for node in self._buckets.get_at_index(i):
                keys.append(node.key)

        return keys

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    receives any DynamicArray and  returns a tuple containing a DynamicArray comprising
    the mode value of the array and an integer representing the highest frequency.

    if more than one value have the highest frequency, all values at that frequency are returned.
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap(da.length() // 3, hash_function_1)

    for i in range(da.length()):
        counter = 0
        for j in range(da.length()):
            if da[i] == da[j]:
                counter += 1
        map.put(da[i], counter)

    freq = 0
    for i in range(map._buckets.length()):
        for node in map._buckets.get_at_index(i):
            if node.value > freq:
                freq = node.value
    
    modes = DynamicArray()
    for i in range(map._buckets.length()):
        for node in map._buckets.get_at_index(i):
            if node.value == freq:
                modes.append(node.key)
    
    return (modes, freq)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")

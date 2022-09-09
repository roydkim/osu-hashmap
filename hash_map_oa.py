# Name: Roy Kim
# OSU Email: kimroy@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/3/2022
# Description: Hash Map Open Addressing Implementation


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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
        if given key already exists in hash map, the associated value is replaced.
        if given key does not exists in hash map, key/value pair is added.
        """
        # remember, if the load factor is greater than or equal to 0.5,
        # resize the table before putting the new key/value pair
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        count = 0
        node = HashEntry(key, value)
        hash = self._hash_function(key) % self._capacity
        index = hash

        while count <= self._capacity:
            if self._buckets.get_at_index(index) == None or self._buckets.get_at_index(index).is_tombstone:
                self._buckets.set_at_index(index, node)
                self._size += 1
                break
            else:
                if key == self._buckets.get_at_index(index).key:
                    self._buckets.get_at_index(index).value = value
                    break
                else:
                    count += 1
                    index = (hash + (count * count)) % self._capacity

    def table_load(self) -> float:
        """
        returns the current hash table load factor.
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        returns the number of empty buckets in hash table.
        """
        count = 0
        for i in range(self._capacity):
            if self._buckets.get_at_index(i) == None:
                count += 1
        
        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        changes capacity of internal hash table.
        all existing key/value pairis remain in new hash map, and all hash table links are rehashed.
        if new_capacity is less than 1, or less than the current number of elements in the map, the method does nothing.
        """
        # remember to rehash non-deleted entries into new table
        if new_capacity < 1 or new_capacity < self._size:
            return

        node = HashEntry(0, 0)
        old_buckets = self._buckets
        rehashed_tbl = DynamicArray()
        for i in range(new_capacity):
            rehashed_tbl.append(None)

        self._buckets = rehashed_tbl
        old_capacity = self._capacity
        self._capacity = new_capacity
        self._size = 0

        for i in range(old_capacity):
            if old_buckets.get_at_index(i) != None:
                if not old_buckets.get_at_index(i).is_tombstone:
                    node.key = old_buckets.get_at_index(i).key
                    node.value = old_buckets.get_at_index(i).value
                    self.put(node.key, node.value)

    def get(self, key: str) -> object:
        """
        returns the value associated with given key.
        if key does not exist in hash map, method returns None.
        """
        count = 1
        hash = self._hash_function(key) % self._capacity
        index = hash

        while count <= self._capacity:
            if self._buckets.get_at_index(index) != None:
                if not self._buckets.get_at_index(index).is_tombstone:
                    if self._buckets.get_at_index(index).key == key:
                        return self._buckets.get_at_index(index).value

            index = (hash + (count*count)) % self._capacity
            count += 1
        
        return None

    def contains_key(self, key: str) -> bool:
        """
        returns True if given key is in hash map, otherwise returns False.
        an empty hash map does not contain any keys.
        """
        if self._buckets.length() == 0:
            return False

        count = 0
        hash = self._hash_function(key) % self._capacity
        index = hash

        while count <= self._capacity:
            if self._buckets.get_at_index(index) != None:
                if not self._buckets.get_at_index(index).is_tombstone:
                    if self._buckets.get_at_index(index).key == key:
                        return True
            count += 1
            index = (hash + (count*count)) % self._capacity
        
        return False

    def remove(self, key: str) -> None:
        """
        removes the given key and its associated value from hash map.
        if key does not exist in hash map, method does nothing.
        """
        pass

    def clear(self) -> None:
        """
        clears the contents of the hash map.
        does not change hash table capacity.
        """
        for i in range(self._capacity):
            self._buckets.set_at_index(i, None)
        
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """
        returns a DynamicArray containing all the keys stored in hash map.
        order of keys does not matter.
        """
        keys = DynamicArray()

        for i in range(self._capacity):
            if self._buckets.get_at_index(i) != None:
                keys.append(self._buckets.get_at_index(i).key)

        return keys


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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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

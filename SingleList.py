from typing import Any, Generator, Iterable


class SingleList:
    class Node:
        def __init__(self, val):
            self.next: SingleList.Node = None
            self.val: int = val

        def __str__(self):
            return str(self.val)

    def __init__(self, val=None, *args):
        self.__head: SingleList.Node = None
        self.__tail: SingleList.Node = None

        if val:
            self.__iadd__(val)
            for i in args:
                self.__iadd__(i)

    def append(self, other, *args) -> None:

        if not self.__head:
            self.__head = SingleList.Node(other)
            self.__tail = self.__head
        else:
            self.__tail.next = SingleList.Node(other)
            self.__tail = self.__tail.next

        for i in args:
            self.append(i)
    push = append

    def empty(self) -> bool:
        return self.__head is None

    def length(self) -> int:
        __length = 0
        for i in self:
            __length += 1
        return __length
    __len__ = length

    def add(self, other):
        __list = self.copy()
        __list.__iadd__(other)
        return __list
    __add__ = add

    def pop(self) -> Any:
        for i in self.__nodes():
            if i.next == self.__tail:
                __re = i.next.val
                del i.next
                i.next = None
                self.__tail = i
                return __re
        else:
            if self.__head and self.__head == self.__tail:
                __re = self.__head.val
                del self.__head
                self.__head = None
                self.__tail = None
                return __re
            else:
                raise IndexError('pop from empty list')

    def popn(self, n: int):
        __list = SingleList()
        __from = self.copy()
        if n > self.length():
            raise IndexError('invaild amount to pop')
        for i in range(n):
            __list.append(__from.pop())
        return __list
    __sub__ = popn

    def copy(self):
        __list = SingleList()
        for i in self:
            __list.append(i)
        return __list

    def copyn(self, n: int):
        __list = SingleList()
        for i in range(n):
            __list.__iadd__(self.copy())
        return __list

    def slice(self, n: slice):
        __list = SingleList()
        n = n.indices(self.length())
        for i, j in zip(range(0, n[1]), self):
            if i >= n[0] and not (i-n[0]) % n[2]:
                __list.append(j)
        return __list

    def setn(self, n: slice, other) -> None:
        n, other = n.indices(self.length()), iter(other)
        for i, j in zip(range(0, n[1]), self.__nodes()):
            if i >= n[0] and not (i-n[0]) % n[2]:
                j.val = next(other)

    def get(self, n) -> Any:
        if type(n) is slice:
            return self.slice(n)
        else:
            return self.__noden(n).val
    __getitem__ = get

    def set(self, n, val: Any) -> None:
        if type(n) is slice:
            self.setn(n, val)
        else:
            self.__noden(n).val = val
    __setitem__ = set

    def remove(self, n: int):
        __p = self.__noden(n)

        if self.__head and self.__head == self.__tail:
            del __p
            self.__head = None
            self.__tail = None
        elif __p == self.__head:
            self.__head = __p.next
            del __p
        else:
            __p = self.__noden(n-1)
            del __p.next
            __p.next = None
    __delitem__ = remove

    def __radd__(self, other):
        __list = SingleList()
        __list.__iadd__(other)
        __list.__iadd__(self)
        return __list

    def __iadd__(self, other):
        if isinstance(other, Iterable):
            for i in other:
                self.append(i)
        else:
            self.append(other)
        return self

    def __isub__(self, n: int):
        if n > self.length():
            raise IndexError('invaild amount to pop')
        for i in range(n):
            self.pop()
        return self

    def __imul__(self, n: int):
        self.__iadd__(self.copyn(n-1))

    def __str__(self) -> str:
        __str = ''
        for i in self.__nodes():
            if i == self.__tail:
                __str += f'{i}'
            else:
                __str += f'{i} -> '
        return f'[{__str}]'

    def __noden(self, n) -> Node:
        for i in self.__nodes():
            if not n:
                return i
            n -= 1
        else:
            raise IndexError('list index out of range')

    def __nodes(self) -> Generator:
        __p = self.__head
        while __p:
            yield __p
            __p = __p.next

    def __iter__(self) -> Generator:
        __p = self.__head
        while __p:
            yield __p.val
            __p = __p.next


if __name__ == '__main__':
    # 空列表
    A = SingleList()
    print(f'A: {A}')
    # 位置参数初始化
    B = SingleList(1, 2, 3)
    print(f'B: {B}')
    # 任意迭代器初始化
    C = SingleList([1, 2, 3])
    print(f'C: {C}')
    # 添加元素的两种方法
    C.append(4)
    C.push(5)
    C += 6
    print(f'C: {C}')
    # 长度的两种获取方法
    C -= 1
    D = C.length()
    E = len(C)
    print(f'D: {D}, E: {E}')
    F = C[1:4:2]
    print(f'F: {F}')
    C[1:3] = [9, 8]
    print(f'C: {C}, {C[1:3]}')

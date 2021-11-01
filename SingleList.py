from __future__ import annotations

from typing import Any, Generator, Iterable


class SingleList:
    class Node:
        def __init__(self, val: Any):
            self.next: SingleList.Node = None
            self.val: int = val

        def __str__(self):
            return str(self.val)

    def __init__(self, val: Any = None, *args):
        self.__head: SingleList.Node = None
        self.__tail: SingleList.Node = None

        if val:
            self.__iadd__(val)
            for i in args:
                self.__iadd__(i)

    def append(self, val: Any, *args) -> None:
        '''添加元素'''
        if not self.__head:
            self.__head = SingleList.Node(val)
            self.__tail = self.__head
        else:
            self.__tail.next = SingleList.Node(val)
            self.__tail = self.__tail.next

        for i in args:
            self.append(i)
    push = append

    def empty(self) -> bool:
        '''单链表是否为空'''
        return self.__head is None

    def length(self) -> int:
        '''单链表的长度，也可以使用 len() 获取'''
        __length = 0
        for i in self:
            __length += 1
        return __length
    __len__ = length

    def insert(self, n: int, val: Any) -> None:
        '''在位置 n 后添加一元素 val'''
        __p = self.__node(n)
        if __p == self.__tail:
            # 调用 SingleList.append() 方法，以便移动 __tail 指针
            self.append(val)
        else:
            __tmp = __p.next
            __p.next = SingleList.Node(val)
            __p.next.next = __tmp

    def add(self, other: Iterable | Any) -> SingleList:
        '''与 other 进行连接，若 other 是一迭代器，则将其元素添加至单链表'''
        __list = self.copy()
        __list.__iadd__(other)
        return __list
    __add__ = add

    def pop(self) -> Any:
        '''删除一个元素，返回值是该元素的值'''
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

    def copy(self) -> SingleList:
        '''返回自身的拷贝'''
        __list = SingleList()
        for i in self:
            __list.append(i)
        return __list

    def get(self, n: slice | Node) -> Any:
        if type(n) is slice:
            return self.get_n(n)
        else:
            return self.__node(n).val
    __getitem__ = get

    def set(self, n: slice | int, val: Any) -> None:
        if type(n) is slice:
            self.set_n(n, val)
        else:
            self.__node(n).val = val
    __setitem__ = set

    def remove(self, n: int):
        __p = self.__node(n)

        if self.__head and self.__head == self.__tail:
            del __p
            self.__head = None
            self.__tail = None
        elif __p == self.__head:
            self.__head = __p.next
            del __p
        else:
            __p = self.__node(n-1)
            del __p.next
            __p.next = None

    def pop_n(self, n: int) -> SingleList:
        '''删除 n 个元素，返回由该 n 个元素组成的单链表'''
        __list = SingleList()
        __from = self.copy()
        if n > self.length():
            raise IndexError('invaild amount to pop')
        for i in range(n):
            __list.append(__from.pop())
        return __list
    __sub__ = pop_n

    def copy_n(self, n: int) -> SingleList:
        '''返回自身的 n 次拷贝'''
        __list = SingleList()
        for i in range(n):
            __list.__iadd__(self.copy())
        return __list

    def get_n(self, n: slice):
        '''切片操作，返回由切片的元素组成的 SingleList'''
        __list = SingleList()
        n = n.indices(self.length())
        for i in range(n[0], n[1], n[2]):
            __list.append(self.get(i))
        return __list

    def set_n(self, n: slice, other: Iterable) -> None:
        '''对 n 对应的切片元素进行赋值操作，other 为任意的迭代器'''
        n = n.indices(self.length())
        for i, j in zip(range(n[0], n[1], n[2]), other):
            self.__node(i).val = j

    def remove_n(self, n: slice) -> None:
        n = n.indices(self.length())
        for i in range(n[0], n[1], n[2]):
            self.remove(i)

    def __delitem__(self, n: slice | int):
        if type(n) is slice:
            return self.remove_n(n)
        else:
            return self.remove(n)

    def __radd__(self, other: Any):
        __list = SingleList()
        __list.__iadd__(other)
        __list.__iadd__(self)
        return __list

    def __iadd__(self, other: Iterable | Any):
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
        self.__iadd__(self.copy_n(n-1))

    def __str__(self) -> str:
        __str = ''
        for i in self.__nodes():
            if i == self.__tail:
                __str += f'{i}'
            else:
                __str += f'{i} -> '
        return f'[{__str}]'

    def __node(self, n: int) -> Node:
        for i in self.__nodes():
            if not n:
                return i
            n -= 1
        else:
            raise IndexError('list index out of range')

    def __nodes(self) -> Generator[Node]:
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
    C[1:3] = [9, 8, 3]
    C.insert(1, 'Inserted')
    print(f'C: {C}, {C[1:3]}')

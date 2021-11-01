from __future__ import annotations

from typing import Any, Generator, Iterable


class SingleList:
    class Node:
        def __init__(self, val: Any):
            self.next: SingleList.Node = None
            self.val: int = val

        def __str__(self):
            return str(self.val)

    def __init__(self, *args) -> None:
        # 为了简化逻辑，这里仅维护头指针
        self.__head: SingleList.Node = None

        for i in args:
            self.__iadd__(i)

    def append(self, val: Any, *args) -> None:
        '''添加元素'''
        if not self.__head:
            self.__head = SingleList.Node(val)
        else:
            self.__tail().next = SingleList.Node(val)

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
            if not i.next.next:
                __re = i.next.val
                del i.next
                i.next = None
                return __re
        else:
            if self.__head:
                __re = self.__head.val
                del self.__head
                self.__head = None
                return __re
            else:
                raise IndexError('pop from empty list')

    def copy(self) -> SingleList:
        '''返回自身的拷贝'''
        __list = SingleList()
        for i in self:
            __list.append(i)
        return __list

    def get(self, n: slice | int) -> Any:
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

    def remove(self, n: int | Node) -> None:
        if type(n) is SingleList.Node:
            __p = n
        else:
            __p = self.__node(n)

        if __p == self.__head:
            self.__head = __p.next
            del __p
        else:
            __p = self.__node(n-1)
            __tmp = __p.next.next
            del __p.next
            __p.next = __tmp

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

    def get_n(self, n: slice) -> SingleList:
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
        __n = SingleList()
        n = n.indices(self.length())
        for i in range(n[0], n[1], n[2]):
            __n.append(self.__node(i))
        for i in __n:
            self.remove(i)

    def __delitem__(self, n: slice | int):
        if type(n) is slice:
            return self.remove_n(n)
        else:
            return self.remove(n)

    def __radd__(self, other: Any) -> SingleList:
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

    def __isub__(self, n: int) -> SingleList:
        if n > self.length():
            raise IndexError('invaild amount to pop')
        for i in range(n):
            self.pop()
        return self

    def __imul__(self, n: int) -> SingleList:
        self.__iadd__(self.copy_n(n-1))
        return self

    def __str__(self) -> str:
        __str = ''
        for i in self.__nodes():
            if i.next:
                __str += f'{i} -> '
            else:
                __str += f'{i}'
        return f'[{__str}]'

    def __tail(self) -> Node:
        __p = self.__head
        while __p.next:
            __p = __p.next
        return __p

    def __node(self, n: int) -> Node:
        '''返回位于 n 的节点指针'''
        for i in self.__nodes():
            if not n:
                return i
            n -= 1
        else:
            raise IndexError(f'list index out of range')

    def __nodes(self) -> Generator[Node]:
        '''返回包含所有节点指针的迭代器'''
        __p = self.__head
        while __p:
            yield __p
            __p = __p.next

    def __iter__(self) -> Generator:
        '''返回所有节点的 *值*'''
        __p = self.__head
        while __p:
            yield __p.val
            __p = __p.next


if __name__ == '__main__':
    A = SingleList(0, 1, 2, 3, 4, 5)
    del A[0:4]
    A.append(SingleList(1, 2, 3))
    print(A)

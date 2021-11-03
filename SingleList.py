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
        '''初始化此单链表，可以使用任意 值/迭代器 进行初始化'''
        # 为了简化逻辑，这里仅维护头指针
        self.__head: SingleList.Node = None

        for i in args:
            self.__iadd__(i)

    def append(self, val: Any, *args) -> None:
        '''在此单链表末尾添加元素。若元素也是一个迭代器，则不对其进行解包，语义与 Python 内置列表相同'''
        if not self.__head:
            self.__head = SingleList.Node(val)
        else:
            self.__tail().next = SingleList.Node(val)

        for i in args:
            self.append(i)
    push = append

    def empty(self) -> bool:
        '''检测此单链表是否为空'''
        return self.__head is None

    def length(self) -> int:
        '''计算此单链表的长度'''
        __length = 0
        for i in self:
            __length += 1
        return __length
    __len__ = length

    def insert(self, n: int | Node, val:  Any) -> None:
        '''在此链表位置 n 的元素后添加一元素 val'''
        if type(n) is SingleList.Node:
            __temp = n.next
            n.next = SingleList.Node(val)
            n.next.next = __temp
        else:
            __p = self.__node(n)
            self.insert(__p, val)

    def add(self, other: Iterable | Any) -> SingleList:
        '''此处的 add 方法语义是与迭代器或值做加法运算，此单链表的特殊方法 __add__ 即是使用此方法'''
        __list = self.copy()
        __list.__iadd__(other)
        return __list
    __add__ = add

    def pop(self) -> Any:
        '''删除此单链表末尾的一个元素，并返回该元素的值'''
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
        '''获取此单链表的拷贝'''
        __list = SingleList()
        for i in self:
            __list.append(i)
        return __list

    def get(self, n: slice | int) -> Any:
        '''此处的 get 方法语义与特殊方法 __getitem__ 相同，可以进行伪随机访问和切片的操作'''
        if type(n) is slice:
            return self.get_n(n)
        else:
            return self.__node(n).val
    __getitem__ = get

    def set(self, n: slice | int, val: Any) -> None:
        '''此处的 set 方法语义与特殊方法 __setitem__ 相同，进行伪随机赋值和伪切片赋值的操作'''
        if type(n) is slice:
            self.set_n(n, val)
        else:
            self.__node(n).val = val
    __setitem__ = set

    def remove(self, n: int | Node) -> None:
        '''删除位置为 n 或节点指针为 n 的元素'''
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
        '''删除此单链表末尾 n 个元素，返回由该 n 个元素组成的逆序单链表'''
        __list = SingleList()
        __from = self.copy()
        if n > self.length():
            raise IndexError('invaild amount to pop')
        for i in range(n):
            __list.append(__from.pop())
        return __list
    __sub__ = pop_n

    def copy_n(self, n: int) -> SingleList:
        '''获取此单链表的 n 重拷贝'''
        __list = SingleList()
        for i in range(n):
            __list.__iadd__(self.copy())
        return __list

    def get_n(self, n: slice) -> SingleList:
        '''切片方法，返回切片元素组成的单链表'''
        __list = SingleList()
        n = n.indices(self.length())
        for i in range(n[0], n[1], n[2]):
            __list.append(self.get(i))
        return __list

    def set_n(self, n: slice, other: Iterable) -> None:
        '''切片赋值方法，将切片的元素赋值为迭代器 other 中的各值'''
        if not isinstance(other, Iterable):
            raise TypeError('can only assign an iterable')
        n = n.indices(self.length())
        other = iter(other)
        __p: SingleList.Node = None
        for i, j in zip(range(n[0], n[1], n[2]), other):
            __p = self.__node(i)
            __p.val = j
        for j in other:
            self.insert(__p, j)
            __p = __p.next

    def remove_n(self, n: slice) -> None:
        '''删除切片对应的元素'''
        __n = SingleList()
        n = n.indices(self.length())
        for i in range(n[0], n[1], n[2]):
            __n.append(self.__node(i))
        for i in __n:
            self.remove(i)

    def __delitem__(self, n: slice | int) -> None:
        if type(n) is slice:
            return self.remove_n(n)
        else:
            return self.remove(n)

    def __radd__(self, other: Any) -> SingleList:
        __list = SingleList()
        __list.__iadd__(other)
        __list.__iadd__(self)
        return __list

    def __iadd__(self, other: Iterable | Any) -> SingleList:
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
    __repr__ = __str__

    def __tail(self) -> Node:
        '''获取此单链表的尾指针'''
        __p = self.__head
        while __p.next:
            __p = __p.next
        return __p

    def __node(self, n: int) -> Node:
        '''获取此单链表位于 n 的结点指针'''
        for i in self.__nodes():
            if not n:
                return i
            n -= 1
        else:
            raise IndexError(f'list index out of range')

    def __nodes(self) -> Generator[Node]:
        '''获取一个包含所有节点指针的迭代器'''
        __p = self.__head
        while __p:
            yield __p
            __p = __p.next

    def __iter__(self) -> Generator:
        '''返回所有节点的值'''
        __p = self.__head
        while __p:
            yield __p.val
            __p = __p.next


if __name__ == '__main__':
    A = SingleList()
    A += 1, 2, 3
    A.append(SingleList(1, 2, 3))
    A.pop()
    A += 4, 5, 6
    A[-2:] = 7, 8
    del A[:-2]
    print(A)

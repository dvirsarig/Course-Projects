class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

class Linked:
    def __init__(self):
        self.head = Node()

    def append(self, data):
        new_node = Node(data)
        cur = self.head
        while cur.next is not None:
            cur = cur.next
        cur.next = new_node

    def display(self):
        lst = []
        cur = self.head
        while cur.next is not None:
            cur = cur.next
            lst.append(cur.data)
        print(lst)


def linked_tru(func, lnk):
    new_list = Linked()
    cur_node = lnk.head
    while cur_node.next is not None:
        cur_node = cur_node.next
        if func(cur_node.data):
            new_list.append(cur_node.data)
    return new_list.display()


linked_lst = Linked()
linked_lst.append(2)
linked_lst.append(3)
linked_lst.append(4)
linked_lst.append(5)
linked_lst.append(6)
linked_lst.display()
linked_tru(lambda x: x % 2 == 0, linked_lst)





















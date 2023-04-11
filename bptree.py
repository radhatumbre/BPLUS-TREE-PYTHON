
class Node:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf

class BPlusTree:
    def __init__(self, degree):
        self.degree = degree
        self.root = Node(leaf=True)

    def insert(self, key):
        node = self.root
        if len(node.keys) == (2 * self.degree) - 1:
            new_node = Node()
            self.root = new_node
            new_node.children.append(node)
            self._split_child(new_node, 0, node)
            self._insert_non_full(new_node, key)
        else:
            self._insert_non_full(node, key)

    def _split_child(self, parent, index, node):
        new_node = Node(leaf=node.leaf)
        parent.children.insert(index + 1, new_node)
        parent.keys.insert(index, node.keys[self.degree - 1])
        new_node.keys = node.keys[self.degree:(2 * self.degree) - 1]
        node.keys = node.keys[0:self.degree - 1]

        if not node.leaf:
            new_node.children = node.children[self.degree:(2 * self.degree)]
            node.children = node.children[0:self.degree - 1]

    def _insert_non_full(self, node, key):
        index = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while index >= 0 and key < node.keys[index]:
                node.keys[index + 1] = node.keys[index]
                index -= 1
            node.keys[index + 1] = key
        else:
            while index >= 0 and key < node.keys[index]:
                index -= 1
            index += 1
            if len(node.children[index].keys) == (2 * self.degree) - 1:
                self._split_child(node, index, node.children[index])
                if key > node.keys[index]:
                    index += 1
            self._insert_non_full(node.children[index], key)




import tkinter as tk

degree = 3

class BPlusTreeGUI:
    global items
    def __init__(self, master):
        self.master = master
        self.master.title("B+ Tree")
        self.bptree = BPlusTree(degree-1)
        self.label = tk.Label(self.master, text="Enter a value to insert:")
        self.label.pack()
        self.entry = tk.Entry(self.master)
        self.entry.pack()
        self.button = tk.Button(self.master, text="Insert", command=self.insert)
        self.button.pack()
        self.canvas = tk.Canvas(self.master, width=800, height=600)
        self.canvas.pack()

    def insert(self):
        try:
            value = int(self.entry.get())
            self.bptree.insert(value)
            self.canvas.delete("all")
            self.draw_tree(self.bptree.root, 200, 50, 50, 50, 100)
            self.entry.delete(0, tk.END)
        except ValueError:
            pass

    def draw_tree(self, node, x, y, dx, dy, spacing):
        if node.leaf:
            self.draw_leaf_node(node, x, y, dx, dy)
        else:
            self.draw_non_leaf_node(node, x, y, dx, dy, spacing)

    def draw_leaf_node(self, node, x, y, dx, dy):
        text_size = 12
        keys = node.keys
        num_keys = len(keys)

        # Calculate position of first key
        first_x = x - (num_keys * dx) // 2 + 200
        first_y = y

        # Draw node rectangle
        self.canvas.create_rectangle(first_x , first_y, first_x + dx * num_keys, first_y + dy, fill="white", outline="black")

        # Draw keys
        for key in keys:
            text = str(key)
            self.canvas.create_text(first_x + dx // 2, first_y + dy // 2, text=text, font=("Arial", text_size))
            first_x += dx

    def draw_non_leaf_node(self, node, x, y, dx, dy, spacing):
        text_size = 12
        keys = node.keys
        num_children = len(node.children)

        # Calculate position of first child
        first_child_x = x - ((num_children - 1) * spacing) // 2

        # Draw node rectangle
        self.canvas.create_rectangle(x - dx // 2 + 200, y - dy // 2, x + dx // 2 + 200, y + dy // 2, fill="white", outline="black")

        # Draw node key
        text = ', '.join(str(key) for key in keys)
        self.canvas.create_text(x+200, y, text=text, font=("Arial", text_size))

        # Draw children
        y += dy
        child_x = first_child_x
        for child in node.children:
            self.draw_tree(child, child_x, y, dx, dy, spacing)
            self.canvas.create_line(x+200, y - dy // 2, child_x+200, y + dy // 2)
            child_x += spacing



if __name__ == "__main__":
    root = tk.Tk()
    gui = BPlusTreeGUI(root)
    root.mainloop()

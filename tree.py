# -*- coding: utf-8 -*-


class Tree:
    def __init__(self, data):
        self.tree = self.__generate(data)
        self.steps = dict()

    def __generate(self, data):
        if not data:
            raise Exception("empty data".format(data))
        elif self.__cyclic(data):
            raise Exception("cyclic DAG\n{}".format(data))
        elif not self.__cyclic(data):
            # 初始化树
            root_tree = Node('root')
            # 将无依赖的节点加入root子节点
            # 删除数据中的无依赖节点
            deletes = []
            for k in data.keys():
                if not data[k]:
                    root_tree.insert(k)
                    deletes.append(k)
            for k in deletes:
                del data[k]
            # 遍历剩余数据当剩余数据不为空
            while data:
                deletes = []
                for k in data.keys():
                    # 当全部父节点存在时 则插入子节点
                    if not any([False if root_tree.find(parent) else True for parent in data[k]]):
                        for parent in data[k]:
                            # 向父节点插入子节点
                            root_tree.find(parent).insert(k)
                        # 删除整个数据
                        deletes.append(k)
                for k in deletes:
                    del data[k]
            return root_tree

    @staticmethod
    def __cyclic(graph):
        """Return True if the directed graph has a cycle.
        The graph must be represented as a dictionary mapping vertices to
        iterables of neighbouring vertices. For example:

        >>> a = {
            "a": ["b"],
            "b": ["c"],
            "c": ["a", "d"],
            "d": []
        }
        True
        >>> a = {
            "a": ["b"],
            "b": ["c"],
            "c": ["d"],
            "d": []
        }
        False

        if bug raised, go visit
        https://codereview.stackexchange.com/questions/86021/check-if-a-directed-graph-contains-a-cycle
        """
        visited = set()
        path = [object()]
        path_set = set(path)
        stack = [iter(graph)]
        while stack:
            for v in stack[-1]:
                if v in path_set:
                    return True
                elif v not in visited:
                    visited.add(v)
                    path.append(v)
                    path_set.add(v)
                    stack.append(iter(graph.get(v, ())))
                    break
            else:
                path_set.remove(path.pop())
                stack.pop()
        return False

    def show_graph(self, delta=0, node=None):
        if node is None:
            node = self.tree
        print(" " * delta * 5 + "|" + "----" * 1 + node.name)
        for name, _node in node.children.items():
            self.show_graph(delta + 1, _node)

    def __generate_steps(self, delta=1, node=None):
        """递归生成发版步骤

            Parameters:
            delta (int): 第N步
            node (Node): 树节点

           """
        if node is None:
            node = self.tree
        if delta in self.steps:
            self.steps[delta].append({"name": node.name, "level": node.level})
        else:
            self.steps[delta] = [{"name": node.name, "level": node.level}]
        for name, _node in node.children.items():
            self.__generate_steps(delta + 1, _node)

    def show_steps(self):
        self.__generate_steps()
        step_1 = self.steps[1]
        del self.steps[1]
        tmp_steps = {}
        for key, val in self.steps.items():
            for index in range(len(val)):
                name = self.steps[key][index]["name"]
                level = self.steps[key][index]["level"]
                if name not in tmp_steps:
                    tmp_steps[name] = {"level": level, "key": key, "index": index}
                else:
                    if tmp_steps[name]['level'] < level:
                        tmp = tmp_steps[name]
                        tmp_steps[name] = {"level": level, "key": key, "index": index}
                        del self.steps[tmp["key"]][tmp["index"]]
        d = {}
        for key, items in self.steps.items():
            for item in items:
                if key not in d:
                    d[key] = [item["name"]]
                else:
                    d[key].append(item["name"])
        self.steps[1] = step_1
        steps = {}
        for index in d.keys():
            steps[index - 1] = [k for k in list(set(d[index]))]
        return steps


class Node:
    def __init__(self, name, level=1):
        self.name = name
        self.children = dict()
        self.level = level

    def insert(self, name):
        if name not in self.children:
            self.children[name] = Node(name, self.level + 1)

    def bulk_insert(self, names):
        for name in names:
            self.insert(name)

    def delete(self, name):
        if name in self.children:
            del self.children[name]

    def find(self, name):
        if name == self.name:
            return self
        else:
            for _name, _node in self.children.items():
                match = _node.find(name)
                if match:
                    return match
        return False

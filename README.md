This repo is a DevOps tool for examining whether the repos' dependencies of DAG is cyclic. Additionally, it will output a sequential structure for the priority of deployment for apps.

Devops检测发版前每个应用的依赖关系是否有向无环, 并且输出对应发版顺序
### 1. It will examine whether DAG of apps' dependencies is cyclic. (检测各个应用间是否有向无环) 
### 2. It will output the sequence of apps' deploment. (输出发版顺序)
### 3. I'm new to python, I wrote the code with mannual, Google and SO. Hope it works fine. (我是菜逼)

### 4. Input
The input is a dictionary, key is the app you want to deploy and its value(list) is the dependency.

初始化结构是一个字典, key是你想发布的app名称, 值是一个list, 里面是其依赖的app, 无依赖传空list
```
a = {
    "a": ["c", "d"], # a depends on c and d 
    "b": ["f"],      # you should deploy f before b
    "c": [],         # it could be deployed at the first
    "d": [],
    "e": ["b", "g"],
    "f": [],
    "g": ["a", "b"],
    "h": ["c"],
    "j": ["g"],
    "k": ["j"]
}
```
### 5. Usage
```
from tree import Tree
a = {
    "a": ["c", "d"],
    "b": ["f"],
    "c": [],
    "d": [],
    "e": ["b", "g"],
    "f": [],
    "g": ["a", "b"],
    "h": ["c"],
    "j": ["g"],
    "k": ["j"]
}
tree = Tree(a)
tree.show_graph()
print(tree.show_steps())
```
```
# situation 1
a = {}
tree = Tree(a)
tree.show_graph()
print(tree.show_steps())
print(time.time() - start)
# This will raise an expection of empty data

# situation 2
a = {"a":["a"]}
tree = Tree(a)
tree.show_graph()
print(tree.show_steps())
print(time.time() - start)
# This will raise an expection of cyclic DAG

# situation 3
a = {
    "a": ["c", "d"],
    "b": ["f"],
    "c": [],
    "d": [],
    "e": ["b", "g"],
    "f": [],
    "g": ["a", "b"],
    "h": ["c"],
    "j": ["g"],
    "k": ["j"]
}
tree = Tree(a)
tree.show_graph()
print(tree.show_steps())
# This will return a normal tree structure and the sequence as below
|----root
     |----c
          |----a
               |----g
                    |----j
                         |----k
                    |----e
          |----h
     |----d
          |----a
     |----f
          |----b
               |----e
               |----g
{1: ['c', 'd', 'f'], 2: ['a', 'h', 'b'], 3: ['e', 'g'], 4: ['j'], 5: ['k']}
```

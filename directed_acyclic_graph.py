import networkx as nx
import matplotlib.pyplot as plt

class DAG:
    def __init__(self):
        self.dag = nx.DiGraph()
        
    def add_node(self, node):
        self.dag.add_node(node)
        
    def add_edge(self, source, target):
        self.dag.add_edge(source, target)

    def is_dag(self):
        return nx.is_directed_acyclic_graph(self.dag)
        
    def topological_division(self):
        stack1 = []
        stack2 = []
        
        for node, in_degree in self.dag.in_degree():
            if in_degree == 0:
                stack1.append(node)
            
        while stack1:
            node = stack1.pop()
            stack2.append(node)
            
            self.dag.remove_node(node)
            
            for new_0_in_degree_node, in_degree in self.dag.in_degree():
                if in_degree == 0:
                    stack1.append(new_0_in_degree_node)
                    
        divisions = []
        while stack2:
            division = []
            while stack2:
                node = stack2.pop()
                division.append(node)
            divisions.append(division)
        
        return divisions    
    
    def plot(self):
        pos = nx.spring_layout(self.dag)
        nx.draw(self.dag, pos, with_labels=True, node_size=1000, node_color="lightblue", font_size=12, font_color="black")
        plt.title("Directed Acyclic Graph (DAG)")
        plt.show()
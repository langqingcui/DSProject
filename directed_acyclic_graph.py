import networkx as nx

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
        if not self.is_dag:
            return None
        
        # List to store nodes at each division
        divisions = []
        
        while True:
            # Find nodes with in-degrees of 0
            zero_in_degree_nodes = [node for node, in_degree in self.dag.in_degree() if in_degree == 0]
            
            # Break if there are no nodes with in-degree of 0
            # Indicating the process has completed
            if not zero_in_degree_nodes:
                break
            
            # Store this level of nodes into list
            divisions.append(zero_in_degree_nodes)       
            
            # Remove all the 0 in-degree nodes
            for node in zero_in_degree_nodes:
                self.dag.remove_node(node)
        
        return divisions    

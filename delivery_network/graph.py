class Graph: 

    """ 

    A class representing graphs as adjacency lists and implementing various algorithms on the graphs. Graphs in the class are not oriented.  

    Attributes:  

    ----------- 

    nodes: NodeType 

        A list of nodes. Nodes can be of any immutable type, e.g., integer, float, or string. 

        We will usually use a list of integers 1, ..., n. 

    graph: dict 

        A dictionnary that contains the adjacency list of each node in the form 

        graph[node] = [(neighbor1, p1, d1), (neighbor1, p1, d1), ...] 

        where p1 is the minimal power on the edge (node, neighbor1) and d1 is the distance on the edge 

    nb_nodes: int 

        The number of nodes. 

    nb_edges: int 

        The number of edges.  

    """ 

 
 

    def __init__(self, nodes=[]): 

        """ 

        Initializes the graph with a set of nodes, and no edges.  

        Parameters:  

        ----------- 

        nodes: list, optional 

            A list of nodes. Default is empty. 

        """ 

        self.nodes = nodes 

        self.graph = dict([(n, []) for n in nodes]) 

        self.nb_nodes = len(nodes) 

        self.nb_edges = 0 

     

 
 

    def __str__(self): 

        """Prints the graph as a list of neighbors for each node (one per line)""" 

        if not self.graph: 

            output = "The graph is empty"             

        else: 

            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n" 

            for source, destination in self.graph.items(): 

                output += f"{source}-->{destination}\n" 

        return output 

     

    def add_edge(self, node1, node2, power_min, dist=1): 

        """ 

        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes.  

 
 

        Parameters:  

        ----------- 

        node1: NodeType 

            First end (node) of the edge 

        node2: NodeType 

            Second end (node) of the edge 

        power_min: numeric (int or float) 

            Minimum power on this edge 

        dist: numeric (int or float), optional 

            Distance between node1 and node2 on the edge. Default is 1. 

        """ 

         

        if node1 not in self.nodes: 

            self.nodes.append(node1) 

            self.graph[node1]=[] 

            self.nb_nodes+=1 

        if node2 not in self.nodes: 

            self.nodes.append(node2) 

            self.graph[node2]=[] 

            self.nb_nodes+=1 

        self.graph[node1].append((node2,power_min,dist)) 

        self.graph[node2].append((node1,power_min,dist)) 

        self.nb_edges+=1 

 
 

     

    def get_path_with_power(self, src, dest, power): 

        raise NotImplementedError 

     

 
 

    def connected_components(self): 

        raise NotImplementedError 

 
 
 

    def connected_components_set(self): 

        """ 

        The result should be a set of frozensets (one per component),  

        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})} 

        """ 

        return set(map(frozenset, self.connected_components())) 

     

    def min_power(self, src, dest): 

        """ 

        Should return path, min_power.  

        """ 

        raise NotImplementedError 

 
 
 

def graph_from_file(filename): 

    """ 

    Reads a text file and returns the graph as an object of the Graph class. 

 
 

    The file should have the following format:  

        The first line of the file is 'n m' 

        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default) 

        The nodes (node1, node2) should be named 1..n 

        All values are integers. 

 
 

    Parameters:  

    ----------- 

    filename: str 

        The name of the file 

 
 

    Outputs:  

    ----------- 

    G: Graph 

        An object of the class Graph with the graph from file_name. 

    """ 

    f = open("/home/onyxia/work/ensae-prog23/"+filename, "r") #On rajoute le début du chemin pour que le programme trouve le chemin du fichier 

    L = f.readlines()#On transforme le tableau en une liste de chaîne de caractères, avec une chaîne = une ligne 

    lignes=[] 

    g=Graph([]) 

    for i in range(1,len(L)): 

        lignes.append(L[i].split()) #"lignes" est une liste, donc les éléments (qui représentent les lignes de notre tableau) sont des listes de chaînes de caractères 

    for line in lignes: 

        if len(line)==3: 

            g.add_edge(int(line[0]),int(line[1]),int(line[2]),1) 

        else : 

            g.add_edge(int(line[0]),int(line[1]),int(line[2]),int(line[3])) 

    #Attention ! Tous les sommets ne sont pas forcément reliés à d'autres sommets ! Dans cette partie du code, on s'occupe de mettre dans le graphe les sommets isolés 

    nb_nodes=int(L[0].split()[0]) #Le nombre de sommets est donné par le premier nombre de la première ligne 

    for n in range(1,nb_nodes+1): #On suppose ici que s'il y a n noeuds, tous les noeuds sont exactement tous les numéros de 1 à n. 

        if n not in g.graph: 

            g.graph[n]=[] 

            g.nb_nodes+=1 #Le nombre d'arêtes n'a pas été modifié, mais le nombre de sommets a lui changé 

    return g 
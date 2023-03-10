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
         
         #On v??rifie tour ?? tour si les noeuds sont d??j?? dans le graphe.
        if node1 not in self.nodes: 
            self.nodes.append(node1) #Si ??a n'est pas le cas, on les ajoute aux noeuds...
            self.graph[node1]=[] #... au dictionnaire repr??sentant le graphe pour povoir lui ajouter des voisins...
            self.nb_nodes+=1 #... et enfin on ajoute +1 au nombre de noeuds du graphe.
        
        #On fait de m??me pour le deuxi??me noeud
        if node2 not in self.nodes: 
            self.nodes.append(node2) 
            self.graph[node2]=[] 
            self.nb_nodes+=1 
        
        #On d??clare ensuite chacun des noeuds comme le voisin de lautre en les ajoutant mutuellement ?? leurs listes de voisins.
        self.graph[node1].append((node2,power_min,dist)) 
        self.graph[node2].append((node1,power_min,dist)) 
        
        #Et enfin, on ajoute +1 au nombre d'ar??tes du graphe.
        self.nb_edges+=1 
    
    #On impl??mente une fonction auxiliaire r??cursive explorer1, qui servira pour la fonction get_path_with_power.
    #'ville' et 'dest' sont deux villes ('dest' est la destination entr??e dans get_path_with_power).
    #'visite' est la liste des villes d??j?? visit??es.
    #'power' est la puissance entr??e dans get_path_with_power.
    #'trajet' contient la liste des villes qui forment le trajet en cours, partant de la ville de d??part ('src').
    
    def explorer1(self,ville,dest,visite,power,trajet):
        if ville==dest: #On se place dans le cas dans lequel on arrive ?? destination.
            return trajet #On renvoie le trajet effectu??, qui est un trajet effectif pour reliser 'src' ?? 'dest'.
        
        visite.append(ville) #On d??clare 'ville' comme un ville visit??e.
        voisins_de_ville=self.graph[ville] #On pose une nouvelle liste de listes, dont chaque premier ??l??ment est le num??ro d'un voisin de 'ville'.
        
        for voisin in voisins_de_ville: #On parcourt tous les voisins de 'ville'.
            
            if voisin[0] not in visite and power>=voisin[1]: #On se place dans le cas o?? la ville voisine n'a pas ??t?? visit??e, et la puissance du camion est assez grande pour passer par cette ar??te.
                trajet.append(voisin[0]) #On ajoute alors le voisin au trajet.
                resultat = self.explorer1(voisin[0],dest,visite,power,trajet)
                if resultat is not None: #On se place dans le cas o?? passer par cette ville ne nous emp??che pas de rallier 'dest' et 'src'.
                    return resultat 
                else: #On se place dans le cas o?? on ne parvient pas ?? rallier 'dest' et 'src' en passant par 'voisin[0]'
                    trajet.pop() #Dans ce cas, on enl??ve simplement 'voisin[0]' (le dernier ??l??ment du trajet) du trajet. On ne rebouclera pas car d??sormais, voisin[0] est dans 'visite'.
       
        return None #Si on arrive ici, c'est que tous les voisins de 'ville' ont soit d??j?? ??t?? visit??s sans succ??s, soit que le camion ne pourra y acc??der en passant par 'ville'. Il a donc ??t?? impossible de relier 'src' et 'dest' en passant par 'voisin' : on renvoie 'None'.

    #On passe ?? la fonction en elle-m??me.
    def get_path_with_power(self, src, dest, power):
        
        #On cherche la composante connexe de 'src'. 
        W=[]
        for l in self.connected_components(): #l est un element de la liste obtenu par la meth comp 
            if src in l:
                W=l
        #Comme 'self.connected_components()' est une partition des noeuds du graphe, il y aura forc??ment un et un seul 'l' dans 'self.connected_components()' tel que 'W=l'.

        if dest in W :      #On se place dans le cas o?? 'src' et 'dest' sont dans la m??me composante connexe.
            visite=[]       #On initialise les voisins visit??s de 'src' ?? l'ensemble vide.
            trajet=[src]    #On initialise le trajet pour qu'il commence toujours par 'src'.
            return self.explorer1(src,dest,visite,power,trajet) #On utilise la fonction auxiliaire d??finie ci-dessus.
        
        else : #On se place dans le cas o?? 'src' et 'dest' ne sont pas dans la m??me composante connxe, c'est-??-dire qu'il n'existe m??me pas de chemin les reliant (ind??pendamment de la puissance).
            return None
     

    
    #On impl??mente une fonction r??cusrive annexe explorer2 pour connected_components. 
    #'i' est un num??ro de noeud.
    #'visited' est un dictionnaire associant ?? chaque noeud du graphe un bool??en ('True' s'il a d??j?? ??t?? visit??, 'False' sinon). 
    def explorer2(self,i,visited):
            L=[]    #'L' est une liste repr??sentant la composante connexe de 'i'.
            if self.graph[i]==[]:   #Si 'i' n'a aucun voisin... 
                L=[i]               #... alors la composante connexe n'est compos??e que du noeud 'i'.
            
            for W in self.graph[i]: #Sinon, on parcourt les voisins de 'i'.
                if visited[W[0]]==False :   #Cas o?? 'W[0]' n'a pas ??t?? visit??.
                    visited[W[0]]=True      #On le d??clare alors comme visit??.
                    L.append(W[0])          #On le rajoute ?? la composante connexe de 'i' (car il est dans ses voisins).
                    L=L+self.explorer2(W[0], visited) #On rappelle la fonction pour parcourir tous les voisins des voisins.
            
            return L
 
    #On impl??mente la fonction en elle-m??me.
    def connected_components(self):  
        U=[] #'U' est une liste de listes, repr??sentant la liste des composantes connexes.
        
        #On initialise le dictionnaire des noeuds de telle sorte que chacun est consid??r?? comme "non visit??".
        visited={} 
        for W in self.graph :
            visited[W]=False   

        #On ex??cute alors le programme auxiliaire explorer1 pour tous les noeuds du graphe   
        for i in self.graph:
            L=self.explorer2(i,visited)
            if L!=[]: #Cas o?? la composante connexe de 'i' n'a pas d??j?? ??t?? rentr??e dans 'U'.
                U.append(L)
        
        return (U)

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
         #prob avec graph[cle] mafine
        maxi=0
        for voisins in self.graph[src]:
            if voisins[1]>maxi :
                maxi=voisins[1]  #je ne vais pas faire ca pour min pour ne pas reparcourir if

        puissance_min = 0
        puissance_max = maxi
        chemin=[]
        while puissance_min < puissance_max:
            puissance = (puissance_min + puissance_max) // 2
            if self.get_path_with_power(src, dest, puissance) is not None: #cad si c est un des chemins possible j'essaie de voir s'il ya un pour une plus petite puiss
                puissance_max = puissance
                
            else:
                puissance_min = puissance + 1  #on augmente la puiss pour arriver a une puisssance efficace

        chemin=self.get_path_with_power(src,dest,puissance_max) #on retourne le chemin pr la puiss
        return (chemin, puissance_max)
 

#Cette fonction ne marche qu'avec des tableaux d'entiers, comme dans les fichiers 'network' propos??s dans le dossier 'input'.
def graph_from_file(filename): 
    f = open("/home/onyxia/work/ensae-prog23/"+filename, "r") #On rajoute le d??but du chemin pour que le programme trouve le chemin du fichier 
    L = f.readlines()   #On transforme le tableau en une liste de cha??ne de caract??res, avec une cha??ne = une ligne 
    lignes=[] 
    g=Graph([]) 
    for i in range(1,len(L)): 
        lignes.append(L[i].split()) #"lignes" est une liste, donc les ??l??ments (qui repr??sentent les lignes de notre tableau) sont des listes de cha??nes de caract??res 
    for line in lignes: 
        if len(line)==3: 
            g.add_edge(int(line[0]),int(line[1]),int(line[2]),1) 
        else : 
            g.add_edge(int(line[0]),int(line[1]),int(line[2]),int(line[3])) 
    #Attention ! Tous les sommets ne sont pas forc??ment reli??s ?? d'autres sommets ! Dans cette partie du code, on s'occupe de mettre dans le graphe les sommets isol??s 
    nb_nodes=int(L[0].split()[0]) #Le nombre de sommets est donn?? par le premier nombre de la premi??re ligne 
    for n in range(1,nb_nodes+1): #On suppose ici que s'il y a n noeuds, tous les noeuds sont exactement tous les num??ros de 1 ?? n. 
        if n not in g.graph: 
            g.graph[n]=[] 
            g.nb_nodes+=1 #Le nombre d'ar??tes n'a pas ??t?? modifi??, mais le nombre de sommets a lui chang?? 
    return g 

'''def kruskal(g) :
    g_mst=Graph([])
    #Trier les ar??tes du graphe 
    for u
    for ar??tes in ensemble_des_ar??tes_tri?? :
        if u !=v :
            g_mst.add_edge(u, v, truc)

    return (g_mst)'''
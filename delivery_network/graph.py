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
         
         #On vérifie tour à tour si les noeuds sont déjà dans le graphe.
        if node1 not in self.nodes: 
            self.nodes.append(node1) #Si ça n'est pas le cas, on les ajoute aux noeuds...
            self.graph[node1]=[] #... au dictionnaire représentant le graphe pour povoir lui ajouter des voisins...
            self.nb_nodes+=1 #... et enfin on ajoute +1 au nombre de noeuds du graphe.
        
        #On fait de même pour le deuxième noeud
        if node2 not in self.nodes: 
            self.nodes.append(node2) 
            self.graph[node2]=[] 
            self.nb_nodes+=1 
        
        #On déclare ensuite chacun des noeuds comme le voisin de lautre en les ajoutant mutuellement à leurs listes de voisins.
        self.graph[node1].append((node2,power_min,dist)) 
        self.graph[node2].append((node1,power_min,dist)) 
        
        #Et enfin, on ajoute +1 au nombre d'arêtes du graphe.
        self.nb_edges+=1 
    
    #On implémente une fonction auxiliaire récursive explorer1, qui servira pour la fonction get_path_with_power.
    #'ville' et 'dest' sont deux villes ('dest' est la destination entrée dans get_path_with_power).
    #'visite' est la liste des villes déjà visitées.
    #'power' est la puissance entrée dans get_path_with_power.
    #'trajet' contient la liste des villes qui forment le trajet en cours, partant de la ville de départ ('src').
    
    def explorer1(self,ville,dest,visite,power,trajet):
        if ville==dest: #On se place dans le cas dans lequel on arrive à destination.
            return trajet #On renvoie le trajet effectué, qui est un trajet effectif pour reliser 'src' à 'dest'.
        
        visite.append(ville) #On déclare 'ville' comme un ville visitée.
        
        for voisins in self.graph[ville]: #On parcourt tous les voisins de 'ville'.
            voisin=voisins[0] #'voisin' désigne le numéro du noeud voisin
            puissance=voisins[1] #'puissance' désigne la puissance minimale nécessaire pour parcourir l'arête
            if voisin == dest: #On regarde si la ville voisine est la ville d'arrivée...
                if power >= puissance: #...et si on a la puissance suffisante pour parcourir le chemin...
                    trajet.append(dest) 
                    return trajet #... alors cela signifie qu'on est arrivés au résultat, donc on le renvoie

            else: #On se place dans le cas où la ville qu'on regarde n'est pas la ville d'arrivée, ou qu'elle l'est mais qu'on ne peut pas l'atteindre par le chemin choisi.
                if voisin not in visite and power>=puissance: #On se place dans le cas où le voisin n'est pas visité, et on a assez de puissance pour aller le rejoindre.
                    trajet.append(voisin) #On peut donc l'ajouter au trajet
                    if self.explorer1(voisin,dest,visite,power,trajet) is None: #Si on obtient "None", c'est qu'on a fait toute la boucle avec 'voisin' sans arriver à relier la ville à 'dest'.
                        trajet.pop( )   #Cela signifie que c'était une mauvaise idée de passer par 'voisin', et on le retire du trajet.
                                        #On remarque qu'on ne rebouclera pas à l'infini car désormais 'voisin' est dans 'visiste'.
                    else:
                        return trajet

    #On passe à la fonction en elle-même.
    def get_path_with_power(self, src, dest, power):
        
        #On cherche la composante connexe de 'src'. 
        W=[]
        for l in self.connected_components(): #l est un element de la liste obtenu par la meth comp 
            if src in l:
                W=l
        #Comme 'self.connected_components()' est une partition des noeuds du graphe, il y aura forcément un et un seul 'l' dans 'self.connected_components()' tel que 'W=l'.

        if dest in W :      #On se place dans le cas où 'src' et 'dest' sont dans la même composante connexe.
            visite=[]       #On initialise les voisins visités de 'src' à l'ensemble vide.
            trajet=[src]    #On initialise le trajet pour qu'il commence toujours par 'src'.
            return self.explorer1(src,dest,visite,power,trajet) #On utilise la fonction auxiliaire définie ci-dessus.
        
        else : #On se place dans le cas où 'src' et 'dest' ne sont pas dans la même composante connxe, c'est-à-dire qu'il n'existe même pas de chemin les reliant (indépendamment de la puissance).
            return None
     

    
    #On implémente une fonction récusrive annexe explorer2 pour connected_components. 
    #'i' est un numéro de noeud.
    #'visited' est un dictionnaire associant à chaque noeud du graphe un booléen ('True' s'il a déjà été visité, 'False' sinon). 
    def explorer2(self,i,visited):
            L=[]    #'L' est une liste représentant la composante connexe de 'i'.
            if self.graph[i]==[]:   #Si 'i' n'a aucun voisin... 
                L=[i]               #... alors la composante connexe n'est composée que du noeud 'i'.
            
            for W in self.graph[i]: #Sinon, on parcourt les voisins de 'i'.
                if visited[W[0]]==False :   #Cas où 'W[0]' n'a pas été visité.
                    visited[W[0]]=True      #On le déclare alors comme visité.
                    L.append(W[0])          #On le rajoute à la composante connexe de 'i' (car il est dans ses voisins).
                    L=L+self.explorer2(W[0], visited) #On rappelle la fonction pour parcourir tous les voisins des voisins.
            
            return L
 
    #On implémente la fonction en elle-même.
    def connected_components(self):  
        U=[] #'U' est une liste de listes, représentant la liste des composantes connexes.
        
        #On initialise le dictionnaire des noeuds de telle sorte que chacun est considéré comme "non visité".
        visited={} 
        for W in self.graph :
            visited[W]=False   

        #On exécute alors le programme auxiliaire explorer1 pour tous les noeuds du graphe   
        for i in self.graph:
            L=self.explorer2(i,visited)
            if L!=[]: #Cas où la composante connexe de 'i' n'a pas déjà été rentrée dans 'U'.
                U.append(L)
        
        return (U)

    def connected_components_set(self): 
        """ 
        The result should be a set of frozensets (one per component),  
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})} 
        """ 
        return set(map(frozenset, self.connected_components())) 

    def min_power(self, src, dest): 
        
        # On recherche d'abord l'arête qui représente la plus grande puissance dans tout le graphe.
        maxi=0
        for node in self.nodes: 
            for voisins in self.graph[node]:
                if voisins[1]>maxi :
                    maxi=voisins[1]  
        #On ne fait pas la même chose pour la puissance minimale, pour ne pas reparcourir de boucle 'if'. Partir de 0 suffit.

        puiss_min=0
        puiss_max=maxi
        chemin =[]
        
        # La recherche binaire consiste à diviser en 2 parties à peu près égales le segment [puiss_min, puiss_max].
        while puiss_min < puiss_max :               # Si on met '<=', en cas d'égalité, on aura 'puiss=0' et après 'puiss_min=0' et on pourrait rentrer dans des boucles infinies.
            puiss = (puiss_max + puiss_min)//2      #On prend un entier "à peu près" au milieu de 'puiss_min' et 'puiss_max'.
            if self.get_path_with_power(src, dest, puiss) is not None: #On se place dans le cas où il a été possible de relier les deux villes avec la puissance fournie.
                puiss_max=puiss #On essaye de trouver une puissance plus petite que 'puiss' : 'puiss' devient la borne supérieure de la recherche.
            else:
                puiss_min = puiss+1 # Comme la puissance "puiss" ne suffit pas pour le parcours, on recherche dans une puissance supérieure à 'puiss'.
                                    # Si on ne rajoute pas le '+1', on aura un problème quand on trouve la puiss minimale la boucle while rstera infini
        
        chemin= self.get_path_with_power(src, dest, puiss_max) # A la dernière itération, 'puiss' est modifiée et on rentrera dans le cas else donc on ne peut pas mettre puiss
        return (chemin, puiss_max)

#Cette fonction ne marche qu'avec des tableaux d'entiers, comme dans les fichiers 'network' proposés dans le dossier 'input'.
def graph_from_file(filename): 
    f = open("/home/onyxia/work/ensae-prog23/"+filename, "r") #On rajoute le début du chemin pour que le programme trouve le chemin du fichier 
    L = f.readlines()   #On transforme le tableau en une liste de chaîne de caractères, avec une chaîne = une ligne 
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


#Question 10 
#On cherche ici à implémenter une fonction qui permet d'estimer le temps pour calculer la puissance minimale sur un ensemble de trajets.

#On commence par implémenter une fonction auxiliaire, qui lit un fichier de type 'routes.x.in' (tableau d'entiers) et renvoie ce tableau comme une liste de listes (une liste d'entiers par ligne)
def lecture(filename): 
    f = open("/home/onyxia/work/ensae-prog23-2/input/"+filename, "r") #On rajoute le début du chemin pour que le programme trouve le chemin du fichier 
    L = f.readlines()#On transforme le tableau en une liste de chaîne de caractères, avec une chaîne = une ligne 
    lignes=[] 
    for i in range(1,len(L)): 
        lignes.append(list(map(int,L[i].split()))) #"lignes" est une liste, donc les éléments (qui représentent les lignes de notre tableau) sont des listes de chaînes de caractères 
    return lignes 

#On arrive à la fonction en elle-même, qui prend en entrée un fichier (de types 'routes.x.in') et un graphe 'g' (qu'on doit prendre comme le graphe associé à l'ensemble des routes du fichier 'routes.x.in' choisi).

from time import perf_counter

def Temps(g, filename):
    L=[] #'L' contiendra tous les temps d'exécutions de 'min_power' pour les premières lignes. 
    lignes = lecture(filename) #On utilise la fonction auxiliaire pour obtenir une liste de listes d'entiers.
    for i in range(20): #On prend les 20 premiers trajets
        l=lignes[i]     #'l' est la i-ème ligne correspondant au i-ème trajet du tableau.
        src = l[0] ; dest=l[1] #Dans cette ligne, le premier entier correspond au noeud de départ, et le deuxième au noeud d'arrivée.
        t1_start = perf_counter()
        g.min_power(src, dest)
        t1_stop = perf_counter()
        L.append(t1_stop - t1_start) #On ajoute à la liste 'L' le temps qu'a mis 'min_power' pour s'exécuter.
    
    #On cherche ensuite à donner le temps global (on ne se réduit plus qu'aux 20 premières lignes).
    S=0
    #On fait la somme de tous les temps
    for l in L:
        S+=l 
    Tmoy= S/len(L)
    #Renvoie le temps moyen d'exécution de 'min_power' pour un seul trajet.
    return Tmoy*(len(lignes)) #Multiplié par le nombre de trajets, on obtient le temps d'exécution global.

#Question 12

def find(x,parent):
    if parent[i]==[]:
        return i
    parent[i]=Find(parent[i])
    return parent[i]

def union(x,y,parent):
    parent[find(x)]=find(y)


def trifusiontriplet(L):
    n=len(L)
    if n<=1:
        return L
    else : 
        return fusiontriplet(trifusiontriplet(L[0, n//2]),trifusiontriplet(L[n//2,n]))

def fusiontriplet(L,M):
    if L==[]:
        return M
    if M==[]:
        return L
    if L[0][2]<=M[0][2]:
        return [L[0]]+fusiontriplet(L[1,len(L)],M)
    return [M[0]]+fusiontriplet(M[1,len(M)],L)

def kruskal(graphe):
    E=Graph([])#Graphe qu'on va vouloir renvoyer
    Liste=[] #Liste dans laquelle on va stocker des triplets (noeud1,noeud2,puissance) --> C'est la liste qu'on triera
    for u in E.graph:
        for V in E.graph[u]:
            v=V[0]
            if u<v:
                t=(u,v,V[1])
            else : 
                t=(v,u,V[1])
            if t not in Liste:
                Liste.append(t)
    parent=[[]*graphe.nb_nodes]
    L=trifusiontriplet(Liste) #Savoir à qui on affecte le tri !!
    for U in L:
        u=U[0]
        for V in E.graph[u]:
            v=V[0] ; power=V[1] ; dist=V[2]
            if find(u,parent)!=find(v,parent):
                E.add_edge(u,v,power,dist)
                union(u,v,parent)
    return E


#J'écris une fonction pour la question 18, qui sert à supprimer tous camions inutiles, parce que plus cher et moins efficace que d'autres.
def tri_des_camions(filename):
    L_reverse=[]
    lignes = lecture(filename)
    max=lignes[-1][1]
    for l in reversed(lignes):
        valeur = l[1]
        if valeur<=max :
            max=valeur
            L_reverse.append(l)
    return list(reversed(L_reverse))
#Complexité en O(n)

def function(fichier_trucks,fichier_routes,fichier_network): #on lui donne les fichiers: routes (trajet,utilite), trucks (p,c) 
    b= 25*(10**9) #contrainte budg
    depenses=0
    utilite = 0
    trucks=tri_des_camions(fichier_trucks)
    while depenses <= b :
        #  je veux acceder aux lignes du fichier_routes, chaque ligne i>=1 represente le trajet i et son utilite i 
        g=graph_from_file("input/"+fichier_routes)  #il faudra peut etre deplacer la fct
        d=g.graph
        #d.items() me donne une liste tq l'element k contient (clek,valeurk)
    
        gg= graph_from_file("input/"+fichier_network)
        # g sera un graphe tq: cles i -> [(ville j , u i->j),(ville k , u i->k),.......]
        
        for i in range (0,len(d.items())):    #on parcourt tous les noeuds et donc toutes les villes qui sont le depart d'un trajet dans le fichier routes
            for ville_i, valeur in d.items[i]:
                for j in range (0, len(valeur)):
                    ville_j= valeur[j][0] #rep la ville arrivee du trajet
                    utilite_ij= valeur[j][1] #rep l'utilite de ce trajet
                    trajet_ij = (ville_i,ville_j,utilite_ij) 
                    pmin= gg.min_power(ville_i,ville_j)
                    # a present on travail dans le fichier trucks
                    dd=dict_from_file_trucks(fichier_trucks)
                    liste= dd.items() #dd.items() va etre une liste tq chaque element represente: [p,c]
                    #trions la liste dd.items suivant le cout mais j pense faut revoir car pb avec liste de liste
                    liste.sort(key=lambda x: x[1]) # on aura liste de (p,c) trier par cout croissant

                    for i in range (0,len(liste)):
                        if liste[i][0]< pmin: # liste[i][0] est puissance donnee dans le fichier truck 
                            liste.delete(liste[i])
                    #notre liste a present contient les puiss et cout tq puiss >= pmin et triee par odre croissant de cout
                    cout_minimal=liste[0][1]

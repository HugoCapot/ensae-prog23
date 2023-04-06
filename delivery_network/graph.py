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
        
        else : #On se place dans le cas où 'src' et 'dest' ne sont pas dans la même composante connexe, c'est-à-dire qu'il n'existe même pas de chemin les reliant (indépendamment de la puissance).
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

    #Question 12
    #On utilise des programmes auxiliaires qui permettent la méthode "Union-find" pour construire un arbre, comme proposé par l'énoncé.
    def find(self,i,parent):
        if parent[i-1]==[]:
            return i
        parent[i-1]=self.find(parent[i-1],parent)
        return parent[i-1]

    def union(self,x,y,parent):
        parent[self.find(x,parent)-1]=self.find(y,parent)

    #On utilise ensuite deux nouveaux programmes auxiliaires qui vont nous permettre de trier les arêtes selon leurs puissances, en utilisant la méthode du "tri fusion".
    def trifusionquadruplet(self,L):
        n=len(L)
        if n<=1:
            return L
        else : 
            return self.fusionquadruplet(self.trifusionquadruplet(L[0 : n//2]),self.trifusionquadruplet(L[n//2 : n]))

    def fusionquadruplet(self,L,M):
        if L==[]:
            return M
        if M==[]:
            return L
        if L[0][2]<=M[0][2]:
            return [L[0]]+self.fusionquadruplet(L[1 :len(L)],M)
        return [M[0]]+self.fusionquadruplet(M[1 :len(M)],L)

    #On développe enfin la fonction, qui renvoie l'arbre couvrant de poids minimal du graphe
    def kruskal(self):
        E=Graph([])#Graphe (arbre) qu'on va vouloir renvoyer
        Liste=[] #Liste dans laquelle on va stocker des quadruplets (noeud1,noeud2,puissance,dist) --> C'est la liste qu'on triera
        for u in self.graph:
            for V in self.graph[u]:
                v=V[0]
                if u<v:
                    t=(u,v,V[1],V[2])
                else : 
                    t=(v,u,V[1],V[2]) #On prend cette précaution afin de ne pas placer deux fois les mêmes arêts dans la liste
                if t not in Liste:
                    Liste.append(t)
        parent=[[] for i in range (self.nb_nodes)] #Liste des parents qui sera utile pour la méthode Union-find
        L=self.trifusionquadruplet(Liste) #On trie les arêtes par puissance croissante
        for U in L: 
            u=U[0] ; v=U[1] ; power=U[2] ; dist=U[3]
            if self.find(u,parent)!=self.find(v,parent): #On s'assure que u et v ne sont pas déjà reliés, sinon on formerait des cycles (et on n'obtiendrait donc pas d'arbre).
                E.add_edge(u,v,power,dist) 
                self.union(u,v,parent) #On signale que u et v sont désormais reliés
        return E

    #Question 14
    #On modifie légèrement la fonction "get_path_with_power" et sa fonction auxiliaire, car dans le cas d'un arbre, on sait que le chemin est unique. On ne prend plus de puissance en entrée
    def explorer3(self,ville,dest,visite,trajet,liste_puissance):
        if ville==dest: #On se place dans le cas dans lequel on arrive à destination.
            return (trajet,sum(liste_puissance)) #On renvoie le trajet effectué, qui est un trajet effectif pour reliser 'src' à 'dest'.
        visite.append(ville) #On déclare 'ville' comme un ville visitée.
        for voisins in self.graph[ville]: #On parcourt tous les voisins de 'ville'.
            voisin=voisins[0] #'voisin' désigne le numéro du noeud voisin
            puissance=voisins[1] #'puissance' désigne la puissance minimale nécessaire pour parcourir l'arête
            if voisin == dest: #On regarde si la ville voisine est la ville d'arrivée...
                trajet.append(dest) 
                liste_puissance.append(puissance)
                return (trajet,sum(liste_puissance)) #... alors cela signifie qu'on est arrivés au résultat, donc on le renvoie

            else: #On se place dans le cas où la ville qu'on regarde n'est pas la ville d'arrivée, ou qu'elle l'est mais qu'on ne peut pas l'atteindre par le chemin choisi.
                if voisin not in visite : #On se place dans le cas où le voisin n'est pas visité, et on a assez de puissance pour aller le rejoindre.
                    trajet.append(voisin)#On peut donc l'ajouter au trajet
                    liste_puissance.append(puissance)
                    if self.explorer3(voisin,dest,visite,trajet,liste_puissance) is None: #Si on obtient "None", c'est qu'on a fait toute la boucle avec 'voisin' sans arriver à relier la ville à 'dest'.
                        trajet.pop( )   #Cela signifie que c'était une mauvaise idée de passer par 'voisin', et on le retire du trajet.
                        liste_puissance.pop()               #On remarque qu'on ne rebouclera pas à l'infini car désormais 'voisin' est dans 'visiste'.
                    else:
                        return (trajet,sum(liste_puissance))

    def new_get_path_with_power(self, src, dest):
        #Comme 'self.connected_components()' est une partition des noeuds du graphe, il y aura forcément un et un seul 'l' dans 'self.connected_components()' tel que 'W=l'.     #On se place dans le cas où 'src' et 'dest' sont dans la même composante connexe.
        liste_puissance=[]
        visite=[]       #On initialise les voisins visités de 'src' à l'ensemble vide.
        trajet=[src]    #On initialise le trajet pour qu'il commence toujours par 'src'.
        return self.explorer3(src,dest,visite,trajet,liste_puissance) #On utilise la fonction auxiliaire définie ci-dessus.
    
    #Fonction auxiliaire pour "creer_parents"
    def explorer4(self,ville,visite,parents):
        if sum(visite) == self.nb_nodes :
            return parents
        visite[ville-1]=1 #On déclare 'ville' comme un ville visitée.
        for voisins in self.graph[ville]: #On parcourt tous les voisins de 'ville'.
            voisin=voisins[0] #'voisin' désigne le numéro du noeud voisin
            if len(self.graph[voisin])==1 and visite[voisin-1]==0:
                parents[voisin-1]=(ville,voisins[1],voisins[2])
                visite[voisin-1]=1
                if sum(visite) == self.nb_nodes :
                    return parents
            if visite[voisin-1]==0 :
                parents[voisin-1]=(ville,voisins[1],voisins[2])
                if self.explorer4(voisin,visite,parents) is not None:
                    return(self.explorer4(voisin,visite,parents))
                    

    #Fonction pour créer la liste des parents de chaque noeud du graphe
    def creer_parents(self,racine):
        parents=[[] for i in range (self.nb_nodes)]
        visite=[0 for i in range (self.nb_nodes)]
        parents[racine-1]=racine  
        return(self.explorer4(racine,visite,parents))

    def new_power_min(self,src,dest):
        A=self.kruskal()
        return A.new_get_path_with_power(src, dest)
    
    def new_new_power_min(self,src,dest):
        return self.new_get_path_with_power(src, dest)
    
    def trajet(self,ville,racine,parent):
        t=ville
        route=[]
        while t!=racine:
            route.append(parent[t-1])
            t=parent[t-1][0] 
        return(route)
    
    #creer_parent est déjà construite
    def min_power_arbre(self, src, dest,racine,parent):
        L=list(reversed(self.trajet(src,racine,parent)))
        M=list(reversed(self.trajet(dest,racine,parent)))
        if M==[] or L==[]:
            return 0
        else :
            while L!=[] and M!=[] and M[0]==L[0]:
                M.pop(0)
                L.pop(0)
            route=list(reversed(M))+L
            puissance =0
            for l in route :
                if puissance < l[1]:
                    puissance=l[1]
            return puissance


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

#Question 18

#Fonction auxiliaire pour la question 18, qui sert à supprimer tous camions inutiles, parce que plus cher et moins efficace que d'autres.
#Elle présuppose que les camions sont rangés par puissance croissante
def tri_des_camions(lignes):
    L_reverse=[]
    max=lignes[-1][1]
    for l in reversed(lignes):
        valeur = l[1]
        if valeur<=max :
            max=valeur
            L_reverse.append(l)
    return list(reversed(L_reverse))
#Complexité en O(n)


#Méthode 1:methode naive, exacte mais non optimal
#Pour la tester on a créé des fichiers dans input .a.in et .b.in
def function_profit_exacte(fichier_trucks,fichier_routes,fichier_network): 
       
    lr=liste_from_file("input/"+fichier_routes)
    g= graph_from_file("input/"+fichier_network)        
    lt=liste_from_file("input/"+fichier_trucks) 

    '''on veut tester toutes les listes possibles qu'on peut faire a partir du fichier routes et trouver dans 
    chacune umax pour ensuite trouver le max de tous        
    '''

    import itertools
    permutations= list(itertools.permutations(lr)) #liste ou sera stockés toutes les permutations

    umax=0
    resultat_final=[]
    b= 25* (10**9)

    for perm in permutations: #pour chaque element de la liste permutations cad chaque ensemble d'utilite
        u=0
        resultat=[]
        depenses=0 #on definit depenses a l'intérieur de for pour que pour chaque perm la variable se réinitialise a 0
        for i in range (0,len(perm)):
            if depenses <= b:
                p=g.min_power(perm[i][0],perm[i][1])
                pmin=p[1]
                for j in range(0,len(lt)):
                    if lt[j][0]>= pmin:
                        puiss= lt[j][0]
                        c=lt[j][1]
                        depenses=depenses+c
                        if depenses<=b: #pour s'assurer qu'une fois rajouter on ne depassera pas cb
                            resultat.append([(puiss,c),(perm[i][0],perm[i][1])])
                            u=u+perm[i][2] 
                        break   
            else:
                break
        if u>= umax:
            umax=u
            resultat_final=resultat
    return (umax,resultat_final)
        




#Méthode rapide mais non optimale
def function_profit(fichier_trucks,fichier_routes,fichier_network):
    # je veux acceder aux lignes du fichier_routes, chaque ligne i>=1 represente le trajet i=(ville1,ville2) et son utilite i 
    lr=liste_from_file("input/"+ fichier_routes) #"lr" sera la liste des lignes du fichier route (chaque élément est de la forme [ville 1, ville 2, utilité]) 
    lr.sort(key=lambda x: x[2]) #On trie "lr" par ordre croissant d'utilité         
    g= graph_from_file("input/"+fichier_network) #On importe le graphe construit à partir du fichier texte demandé
    A=g.kruskal()
    racine=lr[0][0]
    parents=A.creer_parents(racine)
    lt=tri_des_camions(liste_from_file("input/"+fichier_trucks)) #On importe la liste des camions triée. Chaque élément est de la forme [puissance, coût]

    b= 25*(10**9) #Contrainte budgétaire
    depenses=0 #Compteur de nos dépenses
    umax= 0 #Compteur de notre utilité
    c=0 
    resultat=[]
    for i in range (0,len(lr)): #On parcourt toutes les routes dans l'ordre
        l=len(lr)
        pmin=A.min_power_arbre(lr[l-i-1][0],lr[l-i-1][1],racine, parents) #On récupère la puissance minimale sur le trajet considéré
        #On cherche le camion le moins cher qui permet d'effectuer le trajet
        for j in range (0,len(lt)):
            if lt[j][0]>= pmin:
                puiss=lt[j][0]
                c= lt[j][1]
                depenses=depenses+c
                break
        if depenses>b:
            break
        resultat.append([(puiss,c),(lr[l-i-1][0],lr[l-i-1][1])])
        umax+=lr[l-i-1][2]   #On prend l'indice "l-i-1" car on veut sommer les utilités en partant des plus grandes utilités ("lr" est triée par ordre croissant d'utilité) 
    return (umax,resultat)

def liste_from_file(filename):
    f = open("/home/onyxia/work/ensae-prog23/"+filename, "r") 
    L = f.readlines()
    lignes=[] 
    liste=[]
    for i in range(1,len(L)): 
        lignes.append(L[i].split())  
    for line in lignes: 
        if len(line)==2: #Pour le fichier trucks
            liste.append([int(line[0]) ,int(line[1])]) # Elements de la forme [puissance, coût]
        if len(line)==3: #Pour le fichier routes
            liste.append([int(line[0]),int(line[1]),int(line[2])]) #Elements de la forme [ville 1,ville 2, utilité]
    return liste

from graph import Graph, graph_from_file 
import graphviz

data_path = "input/" 
file_name = "network.03.in" 

g = graph_from_file(data_path + file_name) 
print(g.connected_components_set()) 
#g=Graph([]) 
#g.add_edge("Paris","Palaiseau",4,20) 
#print(g) 

#A écrire dans le terminal : pip install graphviz
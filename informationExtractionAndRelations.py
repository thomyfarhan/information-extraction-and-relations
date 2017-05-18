import nltk
# nltk.download('all')
import networkx as nx
import matplotlib.pyplot as plt
import os

def remove_non_ascii(document):
    return ''.join(i for i in document if ord(i) < 128)

def ie_preprocess(document):
    sentences = nltk.sent_tokenize(document)
    sentences = [nltk.word_tokenize(sent) for sent in sentences]
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    return sentences

def extract_names(document):
    names = []
    sentences = ie_preprocess(document)
    for tagged_sentence in sentences:
        for chunk in nltk.ne_chunk(tagged_sentence):
            if type(chunk) == nltk.tree.Tree:
                if chunk.label() == 'PERSON':
                    names.append(' '.join([c[0] for c in chunk]))
    return names	
	
def extract_organizations(document):
   organizations = []
   sentences = ie_preprocess(document)
   for tagged_sentence in sentences:
       for chunk in nltk.ne_chunk(tagged_sentence):
           if type(chunk) == nltk.tree.Tree:
               if chunk.label() == 'ORGANIZATION':
                   organizations.append(' '.join([c[0] for c in chunk]))
   return organizations

def draw_graph(graph, label):
    G = nx.Graph()
    G.add_edges_from(graph)
    graph_pos = nx.shell_layout(G)
    nx.draw_networkx_nodes(G, graph_pos, node_size=200, node_color='yellow', alpha=0.5)
    nx.draw_networkx_edges(G, graph_pos, width=2, alpha=0.3, edge_color='black')
    nx.draw_networkx_labels(G, graph_pos, font_size=9, font_family='DejaVu Sans')
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=label)
    plt.show()
	
def main():
	entity = []
	x = 1
	for file in os.listdir('data'):
		artikel = os.path.join('data', file)
		artikel = open(artikel)
		text = artikel.read()
		artikel.close()
		string = remove_non_ascii(text)
		names = extract_names(string)
		organizations = extract_organizations(string)
		merged = set(list(organizations+names))
		entity.append(merged)
		print "Ditambahkan hasil ekstrasi artikel ke-",x," .."
		print entity
		print "\n"
		x = x + 1
	
	graph = []
	label = {}
	temp = {}

	for item in entity:
		for i in item:
			for j in item:
				if i != j:
					val = (i, j)
					if temp.has_key(val):
						temp[val] = temp[val] + 1
						if temp[val] > 1:
							label[val] = temp[val]
							graph.append(val)
					else:
						temp[val] = 1

	draw_graph(graph, label)
	
main()

## thomyfarhan
from flask import Flask, request
from flask_cors import CORS

import networkx as nx
from lib.obsidian_graph import build_graph

####################################################################################
# config
####################################################################################
PORT = 5000
HOST = '127.0.0.1'
MAX_RESULTS = 20

app = Flask(__name__)
####################################################################################
# Cors
####################################################################################
# Allows access to fetch at 'http://localhost:5000/' from origin 'app://obsidian.md'
obsidian_origin = "app://obsidian.md"
cors = CORS(app, origins=obsidian_origin)
app.config['CORS_HEADERS'] = 'Content-Type'


####################################################################################
# Routers
####################################################################################

# Used by the obsidian plugin to know what methods are there.
@app.route('/', methods=['GET'])
def root():
    return {
        'scripts': [
            f'http://{HOST}:{PORT}/page_rank'
        ]
    }


@app.route('/page_rank', methods=['POST'])
def idf():
    # note_path = request.json['notePath']
    vault_path = request.json['vaultPath']
    G, page_ref = build_graph(vault_path)
    results = []

    # A map of the form:
    # {id: note_path}
    source_file = nx.get_node_attributes(G, "source_file")
    pr = nx.pagerank(G, alpha=0.8)
    sorted_page_rank = sorted(pr.items(), key=lambda x: x[1], reverse=True)

    for k, v in sorted_page_rank[0:MAX_RESULTS]:
        # Some nodes will not be in this list, this means they don't have a note yet
        if k in source_file:
            name = page_ref[k].replace(vault_path, '')
            results.append({
                'info': {
                    'score': v
                },
                'name': name,
                'path': page_ref[k]
            })
    return {
        "label": f' Page rank, (first {MAX_RESULTS})',
        "n_nodes": G.number_of_nodes(),
        "n_edges": G.number_of_edges(),
        "contents": results,
    }

def main():
    app.run(port=PORT, host=HOST)


if __name__ == '__main__':
    main()

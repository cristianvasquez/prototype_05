import networkx as nx

from lib.obsidian_graph import build_graph
from playground.vars import DEFAULT_DIR


def main(
        input_dir=DEFAULT_DIR,
):
    G, page_ref = build_graph(input_dir, directed=False)

    def printDiameter():
        components = nx.connected_components(G)
        largest_component = max(components, key=len)
        diameter = nx.diameter(largest_component)
        return diameter

    print(nx.info(G))
    print('Loaded', len(page_ref), 'files')
    print('Generated', G.number_of_nodes(), 'nodes')
    print("Network diameter:", printDiameter())
    print('-----')


if __name__ == '__main__':
    main()

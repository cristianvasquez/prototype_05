import os
import networkx as nx

from lib.obsidian_graph import build_graph

THIS_DIR = os.getcwd()


def main(
        # input_dir=DEFAULT_DIR,
        input_dir='../test_obsidian_vault',
):
    G, page_ref = build_graph(input_dir)

    def print_node_list(pr, first_n):
        results = []
        source_file = nx.get_node_attributes(G, "source_file")
        sorted_page_rank = sorted(pr.items(), key=lambda x: x[1], reverse=True)
        for k, v in sorted_page_rank[0:first_n]:
            # Some nodes will not be in this list, this means they don't have a note yet
            if k in source_file:
                results.append({
                    'score':v,
                    'internal id':k,
                    'path':page_ref[k]
                })
        return results

    print(nx.info(G))
    print('Loaded', len(page_ref), 'files')
    print('Generated', G.number_of_nodes(), 'nodes')
    print("Network density:", nx.density(G))
    print('-----')

    print('10 highest page-rank scores')
    pr = nx.pagerank(G, alpha=0.8)
    first_ten = print_node_list(pr, 10)
    for current in first_ten:
        print(current)


if __name__ == '__main__':
    main()

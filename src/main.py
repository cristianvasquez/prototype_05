import codecs
import os
from functools import partial

import frontmatter
import networkx as nx
from yaml.scanner import ScannerError

from misc import build_inverted_index, get_title, get_links
from misc import label_to_path

THIS_DIR = os.getcwd()


def main(
        input_dir='/home/cvasquez/obsidian/workspace',
        # input_dir='../test_obsidian_vault',
):
    input_dir = os.path.abspath(os.path.join(THIS_DIR, input_dir))

    # Inverted index, used to handle Obsidian's 'shortest path' strategy
    exclude = {'.git', '.obsidian', '.trash'}
    names_relpath = build_inverted_index(input_dir, exclude)
    get_path = partial(label_to_path, names_relpath)

    # A directed graph
    G = nx.DiGraph()
    page_ref = {}

    def get_set_id(value):
        if value not in page_ref:
            page_ref[value] = len(page_ref) + 1
        return page_ref[value]

    number_of_files=0
    # Generating the graph
    for root, dirs, files in os.walk(input_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]

        for file_name in files:
            source_file = os.path.join(root, file_name)
            name, _ = os.path.splitext(file_name)
            with codecs.open(source_file, 'r', encoding='utf-8') as f:

                name, extension = os.path.splitext(file_name)

                def add_node(fm):
                    content = fm.content
                    metadata = fm.metadata

                    unique_name = os.path.relpath(source_file, start=input_dir)
                    _id = get_set_id(unique_name)
                    page_ref[_id] = unique_name

                    node = {
                        'id': _id,
                        'title': get_title(metadata, content, source_file),
                        'source_file': source_file,
                        'metadata': metadata,
                        # 'content': content,
                        # 'links': links
                    }

                    # Add nodes
                    G.add_nodes_from([
                        (_id, node),
                    ])

                    # Add edges
                    for label in get_links(content):
                        link = get_path(label)
                        if link is not None:
                            G.add_edge(_id, get_set_id(link))



                if extension == '.md':
                    try:
                        fm = frontmatter.load(f)
                        add_node(fm)
                        number_of_files += 1
                    except ScannerError:
                        print("Warning: could not process front-matter of: {}".format(source_file))


    print(nx.info(G))

    print('Loaded',number_of_files,'files')

    # nx.draw(G, with_labels=True)
    # plt.show()
    pr = nx.pagerank(G, alpha=0.8)
    source_file = nx.get_node_attributes(G, "source_file")

    sorted_page_rank = sorted(pr.items(), key=lambda x: x[1], reverse=True)
    print('Generated',len(sorted_page_rank),'nodes')

    for k, v in sorted_page_rank[1:50]:

        # Some nodes will not be in this list, this means they don't have a note yet
        if k in source_file:
            print(v, k, page_ref[k])

if __name__ == '__main__':
    main()

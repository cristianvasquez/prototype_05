import codecs
import os
from functools import partial

import frontmatter
import networkx as nx
import matplotlib.pyplot as plt

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

    # Generating the graph
    for root, dirs, files in os.walk(input_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]

        for file_name in files:
            source_file = os.path.join(root, file_name)
            name, _ = os.path.splitext(file_name)
            with codecs.open(source_file, 'r', encoding='utf-8') as f:

                name, extension = os.path.splitext(file_name)
                if extension == '.md':

                    try:
                        fm = frontmatter.load(f)
                    except:
                        print("{}".format(source_file))

                    content = fm.content
                    metadata = fm.metadata

                    unique_name = os.path.relpath(source_file, start=input_dir)
                    _id = id(unique_name)
                    page_ref[_id]=unique_name

                    node = {
                        'id': _id,
                        'title': get_title(metadata, content, source_file),
                        'source_file': source_file,
                        'metadata': metadata,
                        # 'content': content,
                        # 'links': links
                    }

                    G.add_nodes_from([
                        (_id, node),
                    ])

                    # links = set()
                    for label in get_links(content):
                        link = get_path(label)
                        if link is not None:
                            G.add_edge(_id, id(link))
                            # links.add(id(link))

    # with open(target_filename, 'w', encoding="utf-8") as out_file:
    #     out_file.write(template.render(context))
    # nx.draw(G, with_labels=True)
    # plt.show()
    # print(G.nodes)
    pr = nx.pagerank(G, alpha=0.8)
    winner_page_rank = max(pr)
    print(page_ref[winner_page_rank])

if __name__ == '__main__':
    main()

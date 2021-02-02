import codecs
import os
import shutil
from functools import partial
from shutil import copyfile

import frontmatter

from misc import build_inverted_index, get_title, get_links
from misc import label_to_path

THIS_DIR = os.getcwd()

def main(
        # input_dir='/home/cvasquez/obsidian/public-garden',
        input_dir='../test_obsidian_vault',
):
    input_dir = os.path.abspath(os.path.join(THIS_DIR, input_dir))

    # Inverted index, used to handle Obsidian's 'shortest path' strategy
    exclude = {'.git', '.obsidian', '.trash'}
    names_relpath = build_inverted_index(input_dir, exclude)
    get_path = partial(label_to_path, names_relpath)

    # Preparing the template
    for root, dirs, files in os.walk(input_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]

        for file_name in files:
            source_file = os.path.join(root, file_name)
            name, _ = os.path.splitext(file_name)
            with codecs.open(source_file, 'r', encoding='utf-8') as f:
                fm = frontmatter.load(f)
                content = fm.content
                metadata = fm.metadata

                links = []
                for label in get_links(content):
                    link = get_path(label)
                    if link is not None:
                        links.append(link)

                node = {
                    'title': get_title(metadata, content, source_file),
                    'source_file': source_file,
                    'metadata': metadata,
                    'content': content,
                    'links': links
                }
                print(node)
    # with open(target_filename, 'w', encoding="utf-8") as out_file:
    #     out_file.write(template.render(context))


if __name__ == '__main__':
    main()

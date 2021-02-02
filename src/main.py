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
        output_dir='../output',
):
    input_dir = os.path.abspath(os.path.join(THIS_DIR, input_dir))
    output_dir = os.path.abspath(os.path.join(THIS_DIR, output_dir))

    shutil.rmtree(output_dir)

    # Output dir
    os.makedirs(output_dir, exist_ok=False)

    # Inverted index, used to handle Obsidian's 'shortest path' strategy
    exclude = {'.git', '.obsidian', '.trash'}
    names_relpath = build_inverted_index(input_dir, exclude)
    get_path = partial(label_to_path, names_relpath)

    # Preparing the template
    for root, dirs, files in os.walk(input_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]

        target_path = root.replace(input_dir, output_dir)
        os.makedirs(target_path, exist_ok=True)

        for file_name in files:
            source_file = os.path.join(root, file_name)
            name, extension = os.path.splitext(file_name)

            # Copy things that are not markdown
            if not extension == '.md':
                target_file = os.path.join(target_path, file_name)
                copyfile(source_file, target_file)
            else:
                # Otherwise generate an HTML

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

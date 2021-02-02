import os
import re

from bs4 import BeautifulSoup

def build_inverted_index(input_dir,exclude):
    names_relpath = {}
    for current_dir, dirs, files in os.walk(input_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if file not in names_relpath:
                names_relpath[file] = []
            relative_path = os.path.relpath(current_dir, start=input_dir)
            names_relpath[file].append(relative_path)
    return names_relpath

def label_to_path(inverted_index,label):

    # If the label contains a pipe '|', then it has an alias.
    tokens = label.split(sep='|', maxsplit=1)
    assert (len(tokens) in {1, 2})
    name, label_extension = os.path.splitext(tokens[0])

    file = f'{name}.md' if label_extension == '' else tokens[0]

    # Obsidian's way
    # If the label does not contain a path, it's unique. We lookup the path.
    # Otherwise, we do nothing
    dir, filename = os.path.split(file)
    if filename not in inverted_index:
        # The reference does not exist
        result = None
    elif dir == '':
        # Lookup the path
        paths = inverted_index[file]
        assert (len(paths) == 1)
        result = os.path.join(paths[0], name)
    else:
        # Has already the path
        result = name
    return result


def get_links(contents):
    WIKILINK_RE = r'\[\[([^\]\]]+)\]\]'
    pattern = re.compile(WIKILINK_RE)
    return pattern.findall(contents)


def get_title(metadata,content,source_file):
    if 'title' in metadata:
        title = metadata['title']
    else:
        bs = BeautifulSoup(content, 'html.parser')
        h1 = bs.find('h1')
        if h1 is not None:
            title = h1.get_text()
        else:
            _, title = os.path.split(source_file)
    return title


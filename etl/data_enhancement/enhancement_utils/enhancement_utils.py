from bs4 import BeautifulSoup


def replace_text_in_node(data, identifier, find, replacement):
    for posts in data:
        enhanced_entry = posts[identifier]
        enhanced_entry = enhanced_entry.replace(find, replacement)
        posts[identifier] = enhanced_entry
    return data

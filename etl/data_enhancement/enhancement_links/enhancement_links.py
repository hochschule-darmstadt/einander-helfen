from bs4 import BeautifulSoup


def fix_mail_to_links(data, identifier):
    for posts in data:
        soup = BeautifulSoup(posts[identifier], 'html.parser')
        links = soup.findAll('a')
        for link in links:
            if 'mailto' not in link.decode():
                link['rel'] = 'noopener'
        posts[identifier] = soup.decode()
    return data


def fix_target_blank(data, identifier):
    for posts in data:
        soup = BeautifulSoup(posts[identifier], 'html.parser')
        links = soup.findAll('a')
        for link in links:
            if 'mailto' not in link.decode():
                link['target'] = '_blank'
                link['rel'] = 'noopener'
        posts[identifier] = soup.decode()
    return data

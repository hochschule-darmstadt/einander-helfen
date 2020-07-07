def run(data):
    enhanced_data_map = add_map_address(data)
    enhanced_data_organization = fix_organization_links(enhanced_data_map)
    enhanced_data_contact = fix_contact_target_link(enhanced_data_organization)
    enhanced_data = fix_task_target_link(enhanced_data_contact)
    return enhanced_data


def fix_organization_links(file):
    for posts in file:
        new_organization = posts['organization']
        new_organization = new_organization.replace('_self', '_blank')
        new_organization = new_organization.replace('/index.cfm', 'https://www.ehrenamtssuche-hessen.de/index.cfm')
        posts['organization'] = new_organization
    return file


def fix_contact_target_link(file):
    add_target_blank(file, 'contact')
    return file


def fix_task_target_link(file):
    add_target_blank(file, 'task')
    return file


def add_target_blank(file, post_key: str):
    from bs4 import BeautifulSoup
    for posts in file:
        soup = BeautifulSoup(posts[post_key], 'html.parser')
        links = soup.findAll('a')
        for link in links:
            if 'mailto' not in link.decode():
                link['target'] = '_blank'
        posts[post_key] = soup.decode()


def add_map_address(file):
    for post in file:
        post['map_address'] = ''
    return file

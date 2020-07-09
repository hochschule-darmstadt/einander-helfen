# run method enhances data with given enhancement methods
def run(data):
    enhanced_data_map = add_map_address(data)
    enhanced_data_organization = fix_organization_links(enhanced_data_map)
    enhanced_data_contact = fix_contact_target_link(enhanced_data_organization)
    enhanced_data = fix_task_target_link(enhanced_data_contact)
    return enhanced_data


# fixes the crawled internal links of ehrenamtsuche-hessen to external link which can be accessed from our page
# changes target from _self to _blank and adds rel _noopener to suppress js injection on target _blank
def fix_organization_links(file):
    from bs4 import BeautifulSoup
    for posts in file:
        new_organization = posts['organization']
        new_organization = new_organization.replace('_self', '_blank')
        new_organization = new_organization.replace('/index.cfm', 'https://www.ehrenamtssuche-hessen.de/index.cfm')
        posts['organization'] = new_organization
        soup = BeautifulSoup(posts['organization'], 'html.parser')
        links = soup.findAll('a')
        for link in links:
            if 'mailto' not in link.decode():
                link['rel'] = 'noopener'
        posts['organization'] = soup.decode()
    return file


# adds the target _blank to contact field
def fix_contact_target_link(file):
    add_target_blank(file, 'contact')
    return file


# adds the target _blank to task field
def fix_task_target_link(file):
    add_target_blank(file, 'task')
    return file


# target _blank method which converts the field with given key to soup object and adds target _blank and
# rel noopener
def add_target_blank(file, post_key: str):
    from bs4 import BeautifulSoup
    for posts in file:
        soup = BeautifulSoup(posts[post_key], 'html.parser')
        links = soup.findAll('a')
        for link in links:
            if 'mailto' not in link.decode():
                link['target'] = '_blank'
                link['rel'] = 'noopener'
        posts[post_key] = soup.decode()


# dummy add map address function which should be used to find lat and lon of the address
# not needed in here since lat and lon are already queried from the domain
def add_map_address(file):
    for post in file:
        post['map_address'] = ''
    return file

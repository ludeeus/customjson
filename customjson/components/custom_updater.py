"""Generate json form old custom_updater format."""
import requests
from customjson.defaults import REUSE, BLACKLIST, DOMAINS


BASE = 'https://raw.githubusercontent.com/{}/master/'
JSONFILES = [
    {
        'repository': 'pnbruckner/homeassistant-config',
        'jsonfile': 'custom_components.json'
    },
    {
        'repository': 'robmarkcole/Hue-sensors-HASS',
        'jsonfile': 'custom_updater.json'
    }
]


def get_data(github):
    """Generate json form old custom_updater format."""
    data = {}
    try:
        for entry in JSONFILES:
            repository = entry['repository']
            jsonfile = entry['jsonfile']
            username = repository.split('/')[0]
            reponame = repository.split('/')[1]
            jsondata = requests.get(BASE.format(repository)+jsonfile).json()
            components = []
            for component in jsondata:
                if component not in BLACKLIST:
                    components.append(component)

            for component in components:
                try:
                    name = component
                    if '.' in name:
                        if name.split('.')[0] not in DOMAINS:
                            continue
                    repo = github.get_repo(repository)
                    print("Generating json for:", "{}/{}".format(
                        repository, name))

                    local_location = jsondata[name]['local_location']
                    version = jsondata[name]['version']
                    updated_at = jsondata[name]['updated_at']
                    changelog = jsondata[name]['changelog']
                    remote_location = jsondata[name]['remote_location']

                    locationformat = 'custom_components/{}/{}.py'
                    embedded_path = locationformat.format(
                        name.split('.')[1], name.split('.')[0])

                    embedded_path_remote = remote_location
                    try:
                        domain = name.split('.')[0]
                        platfrom = name.split('.')[1]
                        path = remote_location.split('/')
                        searchstr = "{}/{}".format(path[-2], path[-1])
                        replacestr = "{}/{}.py".format(platfrom, domain)
                        embedded_path_remote = remote_location.replace(
                            searchstr, replacestr)
                    except Exception:  # pylint: disable=W0703
                        pass

                    embedded_path = embedded_path_remote.split('/master/')[1]

                    try:
                        repo.get_file_contents(embedded_path)
                        embedded = True
                    except Exception:  # pylint: disable=W0703
                        embedded = False

                    description = requests.get(remote_location).text
                    description = description.split('\n')
                    description = description[1] + ' ' + description[2]

                    author = {}
                    author['login'] = username
                    author['html_url'] = 'https://github.com/' + username
                    visit_repo = 'https://github.com/' + repository

                    data[name] = {}
                    data[name]['author'] = author
                    data[name]['updated_at'] = updated_at
                    data[name]['description'] = description
                    data[name]['version'] = version
                    data[name]['local_location'] = local_location
                    data[name]['remote_location'] = remote_location
                    data[name]['visit_repo'] = visit_repo
                    data[name]['changelog'] = changelog
                    data[name]['embedded'] = embedded
                    data[name]['embedded_path'] = '/{}'.format(embedded_path)
                    data[name]['embedded_path_remote'] = REUSE.format(
                        username, reponame, embedded_path)
                except Exception as error:  # pylint: disable=W0703
                    print(error)
    except Exception as error:  # pylint: disable=W0703
        print(error)
    return data

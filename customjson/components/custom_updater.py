"""Generate json form old custom_updater format."""
import requests
from customjson.defaults import REUSE, BLACKLIST


BASE = 'https://raw.githubusercontent.com/{}/master/'
JSONFILES = [
    {
        'repository': 'robmarkcole/Hue-sensors-HASS',
        'jsonfile': 'custom_updater.json'
    }
]


def get_data(github):
    """Generate json form robmarkcole."""
    data = {}
    try:
        for entry in JSONFILES:
            repository = entry['repository']
            jsonfile = entry['jsonfile']
            username = repository.split('/')[0]
            reponame = repository.split('/')[1]
            jsondata = requests.get(BASE + jsonfile).json()
            components = []
            for component in jsondata:
                if component not in BLACKLIST:
                    components.append(component)

            for component in components:
                try:
                    name = component
                    repo = github.get_repo('robmarkcole/Hue-sensors-HASS')
                    print("Generating json for:", "{}/{}".format(
                        repository, name))

                    locationformat = 'custom_components/{}/{}.py'
                    location = locationformat.format(
                        name.split('.')[0], name.split('.')[1])
                    embedded_path = locationformat.format(
                        name.split('.')[1], name.split('.')[0])

                    try:
                        repo.get_file_contents(embedded_path)
                        embedded = True
                    except Exception:  # pylint: disable=W0703
                        embedded = False

                    local_location = '/{}'.format(location)
                    version = jsondata[name]['version']
                    updated_at = jsondata[name]['updated_at']
                    changelog = jsondata[name]['changelog']
                    remote_location = REUSE.format(
                        username, reponame, location)

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
                except Exception:  # pylint: disable=W0703
                    pass
    except Exception:  # pylint: disable=W0703
        pass
    return data

"""Generate json form pnbruckner."""
import requests
from customjson.defaults import REUSE, SKIP_REPOS


def get_data(github, selected_repos):
    """Generate json form pnbruckner."""
    try:
        user = 'pnbruckner/homeassistant-config'
        pnbruckner = github.get_repo('pnbruckner/homeassistant-config')
        base_raw = 'https://raw.githubusercontent.com/{}/master/'.format(user)
        jsondata = requests.get(base_raw + 'custom_components.json').json()
        data = {}
        repos = []
        if selected_repos:
            for repo in selected_repos:
                repos.append(repo)
        else:
            for repo in jsondata:
                if repo not in SKIP_REPOS:
                    repos.append(repo)

        author = {}
        author['login'] = 'pnbruckner'
        author['html_url'] = 'https://github.com/pnbruckner'
        visit_repo = 'https://github.com/pnbruckner/homeassistant-config'

        for repo in repos:
            try:
                name = repo

                locationformat = 'custom_components/{}/{}.py'
                location = locationformat.format(
                    name.split('.')[0], name.split('.')[1])
                embedded_path = locationformat.format(
                    name.split('.')[1], name.split('.')[0])

                try:
                    pnbruckner.get_file_contents(embedded_path)
                    embedded = True
                except Exception:  # pylint: disable=W0703
                    embedded = False

                local_location = '/{}'.format(location)
                version = jsondata[name]['version']
                updated_at = jsondata[name]['updated_at']
                changelog = jsondata[name]['changelog']
                remote_location = REUSE.format(
                    'pnbruckner', 'homeassistant-config', location)

                description = requests.get(remote_location).text.split('\n')
                description = description[1] + ' ' + description[2]

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
                    'pnbruckner', 'homeassistant-config', embedded_path)
            except Exception:  # pylint: disable=W0703
                pass
    except Exception:  # pylint: disable=W0703
        pass
    return data

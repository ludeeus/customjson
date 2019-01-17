"""Generate json form custom-components org."""
from customjson.defaults import REUSE, VISIT, SKIP_REPOS


def get_data(github, selected_repos):
    """Generate json form custom-components org."""
    org = 'custom-components'
    json = {}
    repos = []
    if selected_repos:
        for repo in selected_repos:
            repos.append(repo)
    else:
        for repo in list(github.get_user(org).get_repos()):
            repos.append(repo.name)
    for repo in repos:
        try:
            repo = github.get_repo(org + '/' + repo)
            if repo.name not in SKIP_REPOS and not repo.archived:
                print("Generating json for:", "{}/{}".format(org, repo.name))
                name = repo.name
                updated_at = repo.updated_at.isoformat().split('T')[0]
                if len(name.split('.')) > 1:
                    locationformat = 'custom_components/{}/{}.py'
                    location = locationformat.format(name.split('.')[0],
                                                     name.split('.')[1])
                    embedded_path = locationformat.format(name.split('.')[1],
                                                          name.split('.')[0])
                else:
                    location = 'custom_components/{}.py'.format(name)
                    embedded_path = location
                    try:
                        repo.get_file_contents(location)
                    except Exception:  # pylint: disable=W0703
                        location = 'custom_components/{}/__init__.py'
                        location = location.format(name)
                        embedded_path = location

                try:
                    repo.get_file_contents(embedded_path)
                    embedded = True
                except Exception:  # pylint: disable=W0703
                    embedded = False

                version = None  # reset
                try:
                    if embedded:
                        path = embedded_path
                    else:
                        path = location
                    content = repo.get_file_contents(path)
                    content = content.decoded_content.decode().split('\n')
                    for line in content:
                        if '_version_' in line or 'VERSION' in line:
                            version = line.split(' = ')[1].replace("'", "")
                            break
                except Exception:  # pylint: disable=W0703
                    version = None

                try:
                    releases = list(repo.get_releases())
                    changelog = releases[0].html_url
                    if 'untagged' in changelog:
                        changelog = releases[1].html_url
                    if 'untagged' in changelog:
                        changelog = VISIT.format(org, name)
                except Exception:  # pylint: disable=W0703
                    changelog = VISIT.format(org, name)

                try:
                    repo.get_file_contents('example.png')
                    image_link = REUSE.format(org, name, 'example.png')
                except Exception:  # pylint: disable=W0703
                    image_link = ''

                updated_at = updated_at
                version = version
                description = repo.description
                remote_location = REUSE.format(org, name, location)
                visit_repo = VISIT.format(org, name)
                changelog = changelog

                authordata = list(repo.get_contributors())[0]

                legacy = {}
                legacy['updated_at'] = updated_at
                legacy['version'] = version
                legacy['local_location'] = '/{}'.format(location)
                legacy['remote_location'] = remote_location
                legacy['visit_repo'] = visit_repo
                legacy['changelog'] = changelog

                data = {
                    'author': {
                        'login': authordata.login,
                        'url': authordata.html_url
                    },
                    'repo': repo,
                    'version': version,
                    'description': description,
                    'embedded': embedded,
                    'url': {
                        'html': visit_repo,
                        'changelog': changelog,
                        'image': image_link,
                        'raw': REUSE.format(org, name, ''),
                    },
                    'path': {
                        'local': '/{}'.format(embedded_path),
                        'remote': REUSE.format(org, name, embedded_path),
                        'legacy': {
                            'local': '/{}'.format(location),
                            'remote': REUSE.format(org, name, location)
                        }
                    }
                }

                json[name] = {'legacy': legacy, 'data': data}
        except Exception:  # pylint: disable=W0703
            pass

    return json

"""Generate json form isabellaalstrom."""
from customjson.defaults import REUSE, VISIT


def get_isabellaalstrom(github, selected_repos):
    """Generate json form isabellaalstrom."""
    org = 'isabellaalstrom'
    json = {}
    repos = []
    all_repos = ['sensor.krisinformation']
    if selected_repos:
        for repo in selected_repos:
            if repo in all_repos:
                repos.append(repo)
    else:
        repos = all_repos
    for repo in repos:
        try:
            repo = github.get_repo(org + '/' + repo)
            print("Generating json for:", "{}/{}".format(org, repo.name))
            name = repo.name
            updated_at = repo.updated_at.isoformat().split('T')[0]
            locationformat = 'custom_components/{}/{}.py'
            location = locationformat.format(name.split('.')[0],
                                             name.split('.')[1])
            embedded_path = locationformat.format(name.split('.')[1],
                                                  name.split('.')[0])

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
                    if '__version__' in line:
                        version = line.split(' = ')[1].replace("'", "")
                        break
            except Exception:  # pylint: disable=W0703
                version = None

            try:
                repo.get_file_contents('example.png')
                image_link = REUSE.format(org, name, 'example.png')
            except Exception:  # pylint: disable=W0703
                image_link = ''

            updated_at = updated_at
            version = version
            description = repo.description
            local_location = '/{}'.format(location)
            remote_location = REUSE.format(org, name, location)
            visit_repo = VISIT.format(org, name)
            changelog = visit_repo

            legacy = {}
            legacy['updated_at'] = updated_at
            legacy['version'] = version
            legacy['local_location'] = local_location
            legacy['remote_location'] = remote_location
            legacy['visit_repo'] = visit_repo
            legacy['changelog'] = changelog

            data = {
                'author': {
                    'login': 'isabellaalstrom',
                    'url': 'https://github.com/isabellaalstrom'
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
                        'local': local_location,
                        'remote': remote_location
                    }
                }
            }

            json[name] = {'legacy': legacy, 'data': data}
        except Exception:  # pylint: disable=W0703
            pass
    return json

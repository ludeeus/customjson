"""Generate json form isabellaalstrom."""
from customjson.defaults import REUSE, VISIT, SKIP_REPOS


def get_data(github, selected_repos):
    """Generate json form isabellaalstrom."""
    org = 'isabellaalstrom'
    data = {}
    repos = ['sensor.krisinformation']
    if selected_repos:
        for repo in selected_repos:
            repos.append(repo)
    else:
        for repo in list(github.get_user(org).get_repos()):
            repos.append(repo.name)
    for repo in repos:
        repo = github.get_repo(org + '/' + repo)
        if repo.name not in SKIP_REPOS and not repo.archived:
            print("Generating json for repo:", repo.name)
            name = repo.name
            updated_at = repo.updated_at.isoformat().split('T')[0]
            location = 'custom_components/{}/{}.py'
            location = location.format(name.split('.')[0],
                                       name.split('.')[1])
            content = repo.get_file_contents(location)
            content = content.decoded_content.decode().split('\n')
            for line in content:
                if '__version__' in line:
                    version = line.split(' = ')[1].replace("'", "")
                    break

            updated_at = updated_at
            version = version
            local_location = '/{}'.format(location)
            remote_location = REUSE.format(org, name, location)
            visit_repo = VISIT.format(org, name)
            changelog = visit_repo

            data[name] = {}
            data[name]['updated_at'] = updated_at
            data[name]['version'] = version
            data[name]['local_location'] = local_location
            data[name]['remote_location'] = remote_location
            data[name]['visit_repo'] = visit_repo
            data[name]['changelog'] = changelog
    return data

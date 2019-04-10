"""Generate json form isabellaalstrom."""
from customjson.defaults import REUSE, VISIT


def get_isabellaalstrom(github, selected_repos):
    """Generate json form isabellaalstrom."""
    org = "isabellaalstrom"
    data = {}
    repos = []
    all_repos = ["krisinfo-card", "pollenkoll-card"]
    if selected_repos:
        for repo in selected_repos:
            if repo in all_repos:
                repos.append(repo)
    else:
        repos = all_repos
    for repo in repos:
        try:
            repo = github.get_repo(org + "/" + repo)
            name = repo.name
            print("Generating json for:", "{}/{}".format(org, name))

            content = repo.get_file_contents("VERSION")
            content = content.decoded_content.decode()
            version = content.split()[0]

            remote_location = REUSE.format(org, name, name)
            remote_location = remote_location + ".js"

            visit_repo = VISIT.format(org, name)

            changelog = visit_repo

            data[name] = {}
            data[name]["version"] = version
            data[name]["remote_location"] = remote_location
            data[name]["visit_repo"] = visit_repo
            data[name]["changelog"] = changelog
        except Exception:  # pylint: disable=W0703
            pass
    return data

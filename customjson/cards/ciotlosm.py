"""Generate json form ciotlosm."""
from customjson.defaults import VISIT


def get_data(github, selected_repos):
    """Generate json form ciotlosm."""
    ciotlosm = github.get_repo("ciotlosm/custom-lovelace")
    data = {}
    repos = []
    if selected_repos:
        for repo in selected_repos:
            repos.append(repo)
    else:
        for repo in list(ciotlosm.get_dir_contents("")):
            if repo.path not in ["LICENSE", "README.md"]:
                repos.append(repo.path)
    for repo in repos:
        try:
            name = repo

            version = ciotlosm.get_file_contents(name + "/VERSION")
            version = version.decoded_content.decode()
            version = version.split()[0]

            # This line has to start here, due to the validation.
            print("Generating json for:", "{}/{}".format("ciotlosm", name))

            visit_repo = VISIT.format("ciotlosm", "custom-lovelace")
            visit_repo = visit_repo + "/tree/master/" + name

            changelog = visit_repo + "/changelog.md"

            remote_location = "https://raw.githubusercontent.com/ciotlosm/"
            remote_location = remote_location + "custom-lovelace/master/"
            remote_location = remote_location + name + "/" + name + ".js"

            data[name] = {}
            data[name]["version"] = version
            data[name]["remote_location"] = remote_location
            data[name]["visit_repo"] = visit_repo
            data[name]["changelog"] = changelog
        except Exception:  # pylint: disable=W0703
            pass
    return data

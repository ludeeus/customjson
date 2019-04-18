"""Generate json form custom-cards org."""
import requests
from customjson.defaults import REUSE, REUSE_TAG, VISIT, BLACKLIST


def get_data(github, selected_repos):
    """Generate json form custom-cards org."""
    org = "custom-cards"
    data = {}
    repos = []
    if selected_repos:
        repos.append(selected_repos)
    else:
        for repo in list(github.get_user(org).get_repos()):
            repos.append(repo.name)
    for repo in repos:
        try:
            repo = github.get_repo(org + "/" + repo)
            if repo.name not in BLACKLIST and not repo.archived:
                print("Generating json for:", "{}/{}".format(org, repo.name))

                try:
                    release = list(repo.get_releases())[0]
                except Exception:  # pylint: disable=W0703
                    release = None

                name = repo.name

                version = None
                try:
                    if release and release.tag_name is not None:
                        version = release.tag_name
                    else:
                        content = repo.get_file_contents("VERSION")
                        content = content.decoded_content.decode()
                        version = content.split()[0]
                except Exception:  # pylint: disable=W0703
                    version = None

                if release:
                    remote_location = REUSE_TAG.format(org, name, version, name)
                else:
                    remote_location = REUSE.format(org, name, name)

                remote_location = remote_location + ".js"
                testfile = requests.get(remote_location)

                if testfile.status_code != 200:
                    remote_location = remote_location.split(name + ".js")[0]
                    remote_location = remote_location + "dist/" + name + ".js"
                    testfile = requests.get(remote_location)

                if testfile.status_code != 200:
                    remote_location = remote_location.split("dist/" + name + ".js")[0]
                    remote_location = remote_location + "src/" + name + ".js"
                    testfile = requests.get(remote_location)

                if testfile.status_code != 200:
                    continue

                visit_repo = VISIT.format(org, name)

                try:
                    changelog = list(repo.get_releases())[0].html_url
                    if "untagged" in list(repo.get_releases())[0].name:
                        changelog = None
                except Exception:  # pylint: disable=W0703
                    changelog = None

                if changelog is None:
                    changelog = VISIT.format(org, name)

                data[name] = {}
                data[name]["version"] = version
                data[name]["remote_location"] = remote_location
                data[name]["visit_repo"] = visit_repo
                data[name]["changelog"] = changelog
        except Exception as error:  # pylint: disable=W0703
            print(error)
    return data

"""Generate json form custom-components org."""
import json
from customjson.defaults import REUSE, VISIT, BLACKLIST


def get_data(github, selected_repos):
    """Generate json form custom-components org."""
    org = "custom-components"
    data = {}
    repos = []
    if selected_repos:
        for repo in selected_repos:
            repos.append(repo)
    else:
        for repo in list(github.get_user(org).get_repos()):
            repos.append(repo.name)
    for repo in repos:
        try:
            repo = github.get_repo(org + "/" + repo)
            if repo.name not in BLACKLIST and not repo.archived:
                print("Generating json for:", "{}/{}".format(org, repo.name))
                name = repo.name

                resources = []
                updated_at = repo.updated_at.isoformat().split("T")[0]
                if "." in name:
                    locationformat = "custom_components/{}/{}.py"
                    location = locationformat.format(
                        name.split(".")[0], name.split(".")[1]
                    )
                    embedded_path = locationformat.format(
                        name.split(".")[1], name.split(".")[0]
                    )

                    try:
                        repo.get_file_contents(embedded_path)
                        embedded = True
                    except Exception:  # pylint: disable=W0703
                        embedded = False

                else:
                    location = "custom_components/{}.py".format(name)
                    embedded_path = location
                    embedded = True
                    try:
                        repo.get_file_contents(location)
                    except Exception:  # pylint: disable=W0703
                        location = "custom_components/{}/__init__.py"
                        location = location.format(name)
                        embedded_path = location

                try:
                    release = list(repo.get_releases())[0]
                except Exception:  # pylint: disable=W0703
                    release = None

                version = None

                try:
                    resources = json.loads(
                        repo.get_file_contents(
                            "resources.json"
                        ).decoded_content.decode()
                    )
                except Exception:  # pylint: disable=W0703
                    pass

                try:
                    if embedded:
                        path = embedded_path
                    else:
                        path = location
                    content = repo.get_file_contents(path)
                    content = content.decoded_content.decode().split("\n")
                    for line in content:
                        if "_version_" in line or "VERSION" in line:
                            version = line.split(" = ")[1].replace("'", "")
                            break
                except Exception:  # pylint: disable=W0703
                    version = None

                if version is None:
                    try:
                        if release and release.tag_name is not None:
                            version = release.tag_name
                        else:
                            version = None
                    except Exception:  # pylint: disable=W0703
                        version = None

                try:
                    releases = list(repo.get_releases())
                    changelog = releases[0].html_url
                    if "untagged" in changelog:
                        changelog = releases[1].html_url
                    if "untagged" in changelog:
                        changelog = VISIT.format(org, name)
                except Exception:  # pylint: disable=W0703
                    changelog = VISIT.format(org, name)

                try:
                    repo.get_file_contents("example.png")
                    image_link = REUSE.format(org, name, "example.png")
                except Exception:  # pylint: disable=W0703
                    image_link = ""

                updated_at = updated_at
                version = version
                description = repo.description
                local_location = "/{}".format(location)
                remote_location = REUSE.format(org, name, location)
                embedded_path_remote = REUSE.format(org, name, embedded_path)
                visit_repo = VISIT.format(org, name)
                changelog = changelog

                authordata = list(repo.get_contributors())[0]
                author = {}
                author["login"] = authordata.login
                author["html_url"] = authordata.html_url

                data[name] = {}
                data[name]["author"] = author
                data[name]["updated_at"] = updated_at
                data[name]["version"] = version
                data[name]["description"] = description
                data[name]["image_link"] = image_link
                data[name]["local_location"] = local_location
                data[name]["remote_location"] = remote_location
                data[name]["visit_repo"] = visit_repo
                data[name]["changelog"] = changelog
                data[name]["resources"] = resources
                data[name]["embedded"] = embedded
                data[name]["embedded_path"] = "/{}".format(embedded_path)
                data[name]["embedded_path_remote"] = embedded_path_remote
        except Exception:  # pylint: disable=W0703
            pass
    return data

"""Generate json form isabellaalstrom."""
from customjson.defaults import REUSE, VISIT


def get_isabellaalstrom(github, selected_repos):
    """Generate json form isabellaalstrom."""
    org = "isabellaalstrom"
    data = {}
    repos = []
    all_repos = ["sensor.krisinformation"]
    if selected_repos:
        for repo in selected_repos:
            if repo in all_repos:
                repos.append(repo)
    else:
        repos = all_repos
    for repo in repos:
        try:
            repo = github.get_repo(org + "/" + repo)
            print("Generating json for:", "{}/{}".format(org, repo.name))
            name = repo.name
            resources = []
            updated_at = repo.updated_at.isoformat().split("T")[0]
            locationformat = "custom_components/{}/{}.py"
            location = locationformat.format(name.split(".")[0], name.split(".")[1])
            embedded_path = locationformat.format(
                name.split(".")[1], name.split(".")[0]
            )

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
                content = content.decoded_content.decode().split("\n")
                for line in content:
                    if "__version__" in line:
                        version = line.split(" = ")[1].replace("'", "")
                        break
            except Exception:  # pylint: disable=W0703
                version = None

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
            visit_repo = VISIT.format(org, name)
            changelog = visit_repo

            author = {}
            author["login"] = "isabellaalstrom"
            author["html_url"] = "https://github.com/isabellaalstrom"

            data[name] = {}
            data[name]["author"] = author
            data[name]["updated_at"] = updated_at
            data[name]["description"] = description
            data[name]["image_link"] = image_link
            data[name]["version"] = version
            data[name]["local_location"] = local_location
            data[name]["remote_location"] = remote_location
            data[name]["visit_repo"] = visit_repo
            data[name]["changelog"] = changelog
            data[name]["resources"] = resources
            data[name]["embedded"] = embedded
            data[name]["embedded_path"] = "/{}".format(embedded_path)
            data[name]["embedded_path_remote"] = REUSE.format(org, name, embedded_path)
        except Exception:  # pylint: disable=W0703
            pass
    return data

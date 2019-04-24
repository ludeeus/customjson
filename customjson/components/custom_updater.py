"""Generate json form old custom_updater format."""
import requests
from customjson.defaults import REUSE, BLACKLIST, DOMAINS


BASE = "https://raw.githubusercontent.com/{}/master/"
JSONFILES = [
    {
        "repository": "pnbruckner/homeassistant-config",
        "jsonfile": "custom_components.json",
    },
    {"repository": "robmarkcole/Hue-sensors-HASS", "jsonfile": "custom_updater.json"},
    {
        "repository": "claytonjn/hass-circadian_lighting",
        "jsonfile": "custom_updater.json",
    },
    {"repository": "StyraHem/hass", "jsonfile": "custom_updater.json"},
]


def get_data():
    """Generate json form old custom_updater format."""
    data = {}
    try:
        for entry in JSONFILES:
            repository = entry["repository"]
            jsonfile = entry["jsonfile"]
            username = repository.split("/")[0]
            jsondata = requests.get(BASE.format(repository) + jsonfile).json()
            components = []
            for component in jsondata:
                if component not in BLACKLIST:
                    components.append(component)

            for component in components:
                try:
                    name = component
                    if "." in name:
                        if name.split(".")[0] not in DOMAINS:
                            continue
                    print("Generating json for:", "{}/{}".format(repository, name))
                    version = jsondata[name]["version"]
                    updated_at = jsondata[name]["updated_at"]
                    local_location = jsondata[name]["local_location"]
                    remote_location = jsondata[name]["remote_location"]
                    visit_repo = jsondata[name]["visit_repo"]
                    changelog = jsondata[name]["changelog"]
                    resources = jsondata[name].get("resources", [])

                    embedded = True

                    author = {}
                    author["login"] = username
                    author["html_url"] = "https://github.com/" + username

                    data[name] = {}
                    data[name]["author"] = author
                    data[name]["updated_at"] = updated_at
                    data[name]["version"] = version
                    data[name]["embedded_path"] = local_location
                    data[name]["embedded_path_remote"] = remote_location
                    data[name]["visit_repo"] = visit_repo
                    data[name]["changelog"] = changelog
                    data[name]["resources"] = resources
                    data[name]["embedded"] = embedded
                except Exception as error:  # pylint: disable=W0703
                    print(error)
    except Exception as error:  # pylint: disable=W0703
        print(error)
    return data

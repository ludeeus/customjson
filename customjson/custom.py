"""Create json with information for custom_updater."""
import json
import random
from github import Github
from github.GithubException import UnknownObjectException
from customjson.defaults import COMMIT


class CreateJson:
    """Class for json creation."""

    def __init__(self, token, push, repo=None):
        """Initilalize."""
        self.token = token
        self.repo = repo
        self.selected = repo
        self.push = push
        self.github = Github(token)

    def component(self):
        """Generate json for components."""
        from customjson.components.org import get_data as org
        from customjson.components.isabellaalstrom import get_isabellaalstrom
        from customjson.components.custom_updater import get_data as custom_updater

        organisation = "custom-components"
        data = {}

        components = org(self.github, self.repo)
        for component in components:
            data[component] = components[component]

        components = get_isabellaalstrom(self.github, self.repo)
        for component in components:
            data[component] = components[component]

        components = custom_updater()
        for component in components:
            data[component] = components[component]

        components = data
        legacy = {}
        data = {}

        for component in components:
            changelog = components[component].get("changelog", "")
            local_location = components[component].get("local_location", "")
            remote_location = components[component].get("remote_location", "")
            updated_at = components[component].get("updated_at", "")
            version = components[component].get("version", "")
            visit_repo = components[component].get("visit_repo", "")
            author = components[component].get("author", "")
            resources = components[component].get("resources", [])
            description = components[component].get("description", "")
            image_link = components[component].get("image_link", "")
            embedded = components[component].get("embedded", "")
            embedded_path = components[component].get("embedded_path", "")
            embedded_path_remote = components[component].get("embedded_path_remote", "")

            legacy[component] = {}
            legacy[component]["changelog"] = changelog
            legacy[component]["local_location"] = embedded_path
            if embedded:
                legacy[component]["remote_location"] = embedded_path_remote
            else:
                legacy[component]["remote_location"] = remote_location
            legacy[component]["updated_at"] = updated_at
            legacy[component]["version"] = version
            legacy[component]["visit_repo"] = visit_repo
            legacy[component]["resources"] = resources

            data[component] = {}
            data[component]["author"] = author
            data[component]["version"] = version
            data[component]["description"] = description
            data[component]["image_link"] = image_link
            data[component]["local_location"] = local_location
            data[component]["remote_location"] = remote_location
            data[component]["visit_repo"] = visit_repo
            data[component]["changelog"] = changelog
            data[component]["resources"] = resources
            data[component]["embedded"] = embedded
            data[component]["embedded_path"] = embedded_path
            data[component]["embedded_path_remote"] = embedded_path_remote

        if self.push:
            target = "repos.json"
            repo = self.github.get_repo(organisation + "/information")
            repos_json = repo.get_contents(target)
            old = json.loads(repos_json.decoded_content.decode())
            sha = repos_json.sha
            msg = random.choice(COMMIT)
            raw = legacy
            legacy = json.dumps(legacy, indent=4, sort_keys=True)
            if not legacy:
                print("no data")
                return
            try:
                if has_changed(old, raw):
                    print(repo.update_file(target, msg, legacy, sha))
                else:
                    print("content did not change")
            except UnknownObjectException:
                message = "You do not have premissions to push to {}/{}"
                print(message.format(organisation + "/information"))
            except Exception as error:  # pylint: disable=W0703
                print("Something went horrible wrong :(")
                print(error)
            target = "custom-component-store/V1/data.json"
            repo = self.github.get_repo("ludeeus/data")
            repos_json = repo.get_contents(target)
            old = json.loads(repos_json.decoded_content.decode())
            sha = repos_json.sha
            msg = random.choice(COMMIT)
            raw = data
            data = json.dumps(data, indent=4, sort_keys=True)
            if not data:
                print("no data")
                return
            try:
                if has_changed(old, raw):
                    print(repo.update_file(target, msg, data, sha))
                else:
                    print("content did not change")
            except UnknownObjectException:
                message = "You do not have premissions to push to ludeeus/data"
                print(message)
            except Exception as error:  # pylint: disable=W0703
                print("Something went horrible wrong :(")
                print(error)
        else:
            print(json.dumps(legacy, indent=4, sort_keys=True))
            print(json.dumps(data, indent=4, sort_keys=True))

    def card(self):
        """Generate json for cards."""
        from customjson.cards.org import get_data as org
        from customjson.cards.ciotlosm import get_data as ciotlosm
        from customjson.cards.isabellaalstrom import get_isabellaalstrom
        from customjson.cards.maykar import get_data as maykar
        from customjson.cards.thomasloven import get_data as thomasloven

        organisation = "custom-cards"
        data = {}

        cards = org(self.github, self.repo)
        for card in cards:
            data[card] = cards[card]

        cards = ciotlosm(self.github, self.repo)
        for card in cards:
            data[card] = cards[card]

        cards = get_isabellaalstrom(self.github, self.repo)
        for card in cards:
            data[card] = cards[card]

        cards = maykar(self.github, self.repo)
        for card in cards:
            data[card] = cards[card]

        cards = thomasloven(self.github, self.repo)
        for card in cards:
            data[card] = cards[card]

        if self.push:
            target = "repos.json"
            repo = self.github.get_repo(organisation + "/information")
            repos_json = repo.get_contents(target)
            sha = repos_json.sha
            msg = random.choice(COMMIT)
            if self.selected:
                old = json.loads(repos_json.decoded_content.decode())
                new = data
                data = {}
                for item in old:
                    data[item] = old[item]
                for item in new:
                    data[item] = new[item]
                print(json.dumps(new, indent=4, sort_keys=True))
            raw = data
            data = json.dumps(data, indent=4, sort_keys=True)
            if not data:
                print("no data")
                return
            try:
                old = json.loads(repos_json.decoded_content.decode())
                if has_changed(old, raw):
                    print(repo.update_file(target, msg, data, sha))
                else:
                    print("content did not change")
            except UnknownObjectException:
                message = "You do not have premissions to push to {}/{}"
                print(message.format(organisation + "/information"))
            except Exception as error:  # pylint: disable=W0703
                print("Something went horrible wrong :(")
                print(error)
        else:
            print(json.dumps(data, indent=4, sort_keys=True))


def has_changed(old, new):
    """Return bool if content has changed."""
    import dictdiffer

    return bool(list(dictdiffer.diff(old, new)))

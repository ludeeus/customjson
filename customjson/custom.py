"""Create json with information for custom_updater."""
import json
import random
from github import Github
from github.GithubException import UnknownObjectException
from customjson.defaults import COMMIT


class CreateJson():
    """Class for json creation."""

    def __init__(self, token, repo, push):
        """Initilalize."""
        self.token = token
        self.repo = repo
        self.selected = any(repo)
        self.push = push
        self.github = Github(token)

    def component(self):
        """Generate json for components."""
        from customjson.components.org import get_data as org
        from customjson.components.isabellaalstrom import get_isabellaalstrom
        from customjson.components.pnbruckner import get_data as pnbruckner

        update_pending = self.customjson_update_pending()

        organisation = 'custom-components'
        data = {}

        components = org(self.github, self.repo)
        for component in components:
            data[component] = components[component]

        components = get_isabellaalstrom(self.github, self.repo)
        for component in components:
            data[component] = components[component]

        components = pnbruckner(self.github, self.repo)
        for component in components:
            data[component] = components[component]

        if self.push:
            target = 'repos.json'
            repo = self.github.get_repo(organisation + '/information')
            repos_json = repo.get_contents(target)
            sha = repos_json.sha
            msg = random.choice(COMMIT)
            if self.selected:
                old = json.loads(repos_json.decoded_content.decode())
                new = data
                data = {}
                for item in old:
                    data[item] = {}
                    for subitem in old[item]:
                        new_value = old[item][subitem].replace("'", "")
                        data[item][subitem] = new_value
                for item in new:
                    data[item] = {}
                    for subitem in new[item]:
                        new_value = new[item][subitem].replace("'", "")
                        data[item][subitem] = new_value
                print(json.dumps(new, indent=4, sort_keys=True))
            data = json.dumps(data, indent=4, sort_keys=True)
            try:
                if not update_pending:
                    print(repo.update_file(target, msg, data, sha))
                else:
                    print("You need to update 'customjson' before pushing.")
            except UnknownObjectException:
                message = "You do not have premissions to push to {}/{}"
                print(message.format(organisation + '/information'))
            except Exception as error:  # pylint: disable=W0703
                print("Something went horrible wrong :(")
                print(error)
        else:
            print(json.dumps(data, indent=4, sort_keys=True))

    def card(self):
        """Generate json for cards."""
        from customjson.cards.org import get_data as org
        from customjson.cards.ciotlosm import get_data as ciotlosm
        from customjson.cards.isabellaalstrom import get_isabellaalstrom
        from customjson.cards.maykar import get_data as maykar
        from customjson.cards.thomasloven import get_data as thomasloven

        update_pending = self.customjson_update_pending()

        organisation = 'custom-cards'
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
            target = 'repos.json'
            repo = self.github.get_repo(organisation + '/information')
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
            data = json.dumps(data, indent=4, sort_keys=True)
            try:
                if not update_pending:
                    print(repo.update_file(target, msg, data, sha))
                else:
                    print("You need to update 'customjson' before pushing.")
            except UnknownObjectException:
                message = "You do not have premissions to push to {}/{}"
                print(message.format(organisation + '/information'))
            except Exception as error:  # pylint: disable=W0703
                print("Something went horrible wrong :(")
                print(error)
        else:
            print(json.dumps(data, indent=4, sort_keys=True))

    def customjson_update_pending(self):
        """Check version for this tool."""
        from customjson.version import __version__
        update_pending = False
        version = __version__
        repo = self.github.get_repo('ludeeus/customjson')
        releases = list(repo.get_releases())
        for release in releases:
            version = release.tag_name
            if version is None:
                pass
            elif 'untagged' in version:
                pass
            else:
                break
        if version != __version__:
            update_pending = True
        return update_pending

"""Create json with information for custom_updater."""
import json
import random
from github import Github
from github.GithubException import UnknownObjectException
import customjson.defaults as ORG


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
        organisation = 'custom-components'
        data = {}

        components = org(self.github, self.repo)
        for component in components:
            data[component] = components[component]

        if self.push:
            target = 'repos.json'
            repo = self.github.get_repo(organisation + '/information')
            repos_json = repo.get_contents(target)
            sha = repos_json.sha
            msg = random.choice(ORG.COMMIT)
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
                print(repo.update_file(target, msg, data, sha))
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
        from customjson.cards.thomasloven import get_data as thomasloven
        organisation = 'custom-cards'
        data = {}

        cards = org(self.github, self.repo)
        for card in cards:
            data[card] = cards[card]

        cards = ciotlosm(self.github, self.repo)
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
            msg = random.choice(ORG.COMMIT)
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
                print(repo.update_file(target, msg, data, sha))
            except UnknownObjectException:
                message = "You do not have premissions to push to {}/{}"
                print(message.format(organisation + '/information'))
            except Exception as error:  # pylint: disable=W0703
                print("Something went horrible wrong :(")
                print(error)
        else:
            print(json.dumps(data, indent=4, sort_keys=True))

"""Create json with information for custom_updater."""
from json import dumps
import random
import requests
from github import Github
import customjson.defaults as ORG


class CreateJson():
    """Class for json creation."""

    def __init__(self, token, repo, push):
        """Initilalize."""
        self.token = token
        self.repo = repo
        self.selected = repo is not None
        self.push = push
        self.github = Github(token)

    def component(self):
        """Generate json for components."""
        org = 'custom-components'
        data = {}
        if not self.repo:
            repos = []
            for repo in list(self.github.get_user(org).get_repos()):
                repos.append(repo.name)
            self.repo = repos
        for repo in self.repo:
            repo = self.github.get_repo(org + '/' + repo)
            if repo.name not in ORG.SKIP_REPOS and not repo.archived:
                print("Generating json for repo:", repo.name)
                name = repo.name
                updated_at = repo.updated_at.isoformat().split('T')[0]
                if len(name.split('.')) > 1:
                    location = 'custom_components/{}/{}.py'
                    location = location.format(name.split('.')[0],
                                               name.split('.')[1])
                else:
                    location = 'custom_components/{}.py'.format(name)
                    try:
                        repo.get_file_contents(location)
                    except Exception:  # pylint: disable=W0703
                        location = 'custom_components/{}/__init__.py'
                        location = location.format(name)

                version = None
                try:
                    content = repo.get_file_contents(location)
                    content = content.decoded_content.decode().split('\n')
                    for line in content:
                        if '_version_' in line or 'VERSION' in line:
                            version = line.split(' = ')[1]
                            break
                except Exception:  # pylint: disable=W0703
                    version = None

                try:
                    changelog = list(repo.get_releases())[0].html_url
                    if 'untagged' in list(repo.get_releases())[0].name:
                        changelog = ORG.VISIT.format(org, name)
                except Exception:  # pylint: disable=W0703
                    changelog = ORG.VISIT.format(org, name)

                updated_at = updated_at
                version = version
                local_location = '/{}'.format(location)
                remote_location = ORG.REUSE.format(org, name, location)
                visit_repo = ORG.VISIT.format(org, name)
                changelog = changelog

                data[name] = {}
                data[name]['updated_at'] = updated_at
                data[name]['version'] = version
                data[name]['local_location'] = local_location
                data[name]['remote_location'] = remote_location
                data[name]['visit_repo'] = visit_repo
                data[name]['changelog'] = changelog

        if self.push:
            if self.selected:
                url = "https://raw.githubusercontent.com/"
                url = url + org + "/information/master/repos.json"
                old = requests.get(url).json()
                new = data
                data = {}
                for name in old:
                    data[name] = old[name]
                for name in new:
                    data[name] = new[name]
            data = dumps(data, indent=4, sort_keys=True)
            target = 'repos.json'
            repo = self.github.get_repo(org + '/information')
            sha = repo.get_contents(target).sha
            msg = random.choice(ORG.COMMIT)
            print(dumps(new, indent=4, sort_keys=True))
            print(repo.update_file(target, msg, data, sha))
        else:
            print(dumps(data, indent=4, sort_keys=True))

    def card(self):
        """Generate json for cards."""
        org = 'custom-cards'
        data = {}
        cards = self.cards_org()
        for card in cards:
            data[card] = cards[card]

        cards = self.cards_thomasloven()
        for card in cards:
            data[card] = cards[card]

        cards = self.cards_ciotlosm()
        for card in cards:
            data[card] = cards[card]

        if self.push:
            if self.selected:
                url = "https://raw.githubusercontent.com/"
                url = url + org + "/information/master/repos.json"
                old = requests.get(url).json()
                new = data
                data = {}
                for name in old:
                    data[name] = old[name]
                for name in new:
                    data[name] = old[name]
            data = dumps(data, indent=4, sort_keys=True)
            target = 'repos.json'
            repo = self.github.get_repo(org + '/information')
            sha = repo.get_contents(target).sha
            msg = random.choice(ORG.COMMIT)
            print(dumps(new, indent=4, sort_keys=True))
            print(repo.update_file(target, msg, data, sha))
        else:
            print(dumps(data, indent=4, sort_keys=True))

    def cards_org(self):
        """Generate json form custom-cards org."""
        org = 'custom-cards'
        data = {}
        repos = []
        if self.repo:
            for repo in self.repo:
                repos.append(repo)
        else:
            for repo in list(self.github.get_user(org).get_repos()):
                repos.append(repo.name)
        for repo in repos:
            try:
                repo = self.github.get_repo(org + '/' + repo)
                if repo.name not in ORG.SKIP_REPOS and not repo.archived:
                    print("Generating json for repo:", repo.name)

                    try:
                        release = list(repo.get_releases())[0]
                    except Exception:  # pylint: disable=W0703
                        release = None

                    name = repo.name

                    updated_at = repo.updated_at.isoformat().split('T')[0]

                    version = None
                    try:
                        if release and release.tag_name is not None:
                            version = release.tag_name
                        else:
                            content = repo.get_file_contents('VERSION')
                            content = content.decoded_content.decode()
                            version = content.split()[0]
                    except Exception:  # pylint: disable=W0703
                        version = None

                    remote_location = ORG.REUSE.format(org, name, name)
                    remote_location = remote_location + '.js'

                    visit_repo = ORG.VISIT.format(org, name)

                    try:
                        changelog = list(repo.get_releases())[0].html_url
                        if 'untagged' in list(repo.get_releases())[0].name:
                            changelog = None
                    except Exception:  # pylint: disable=W0703
                        changelog = None

                    if changelog is None:
                        changelog = ORG.VISIT.format(org, name)

                    data[name] = {}
                    data[name]['updated_at'] = updated_at
                    data[name]['version'] = version
                    data[name]['remote_location'] = remote_location
                    data[name]['visit_repo'] = visit_repo
                    data[name]['changelog'] = changelog
            except Exception:  # pylint: disable=W0703
                pass
        return data

    def cards_thomasloven(self):
        """Generate json form thomasloven."""
        org = 'thomasloven'
        data = {}
        repos = []
        if self.repo:
            for repo in self.repo:
                repos.append(repo)
        else:
            for repo in list(self.github.get_user(org).get_repos()):
                repos.append(repo.name)
        for repo in repos:
            try:
                repo = self.github.get_repo(org + '/' + repo)
                if (repo.name not in ORG.SKIP_REPOS and not repo.archived and
                        'lovelace-' in repo.name):
                    name = repo.name.replace('lovelace-', '')
                    fullname = repo.name
                    print("Generating json for repo:", name)

                    updated_at = repo.updated_at.isoformat().split('T')[0]

                    version = list(repo.get_commits())[0].sha[0:6]

                    remote_location = ORG.REUSE.format(org, fullname, name)
                    remote_location = remote_location + '.js'

                    visit_repo = ORG.VISIT.format(org, fullname)

                    changelog = ORG.VISIT.format(org, fullname)

                    data[name] = {}
                    data[name]['updated_at'] = updated_at
                    data[name]['version'] = version
                    data[name]['remote_location'] = remote_location
                    data[name]['visit_repo'] = visit_repo
                    data[name]['changelog'] = changelog
            except Exception:  # pylint: disable=W0703
                pass
        return data

    def cards_ciotlosm(self):
        """Generate json form ciotlosm."""
        ciotlosm = self.github.get_repo('ciotlosm/custom-lovelace')
        data = {}
        repos = []
        if self.repo:
            for repo in self.repo:
                repos.append(repo)
        else:
            for repo in list(ciotlosm.get_dir_contents('')):
                if repo.path not in ['LICENSE', 'README.md']:
                    repos.append(repo.path)
        for repo in repos:
            try:
                name = repo
                print("Generating json for repo:", name)

                version = ciotlosm.get_file_contents(name + '/VERSION')
                version = version.decoded_content.decode()
                version = version.split()[0]

                visit_repo = ORG.VISIT.format('ciotlosm', 'custom-lovelace')
                visit_repo = visit_repo + '/tree/master/' + name

                changelog = visit_repo + '/changelog.md'

                remote_location = "https://raw.githubusercontent.com/ciotlosm/"
                remote_location = remote_location + "custom-lovelace/master/"
                remote_location = remote_location + name + '/' + name + '.js'

                data[name] = {}
                data[name]['updated_at'] = None
                data[name]['version'] = version
                data[name]['remote_location'] = remote_location
                data[name]['visit_repo'] = visit_repo
                data[name]['changelog'] = changelog
            except Exception:  # pylint: disable=W0703
                pass
        return data

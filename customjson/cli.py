"""Enable CLI."""
import click


@click.command()
@click.option("--token", "-T", default=None, help="GitHub access_token.")
@click.option("--push", "-P", is_flag=True, help="Publish a release.")
@click.option("--mode", "-M", default=None, help="Repos.")
@click.option("--repo", "-R", default=None, help="Repos.")
@click.option("--version", "-V", is_flag=True, help="Print version.")
def cli(token, push, mode, version, repo):
    """CLI for this package."""
    if version:
        from customjson.version import __version__

        print(__version__)
    else:
        from customjson.custom import CreateJson

        create_json = CreateJson(token, push, repo)
        if mode == "card":
            create_json.card()
        elif mode == "component":
            create_json.component()
        else:
            print("--mode must be 'card' or 'component'")


cli()  # pylint: disable=E1120

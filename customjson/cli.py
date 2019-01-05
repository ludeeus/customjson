"""Enable CLI."""
import click


@click.command()
@click.option('--token', '-T', help='GitHub access_token.')
@click.option('--repo', '-R', default=None, multiple=True, help='Repo.')
@click.option('--push', '-P', is_flag=True, help="Publish a release.")
@click.option('--mode', '-M', default=None, help='Repos.')
def cli(token, repo, push, mode):
    """CLI for this package."""
    from customjson.custom import CreateJson
    create_json = CreateJson(token, repo, push)
    if mode == 'card':
        create_json.card()
    elif mode == 'component':
        create_json.component()
    else:
        print("--mode must be 'card' or 'component'")


cli()  # pylint: disable=E1120

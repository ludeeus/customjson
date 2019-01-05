"""Enable CLI."""
import click


@click.command()
@click.option('--token', '-T', help='GitHub access_token.')
@click.option('--user', '-U', default=None, help='Addon name.')
@click.option('--repo', '-R', default=None, help='Repos.')
@click.option('--repos', '-R', default=None, multiple=True, help='Repos.')
@click.option('--reuse', is_flag=True, help="")
@click.option('--json_file', is_flag=True, help="Print more stuff.")
@click.option('--push', is_flag=True, help="Publish a release.")
@click.option('--mode', '-R', default=None, help='Repos.')
def cli(token, user, repo, repos, reuse, json_file, push, mode):
    """CLI for this package."""
    from customjson.custom import CreateJson
    create_json = CreateJson(token, user, repo, repos, reuse, json_file, push)
    if mode == 'card':
        create_json.card()
    elif mode == 'component':
        create_json.component()
    else:
        print("--mode must be 'card' or 'component'")


cli()  # pylint: disable=E1120

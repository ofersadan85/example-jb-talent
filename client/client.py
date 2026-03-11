from argparse import ArgumentParser, Namespace
from pathlib import Path

import httpx
from models import User

DEFAULT_USERS_DIR = Path(__file__).parent / "users"


def fetch(args: Namespace, client: httpx.Client):
    users = User.get_multiple_from_web(ids=args.id, client=client)
    for user in users:
        print(user)
        if args.save:
            user.save_to_file(args.dir)


def create(args: Namespace, client: httpx.Client):
    if args.username is None or args.name is None or args.email is None:
        parser.print_usage()
        exit("--username, --name, --email are all required in `create` mode")
    new_user = User(
        id=None,
        username=args.username,
        name=args.name,
        email=args.email,
    ).save_to_web(client)
    print(new_user)
    if args.save:
        new_user.save_to_file(args.dir)


def load(args: Namespace, client: httpx.Client):
    if args.id is None:
        for file in args.dir.glob("*.json"):
            user = User.model_validate_json(file.read_text())
            print(user)
    else:
        for user_id in args.id:
            user = User.load_from_file(args.dir, user_id)
            print(user)


if __name__ == "__main__":
    handler_map = {
        "fetch": fetch,
        "create": create,
        "load": load,
    }

    parser = ArgumentParser()
    parser.add_argument(
        "action",
        choices=handler_map.keys(),
        help="The subcommand to run",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save users as files in default folder or in folder specified by --dir",
    )
    parser.add_argument(
        "--dir",
        type=Path,
        default=DEFAULT_USERS_DIR,
        help="Users folder path",
    )
    parser.add_argument(
        "--id",
        type=int,
        nargs="+",
        help="One or more user id numbers",
    )

    create_group = parser.add_argument_group(
        title="User create arguments",
        description="These arguments are only used by the `create` subcommand",
    )
    create_group.add_argument("--name")
    create_group.add_argument("--username")
    create_group.add_argument("--email")

    args = parser.parse_args()
    print(args)

    client = httpx.Client(base_url="https://jsonplaceholder.typicode.com/")
    args.dir.mkdir(exist_ok=True)

    handler = handler_map[args.action]
    handler(args, client)

    # Optional: add an "update" subcommand
    # Example:
    # python update --id 3 --username john
    # Load the file for user id 3, update the username on the server
    # python update --id 3 --username john --save
    # Load the file for user id 3, update the username on the server + save the result to the 3.json file

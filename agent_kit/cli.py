import argparse

from agent_kit.models.base import get_model_identifier, get_model_by_identifier
from agent_kit.interfaces.text import TextInterface
from agent_kit.tools import get_default_tools
from agent_kit.harness import Harness
from agent_kit.memory import Memory
from agent_kit.agent import Agent


def run(args):

    # setup model
    model = get_model_by_identifier(args.model_identifier)

    # setup harness
    harness = Harness()

    for tool in get_default_tools():
        harness.add_tool(tool)

    # setup memory
    memory = Memory()

    # setup interface
    interface_classes = {
        "text": TextInterface,
    }

    interface = interface_classes[args.interface]()

    # setup agent
    agent = Agent(
        harness=harness,
        model=model,
        memory=memory,
        interface=interface,
    )

    # main loop
    while True:
        try:
            agent.run()

        except (KeyboardInterrupt, EOFError):
            print()
            break


def list(args):
    for identifier in get_model_identifier():
        print(identifier)


def handle_cli():
    parser = argparse.ArgumentParser(
        prog="agent",
        description="agent-kit CLI tool",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    # subparser: run
    run_parser = subparsers.add_parser(
        "run",
        help="Run model interactively",
    )

    run_parser.add_argument(
        "model_identifier",
        type=str,
        help="Model identifier (required)"
    )

    run_parser.add_argument(
        "--interface",
        choices=["text"],
        default="text",
        help="Interface type (default: text)"
    )

    # subparser: list
    subparsers.add_parser("list", help="List available items")

    args = parser.parse_args()

    if args.command == "run":
        run(args)

    elif args.command == "list":
        list(args)

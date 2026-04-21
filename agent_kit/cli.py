import argparse
import sys
import os

from agent_kit.models.base import get_model_identifier, get_model_by_identifier
from agent_kit.interfaces.text import TextInterface
from agent_kit.tools import get_default_tools
from agent_kit.harness import Harness
from agent_kit.memory import Memory
from agent_kit.agent import Agent


def load_prompts(raw_prompts):
    prompt = ""

    for raw_prompt in raw_prompts:
        if raw_prompt.endswith(".md"):
            if not os.path.exists(raw_prompt):
                sys.exit(f"ERROR: {raw_prompt} not found")

            prompt += "\n" + open(raw_prompt, "r").read()

        else:
            prompt += "\n" + raw_prompt

    return prompt


def run(args):

    # go to app directory
    if not os.path.exists(args.app_dir):
        sys.exit(f"ERROR: {args.app_dir} not found")

    os.chdir(args.app_dir)

    # load prompts
    think = not args.disable_thinking
    system_prompt = load_prompts(args.system_prompt)
    user_prompt = load_prompts(args.user_prompt)

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

    interface = interface_classes[args.interface](
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        think=think,
    )

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

            # one-shot (`--user-prompt`)
            if user_prompt:
                break

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

    run_parser.add_argument(
        "--app-dir",
        default=os.getcwd(),
    )

    run_parser.add_argument(
        "--system-prompt",
        nargs="+",
        default=[],
    )

    run_parser.add_argument(
        "--user-prompt",
        nargs="+",
        default=[],
    )

    run_parser.add_argument(
        "--disable-thinking",
        action="store_true",
    )

    # subparser: list
    subparsers.add_parser("list", help="List available items")

    args = parser.parse_args()

    if args.command == "run":
        run(args)

    elif args.command == "list":
        list(args)

#! /usr/bin/env python

import fire

from pyvultr import VultrV2
from pyvultr.exception import PYVException
from pyvultr.utils.box import make_colorful
from pyvultr.v2 import command_wrapper

CLI_NAME = "pyvultr"


def main():
    """Vultr CLI entry point."""
    command_wrapper.is_cli = True
    try:
        fire.Fire(VultrV2, name=CLI_NAME)
    except PYVException as e:
        err = make_colorful(e.json) if e.json is not None else f"Error: {e}"
        print(err)


if __name__ == "__main__":
    main()

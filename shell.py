import argparse
import tempfile
import re
import locale
import os
import sys
from typing import Any, Optional

from asciinema import __version__, config
from asciinema.commands.auth import AuthCommand
from asciinema.commands.cat import CatCommand
from asciinema.commands.play import PlayCommand
from asciinema.commands.record import RecordCommand
from asciinema.commands.upload import UploadCommand


def valid_encoding() -> bool:
    def _locales() -> Optional[str]:
        try:
            return locale.nl_langinfo(locale.CODESET)
        except AttributeError:
            return locale.getlocale()[-1]

    loc = _locales()

    if loc is None:
        return False
    else:
        return loc.upper() in ("US-ASCII", "UTF-8", "UTF8")


def positive_int(value: str) -> int:
    _value = int(value)
    if _value <= 0:
        raise argparse.ArgumentTypeError("must be positive")

    return _value


def positive_float(value: str) -> float:
    _value = float(value)
    if _value <= 0.0:
        raise argparse.ArgumentTypeError("must be positive")

    return _value


def maybe_str(v: Any) -> Optional[str]:
    if v is not None:
        return str(v)
    return None


def execute(cmd, tmp_file) -> Any:
    if not valid_encoding():
        sys.stderr.write(
            "asciinema needs an ASCII or UTF-8 character encoding to run. "
            "Check the output of `locale` command.\n"
        )
        return 1

    try:
        cfg = config.load()
    except config.ConfigError as e:
        sys.stderr.write(f"{e}\n")
        return 1

    # create the top-level parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--version", action="version", version=f"asciinema {__version__}"
    )

    subparsers = parser.add_subparsers()

    # create the parser for the `rec` command
    parser_rec = subparsers.add_parser("rec", help="Record terminal session")
    parser_rec.add_argument(
        "--stdin",
        help="enable stdin recording, disabled by default",
        action="store_true",
        default=cfg.record_stdin,
    )
    parser_rec.add_argument(
        "--append",
        help="append to existing recording",
        action="store_true",
        default=False,
    )
    parser_rec.add_argument(
        "--raw",
        help="save only raw stdout output",
        action="store_true",
        default=False,
    )
    parser_rec.add_argument(
        "--overwrite",
        help="overwrite the file if it already exists",
        action="store_true",
        default=False,
    )
    parser_rec.add_argument(
        "-c",
        "--command",
        help="command to record, defaults to $SHELL",
        default="ls",
        # default=cfg.record_command,
    )
    parser_rec.add_argument(
        "-e",
        "--env",
        help="list of environment variables to capture, defaults to "
        + config.DEFAULT_RECORD_ENV,
        default=cfg.record_env,
    )
    parser_rec.add_argument("-t", "--title", help="title of the asciicast")
    parser_rec.add_argument(
        "-i",
        "--idle-time-limit",
        help="limit recorded idle time to given number of seconds",
        type=positive_float,
        default=maybe_str(cfg.record_idle_time_limit),
    )
    parser_rec.add_argument(
        "--cols",
        help="override terminal columns for recorded process",
        type=positive_int,
        default=None,
    )
    parser_rec.add_argument(
        "--rows",
        help="override terminal rows for recorded process",
        type=positive_int,
        default=None,
    )
    parser_rec.add_argument(
        "-y",
        "--yes",
        help='answer "yes" to all prompts (e.g. upload confirmation)',
        action="store_true",
        default=cfg.record_yes,
    )
    parser_rec.add_argument(
        "-q",
        "--quiet",
        help="be quiet, suppress all notices/warnings (implies -y)",
        action="store_true",
        default=True,
        # default=cfg.record_quiet,
    )
    parser_rec.add_argument(
        "filename",
        nargs="?",
        default="",
        help="filename/path to save the recording to",
    )
    parser_rec.set_defaults(cmd=RecordCommand)

    args = parser.parse_args(
        ["rec", "--quiet", "--overwrite", "--raw", "-c", cmd, tmp_file]
    )
    command = RecordCommand(args, cfg, os.environ)
    code = command.execute()

    return code


def run_cmd(cmd):
    exit_code_file = tempfile.NamedTemporaryFile(suffix=".exit_code", delete=False)
    cmd += "\necho $? > %s" % exit_code_file.name
    t = tempfile.NamedTemporaryFile(suffix=".cast", delete=False)
    execute(cmd, t.name)

    with open(t.name, "r") as f:
        out = f.read()
    os.unlink(t.name)

    with open(exit_code_file.name, "r") as f:
        exit_code = f.read()
    if exit_code == '':
        exit_code = 1
    else:
        exit_code = int(exit_code.strip())

    os.unlink(exit_code_file.name)

    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    out = ansi_escape.sub("", out.strip())
    return exit_code, out

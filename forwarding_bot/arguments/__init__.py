"""Cli argument parsing module which is used by the DatConfig class"""
from ._parser import ArgParser
from .models import ArgsModel

args_parsed = False

if not args_parsed:
    arg_parser = ArgParser()
    args = arg_parser.get_args()

    args_parsed = True

# -*- coding: utf-8 -*- vim:fenc=utf-8:ft=python:et:sw=4:ts=4:sts=4
"""Desktop file tokenizer."""

import types
import wor.tokenizer as tok
import re

# What is needed to use tok.Token from Symbol

SYMBOL_CLASS_NAMES = [
"Encoding",
"X-MultipleArgs",
"Type",
"Version",
"Name",
"GenericName",
"Comment",
"Icon",
"Hidden",
"OnlyShowIn",
"NotShowIn",
"TryExec",
"Exec",
"Path",
"Terminal",
"Actions",
"MimeType",
"Categories",
"Keywords",
"StartupNotify",
"StartupWMClass",
"URL",
]

class Symbol(tok.Token):
    def __init__(self, value=None, pos=None, subvalues=[]):
        super().__init__(pos, value, subvalues)

class GroupHeader(Symbol):
    """Token class for desktop entry file group headers."""
    pass


def init_tokenizer():
    """Initializes desktop file tokenizer and returns it.
    """
    # Create Symbols
    symbol_classes = {}
    for symbol_class_name in SYMBOL_CLASS_NAMES:
        symbol_classes[symbol_class_name] = types.new_class(symbol_class_name, (Symbol,))

    # Create symbol table
    symbol_table = tok.TokenTable("Main")
    symbol_table.default_token_class = Symbol

    # Add symbols to the symbol table
    # The symbol regexp are interpreted as multiline regex when tokenizer joins
    # them.
    ns = symbol_table.add_new_token
    for symbol_name in SYMBOL_CLASS_NAMES:
        ns(symbol_name.upper().replace('-','_'), r"^" + symbol_name + r"(\[.+\])?=(.*)$\n?", token_subclass=symbol_classes[symbol_name])

    ns("EMPTY_LINE", r"^\s*\n", token_subclass=Symbol)
    ns("GROUP_HEADER", r"^\[(.+)\]\s*$\n?", token_subclass=GroupHeader)

    # Create tokenizer with defined symbol table
    try:
        inited_tokenizer = tok.Tokenizer(symbol_table)
    except tok.TokenizerRegexpError as e:
        raise e

    return inited_tokenizer

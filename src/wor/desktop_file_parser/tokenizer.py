# -*- coding: utf-8 -*- vim:fenc=utf-8:ft=python:et:sw=4:ts=4:sts=4
"""Desktop file tokenizer."""

import wor.tokenizer as tok

# What is needed to use tok.Token from Symbol

SYMBOL_CLASS_NAMES = [
"Encoding",
"X-MultipleArgs",
"Type",
"Version",
"Name",
"GenericName",
"NoDisplay",
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

#
# Token classes
#

class GroupHeader_T(tok.Token):
    """Token class for desktop entry file group headers."""
    pass

class EmptyLine_T(tok.Token):
    pass

class CommentLine_T(tok.Token):
    pass

class Entry_T(tok.Token):
    pass


def init_tokenizer(ignore_nonspec_keys=False):
    """Initializes desktop file tokenizer and returns it.

    Returns:
        wor.tokenizer.Tokenizer. Initialized instance of Tokenizer class.
    """
    # Create symbol table
    symbol_table = tok.TokenTable("Main")
    symbol_table.default_token_class = tok.Token

    # Add symbols to the symbol table
    # The symbol regexp are interpreted as multiline regex when tokenizer joins
    # them.
    ns = symbol_table.add_new_token
    for symbol_name in SYMBOL_CLASS_NAMES:
        ns(symbol_name.upper().replace('-','_'), r"^(" + symbol_name + r")(\[.+\])?=(.*)$\n?", token_subclass=Entry_T)

    # Ignore or add non-spec tokens
    if ignore_nonspec_keys:
        ns("IGNORED", r"^(.*)(\[.+\])?=(.*)$\n?", ignore=True, token_subclass=Entry_T)
    else:
        ns("NONSPEC", r"^(.*)(\[.+\])?=(.*)$\n?", ignore=False, token_subclass=Entry_T)

    ns("COMMENT_LINE", r"^#(.*)\n", token_subclass=CommentLine_T)
    ns("EMPTY_LINE", r"^[ \t\r\f\v]*\n", token_subclass=EmptyLine_T)
    ns("GROUP_HEADER", r"^\[(.+)\]\s*$\n?", token_subclass=GroupHeader_T)

    # Create tokenizer with defined symbol table
    try:
        inited_tokenizer = tok.Tokenizer(symbol_table)
    except tok.TokenizerRegexpError as e:
        raise e

    return inited_tokenizer

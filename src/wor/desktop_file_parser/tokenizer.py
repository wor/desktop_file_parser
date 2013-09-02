# -*- coding: utf-8 -*- vim:fenc=utf-8:ft=python:et:sw=4:ts=4:sts=4
"""Desktop file tokenizer."""

import re
from collections import OrderedDict


def tok_gen(text):
    """Simplified token generator.

    As Desktop files are not really that complex to tokenize, this function
    replaces the tokenizer dependency.
    Parameters:
        text: str. Desktop file as string.

    Returns:
        (str,()).
    """
    reg = r"""(?P<ENTRY>^(.+?)(\[.+?\])?=(.*)$\n?)|(?P<COMMENT_LINE>^#(.*)\n)|(?P<EMPTY_LINE>^[ \t\r\f\v]*\n)|(?P<GROUP_HEADER>^\[(.+?)\]\s*$\n?)"""
    r = re.compile(reg, re.MULTILINE)

    tok_gen.groups = OrderedDict(sorted(r.groupindex.items(), key=lambda t: t[1]))

    # Make tok_gen.groups contain mapping from regex group name to submatch
    # range. Submatch range start-1 is the whole match.
    last_i = None
    for i in tok_gen.groups.items():
        if last_i == None:
            last_i = i
            continue
        tok_gen.groups[last_i[0]] = (last_i[1], i[1]-1)
        last_i = i
    tok_gen.groups[last_i[0]] = (last_i[1], r.groups)

    pos = 0
    while True:
        m = r.match(text, pos)
        if not m:
            if pos != len(text):
                raise SyntaxError("Tokenization failed!")
            break
        pos = m.end()
        yield m.lastgroup, m.groups()[ tok_gen.groups[m.lastgroup][0]:
                tok_gen.groups[m.lastgroup][1]]

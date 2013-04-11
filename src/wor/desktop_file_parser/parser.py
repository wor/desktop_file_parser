# -*- coding: utf-8 -*- vim:fenc=utf-8:ft=python:et:sw=4:ts=4:sts=4
"""Desktop file parser."""

from .tokenizer import init_tokenizer


class DesktopEntry(object):
    def __init__(self):
        pass


def desktop_file_parser(input_stream):
    tknzr = init_tokenizer()
    input_text = input_stream.read()
    tokens = tknzr.get_tokens_gen(input_text, yield_eop=False)

    # Refine symbol stream.
    try:
        for t in tokens:
            print("Token str:", str(t))
    except tok.TokenizerException as e:
        print("Tokenization failed:")
        print(e)
        return False
    return True

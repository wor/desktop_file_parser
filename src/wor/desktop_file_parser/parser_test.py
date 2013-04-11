# -*- coding: utf-8 -*- vim:fenc=utf-8:ft=python:et:sw=4:ts=4:sts=4
"""Tests (nose)."""

import io

def test_desktop_file_parser1():
    """
    """
    from .parser import desktop_file_parser
    desktop_file_content = """
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Name=gVim ro
Name[eo]=VIM-fasado
Name[sv]=gVim
Name[xx]=xx
Comment=GTK2 enhanced vim text editor
Comment[bg]=Текст Редактор
Comment[zh_TW]=文字編輯器
GenericName=Text Editor
Type=Application
TryExec=gvim
Exec=gvim -Z -R -n -c ":set guioptions=aegiLt" -c ":set nonumber" -c ":redraw" %u
Icon=gvim
Terminal=false
X-MultipleArgs=false
Categories=GTK;Application;Utility;TextEditor;
MimeType=application/mathml+xml;application/xhtml+xml;application/x-perl;application/x-python;application/x-shellscript;audio/x-mpegurl;audio/x-scpls;image/svg+xml;message/news;message/rfc822;text/calendar;text/css;text/english;text/html;text/mrml;text/plain;text/rdf;text/rss;text/rtf;text/sgml;text/vnd.wap.wml;text/x-adasrc;text/x-bibtex;text/x-chdr;text/x-c++hdr;text/x-csrc;text/x-c++src;text/x-c;text/x-objc;text/x-csv;text/x-diff;text/x-java;text/x-katefilelist;text/x-latex;text/x-log;text/x-lyx;text/x-makefile;text/xmcd;text/xml;text/x-moc;text/x-mswinurl;text/x-objcsrc;text/x-pascal;text/x-perl;text/x-php;text/x-php-source;text/x-python;text/x-tcl;text/x-tex;text/x-vcalendar;text/x-vcard;text/x-xslfo;text/x-xslt;
"""
    df = io.StringIO(desktop_file_content)
    assert desktop_file_parser(df)

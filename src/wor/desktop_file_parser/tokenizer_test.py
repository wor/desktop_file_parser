# -*- coding: utf-8 -*- vim:fenc=utf-8:ft=python:et:sw=4:ts=4:sts=4
"""Tests (nose) for helper_iterate_tokens/tokenizer.py module."""

import io

def helper_iterate_tokens(input_stream):
    from .tokenizer import tok_gen

    input_text = input_stream.read()
    tokens = tok_gen(input_text)

    for t in tokens:
        pass
    return True

# =========================================

def test_desktop_file_tokenizer1():
    """
    """
    desktop_file_content = """
[Desktop Entry]
Name=qiv
Comment=a fast gdk/imlib image viewer for X
Exec=qiv -R -u -t %F
Terminal=false
Type=Application
Categories=Viewer;Utility;
MimeType=image/jpeg;image/png;
StartupNotify=false
"""
    df = io.StringIO(desktop_file_content)
    assert helper_iterate_tokens(df)

def test_desktop_file_tokenizer2():
    """
    """
    desktop_file_content = """[Desktop Entry]
Name=qiv
Comment=a fast gdk/imlib image viewer for X
Exec=qiv -R -u -t %F
Terminal=false
Type=Application
Categories=Viewer;Utility;
MimeType=image/jpeg;image/png;
StartupNotify=false"""
    df = io.StringIO(desktop_file_content)
    assert helper_iterate_tokens(df)

def test_desktop_file_tokenizer3():
    """
    """
    desktop_file_content = """
[Desktop Entry]
Encoding=UTF-8
Version=1.0
Name=gVim ro
Name[eo]=VIM-fasado
Name[sv]=gVim
Name[xx]=xx
Comment=GTK2 enhanced vim text editor
Comment[ar]=محرر نصوص
Comment[bg]=Текст Редактор
Comment[de]=Texteditor
Comment[el]=Διορθωτής Κειμένου
Comment[eo]=Tekstredaktilo
Comment[et]=Tekstiredaktor
Comment[eu]=Testu Editorea
Comment[fi]=Tekstieditori
Comment[he]=עורך טקסט
Comment[is]=Textaritill
Comment[ja]=テキストエディタ
Comment[lt]=Teksto redaktorius
Comment[mt]=Editur tat-test
Comment[pt_BR]=Editor de Texto
Comment[ro]=Editor de text
Comment[ru]=редактор
Comment[sk]=Textový editor
Comment[sl]=Urejevalnik besedil
Comment[ta]=¯¨Ã ¦¾¡ÌôÀ¡Ç÷
Comment[tr]=Metin Düzenleyici
Comment[uk]=Редактор текстів
Comment[vi]=Trình soạn văn bản
Comment[xx]=xx
Comment[zh_CN]=文本编辑器
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
    assert helper_iterate_tokens(df)

def test_desktop_file_tokenizer4():
    """
    """
    desktop_file_content = """# comment 1
[Desktop Entry]
Name=qiv
Comment=a fast gdk/imlib image viewer for X
Exec=qiv -R -u -t %F
# comment 2
Terminal=false
# comment 3

Type=Application
#
# comment 4
#
Categories=Viewer;Utility;

# comment 5

MimeType=image/jpeg;image/png;

# comment 6
StartupNotify=false
"""
    df = io.StringIO(desktop_file_content)
    assert helper_iterate_tokens(df)

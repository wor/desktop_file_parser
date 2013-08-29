# -*- coding: utf-8 -*- vim:fenc=utf-8:ft=python:et:sw=4:ts=4:sts=4
"""Desktop file parser.
TODO: rename get_entry_key_from_group
"""

import wor.tokenizer as tok
from .tokenizer import init_tokenizer


class DesktopFile(object):
    """Desktop file."""
    def __init__(self, entry_groups={}, file_name=""):
        self.entry_groups = entry_groups
        self.file_name = file_name
    def __str__(self):
        df_str = ""
        for g in self.entry_groups:
            df_str += "[{}]\n".format(g)
            for e in self.entry_groups[g]:
                df_str += str(e) + "\n"
        return df_str
    def setup_with(self, key_value_pairs=[]):
        """Simple and limited initialization of a empty desktop file.

        Initializes a desktop file with given key_value_pairs as entries in the
        "Desktop Entry" group. Doesn't support entry locale and if not given
        defaults to following values:
            Encoding=UTF-8
            Type=Application
            Name=Unkown Application
            Exec=echo %f

        If Desktop files "Desktop Entry" group is not empty then this doesn't do
        anything.

        Parameters:
            key_value_pairs: [(str, str)]. List of key value tuples.
        """
        if self.entry_groups["Desktop Entry"]:
            return

        # Ok, this could be cleaner :)
        encoding_added = False
        type_added = False
        name_added = False
        exec_added = False
        for kvp in key_value_pairs:
            if kvp[0] == "Encoding":
                encoding_added = True
            elif kvp[0] == "Type":
                type_added = True
            elif kvp[0] == "Name":
                name_added = True
            elif kvp[0] == "Exec":
                exec_added = True
            self.entry_groups["Desktop Entry"].append(Entry(kvp[0], kvp[1], None))
        if not encoding_added:
            self.entry_groups["Desktop Entry"].append(Entry("Encoding", "UTF-8", None))
        if not type_added:
            self.entry_groups["Desktop Entry"].append(Entry("Type", "Application", None))
        if not name_added:
            self.entry_groups["Desktop Entry"].append(Entry("Name", "Unkown Application", None))
        if not exec_added:
            self.entry_groups["Desktop Entry"].append(Entry("Exec", "echo %f", None))
    def get_entry_key_from_group(self, entry_key, group="Desktop Entry"):
        """Returns entry with given key from specified group.

        Returns:
            Entry. Entry which .key == entry_key or None if not found.
        """
        for e in self.entry_groups[group]:
            if e.key == entry_key:
                return e
        return None
    def get_entry_value_from_group(self, entry_key, group="Desktop Entry"):
        """Returns entries value with given key from specified group.

        Returns:
            str|bool|[str]. Entry.value which Entry.key == entry_key or None if
                not found.
        """
        e = self.get_entry_key_from_group(entry_key, group=group)
        if e:
            return e.value
        return None
    def check(self):
        """Checks if Desktop file is valid according to the specification.

        Returns (bool, str). If file is valid then returns (True, ""), else
            returns False coupled with string explaining what whas wrong.
        """
        if not "Desktop Entry" in self.entry_groups:
            return (False, "Group 'Desktop Entry' is missing.")

        if not self.get_entry_key_from_group(entry_key="Name"):
            return (False, "Entry 'Name' is missing.")

        if not self.get_entry_key_from_group(entry_key="Exec"):
            return (False, "Entry 'Exec' is missing.")

        t = self.get_entry_key_from_group(entry_key="Type")
        if not t:
            return (False, "Entry 'Type' is missing.")

        if t.value == "Link":
            if not self.get_entry_key_from_group(entry_key="URL"):
                return (False, "Entry 'URL' is missing, required for desktop file of type 'Link'.")
        return (True, "")


class Entry(object):
    """Desktop files entry."""
    def __init__(self, key, value, locale):
        self.key = key
        self.value = value
        self.locale = locale
    def __str__(self):
        if isinstance(self.value, bool):
            value = "true" if self.value else "false"
        elif isinstance(self.value, list):
            value = ";".join(self.value)
        else:
            value = self.value
        if self.locale is not None:
            return "{key}[{locale}]={_value}".format(_value=value, **self.__dict__)
        else:
            return "{key}={_value}".format(_value=value, **self.__dict__)


def parse(input_stream):
    """Parses desktop entry file.

    Args:
        input_stream:   file. Desktop file content as readable stream.

    Returns:
        DesktopFile. Instance of DesktopFile class which represents the parsed desktop file.

    Raises:
        wor.tokenizer.TokenizerException. If the tokenization of input stream fails.
        ParsingError. If parsing of the desktop file fails.
    """
    tknzr = init_tokenizer()
    input_text = input_stream.read()
    tokens = tknzr.get_tokens_gen(input_text, yield_eop=False)

    # Desktop files entry groups
    entry_groups = {}

    # Refine symbol stream.
    try:
        current_group = None
        for t in tokens:
            if t.basename == "EmptyLine_T":
                continue
            elif t.basename == "CommentLine_T":
                # TODO: don't throw away!
                continue
            elif t.basename == "GroupHeader_T":
                current_group = t.subvalues[0]
                entry_groups[current_group] = []
                continue
            elif t.basename == "Entry_T":
                entry_name = t.subvalues[0]
                if len(t.subvalues) >= 3:
                    entry_value = t.subvalues[2]
                    entry_locale = t.subvalues[1].strip("[]")
                else:
                    entry_value = t.subvalues[1]
                    entry_locale = None
                entry = Entry(entry_name, entry_value, entry_locale)

                # Check boolean entries
                if entry.key in ["NoDisplay", "Hidden", "Terminal", "StartupNotify", "X-MultipleArgs"]:
                    if not entry.value in ["0", "1", "false", "true"]:
                        print("ERROR: '{}' key did not have boolean value!".format(entry.key))
                    elif entry.value in ["0", "false"]:
                        entry.value = False
                    elif entry.value == ["1", "true"]:
                        entry.value = True
                # Check multiple string entries (string lists)
                elif entry.key in ["OnlyShowIn", "NotShowIn", "Actions", "MimeType", "Categories", "Keywords"]:
                    # TODO: ";" can be escaped with '\' which can of course(?)
                    # be also escaped so splitting should only be done if ';' is
                    # not prefixed with any number of '\' chars or prefixed with
                    # mod 2 number of '\' chars. So <count of '\'> % 2 == 0 ==>
                    # split.
                    entry.value = entry.value.split(";")

                entry_groups[current_group].append(entry)
            else:
                print("ERROR:", t.__class__.__base__.__name__, t.__class__.__name__)
                assert(False)
    except tok.TokenizerException as e:
        raise e

    # Read orginal filename for the desktop file object from the input_stream
    file_name = input_stream.name if hasattr(input_stream, "name") else ""

    df = DesktopFile(entry_groups, file_name=file_name)

    #print("==========DEBUG=========")
    #print(df)
    #ok, error = df.check()
    #if not ok:
    #    print(error)
    #print("==========DEBUG=========")

    return df

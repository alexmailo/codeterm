#!/usr/bin/python3

import re

import json
import sys
from yamltheme import apply
def has(obj, prop):
    return prop in obj

def clean_json(json_path):

    data = open(json_path, "r").read()

    ta = re.compile(r',\s*]')
    td = re.compile(r',\s*}')
    sc = re.compile(r'\/\/.*')
    mc = re.compile(r'\/\*([\s\S]*?)\*\/')
    sm = re.compile(r'"\$?schema.*')

    data = sc.sub("", data)
    data = mc.sub("", data)
    data = sm.sub('', data)
    data = ta.sub("]", data)
    data = td.sub("}", data)

    return json.loads(data)

def apply_colorscheme(theme_path):




    data = clean_json(theme_path)
    colors = {"primary": {}, "normal": {}, "bright": {}}

    if not has(data, "colors"):
        return

    c = data["colors"]
    colors["primary"]["foreground"] = c.get("terminal.foreground", c.get(
        "editor.foreground", c.get("foreground", "#ffffff")))
    colors["primary"]["background"] = c.get("terminal.background", c.get(
        "editor.background", c.get("background", "#000000")))

    for key in c:
        tmp_key = key
        if "terminal" in key:
            if "Bright" in key:
                tmp_key = tmp_key.replace('terminal.ansiBright', '')
                tmp_key = tmp_key.lower()
                colors["bright"][tmp_key] = c[key]
            elif "cursor" in key or "selection" in key:
                pass
            else:
                if not "foreground" in key and not "background" in key:
                    tmp_key = tmp_key.replace('terminal.ansi', '')
                    tmp_key = tmp_key.lower()
                    colors["normal"][tmp_key] = c[key]
    apply({"colors": colors})

    
if __name__ == '__main__':
    
    if len(sys.argv) < 2:
        print("usage: cli.py <yamlfile>")
        sys.exit(1)
    apply_colorscheme(sys.argv[1])
    print(sys.argv[1])

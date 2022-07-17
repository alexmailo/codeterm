#!/usr/bin/python3
import subprocess
import os
import re
from os.path import expanduser, join
import json
import yaml
import simple_term_menu

HOME = expanduser("~")
themes = subprocess.check_output(
    ["code", "--list-extensions", "--category", "themes"]).decode().splitlines()

VS_CODE_EXTENSIONS_PATH = join(HOME, ".vscode", "extensions")
ALL_EXTENSIONS = os.listdir(VS_CODE_EXTENSIONS_PATH)


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


def create_colorscheme(theme_path, yaml_output):
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
    yaml.dump({"colors": colors},  open(
        yaml_output, "w"), default_flow_style=False)


def get_json_files():
    all_extension_themes = []
    json_files = []
    for ext in ALL_EXTENSIONS:
        for theme in themes:
            if theme.lower() in ext:
                all_extension_themes.append(join(VS_CODE_EXTENSIONS_PATH, ext))

    for entry in all_extension_themes:
        if not has(os.listdir(entry), 'package.json'):
            continue
        package = json.load(open(join(entry, "package.json"), "r"))
        if not has(package, "categories") or not has(package, "contributes"):
            continue

        if not has(package["categories"], "Themes") or not has(package["contributes"], "themes"):
            continue

        for theme in package['contributes']['themes']:
            theme_path = join(entry, theme['path'][2:])

            label = theme['label']
            if 'Visual Studio' in label:
                continue
            label = label.replace(' ', '_')
            json_files.append((label, theme_path))
    return json_files


def create_all_yaml_themes(json_files):

    # CREATES A WHOLE LOT OF YAML THEMES
    for label, json_path in json_files:
        create_colorscheme(json_path, f'{label}.yaml')


def list(json_files):

    names = [f'{label}|{path}' for label, path in json_files]

    terminal_menu = simple_term_menu.TerminalMenu(names, menu_cursor_style=('fg_green', 'bold'), preview_command="/home/alex/Tmp/cli.py {}", preview_size=0.75, preview_title="Theme Path")
    terminal_menu.show()

    # print(choice)
json_files = get_json_files()
list(json_files)

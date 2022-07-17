import sys
import yaml


def apply(yaml_theme):
    from os.path import expanduser, join
    home = expanduser("~")
    alacritty_path = join(home, '.config', 'alacritty','alacritty.yml')
    alacritty_dict = yaml.safe_load(open(alacritty_path, 'r').read())

    alacritty_dict['colors'] = yaml_theme['colors']
    yaml.dump(alacritty_dict,  open(alacritty_path, 'w'), default_flow_style=False)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: applyYaml.py <yamlfile>")
        sys.exit(1)


    yaml_file = sys.argv[1]
    theme = yaml.safe_load(open(yaml_file, 'r').read())

    apply(theme)
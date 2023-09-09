#!/usr/bin/env python3

import argparse
import markdown
import yaml
import random
import os

from slugify import slugify
from pathlib import Path
from pygments.formatters import HtmlFormatter
from genanki import Package, Model, Note, Deck

# Constants for default values
PYGMENT_STYLE = "default"
CARD_TEMPLATES = [
    {
        "model_id": 1559383000,
        "name": "Basic (genanki)",
        "fields": [
            {"name": "Topic", "font": "Arial"},
            {"name": "Front", "font": "Arial"},
            {"name": "Back", "font": "Arial"},
            {"name": "Source", "font": "Arial"},
        ],
        "templates": [
            {
                "name": "Card 1",
                "qfmt": "<h2>{{Topic}}</h2>{{Front}}",
                "afmt": "{{FrontSide}}<hr id=answer>{{Back}}<p><a href='{{Source}}'>Resource</a></p>",
            }
        ],
        "css": ".card {font-family: arial; font-size: 20px; color: black; background-color: white;} .card table, th, td {border: 1px solid black; border-collapse: collapse;}",
    },
    {
        "model_id": 1305534440,
        "name": "Basic (type in the answer) (genanki)",
        "fields": [
            {"name": "Topic", "font": "Arial"},
            {"name": "Front", "font": "Arial"},
            {"name": "Back", "font": "Arial"},
            {"name": "Source", "font": "Arial"},
        ],
        "templates": [
            {
                "name": "Card 1",
                "qfmt": "<h2>{{Topic}}</h2>{{Front}}{{type:Back}}",
                "afmt": "<h2>{{Topic}}</h2>{{Front}}<hr id=answer>{{type:Back}}<p><a href='{{Source}}'>Resource</a></p>",
            }
        ],
        "css": ".card {font-family: arial; font-size: 20px; color: black; background-color: white;} .card table, th, td {border: 1px solid black; border-collapse: collapse;}",
    },
    {
        "model_id": 1550428389,
        "name": "Cloze (genanki)",
        "fields": [
            {"name": "Topic", "font": "Arial"},
            {"name": "Text", "font": "Arial"},
            {"name": "Extra", "font": "Arial"},
            {"name": "Source", "font": "Arial"},
        ],
        "templates": [
            {
                "name": "Cloze",
                "qfmt": "<h2>{{Topic}}</h2>{{cloze:Text}}",
                "afmt": "<h2>{{Topic}}</h2>{{cloze:Text}}<hr>{{Extra}}<p><a href='{{Source}}'>Resource</a></p>",
            }
        ],
        "css": ".card {font-family: arial; font-size: 20px; color: black; background-color: white;} .cloze {font-weight: bold; color: blue;} .card table, th, td {border: 1px solid black; border-collapse: collapse;}",
    },
]

def load_templates():
    """
    Load Anki card templates from a dictionary and add CSS styles for code highlighting.

    Returns:
        list: List of Anki card templates.
    """

    f = HtmlFormatter(style=PYGMENT_STYLE, full=True, cssclass="codehilite")
    c = f.get_style_defs()
    return [
        Model(
            model_id=x["model_id"],
            name=x["name"],
            fields=x["fields"],
            templates=x["templates"],
            css=x["css"] + c
        )
        for x in CARD_TEMPLATES
    ]

def process_yaml_file(file_path, models):
    """
    Process a YAML file and create an Anki deck from its contents.

    Args:
        file_path (str): The path to the YAML file.
        models (dict): A dictionary mapping card names to Anki card templates.

    Returns:
        Deck: Anki deck created from the YAML file.
    """
    try:
        d = yaml.safe_load(open(file_path, 'r'))

        deck = Deck(
            name=d['metadata']['name'],
            deck_id=d['id'],
            description=d['metadata']['description']
        )

        exts = ['extra', "codehilite"]

        for e in d['cards']:
            s = models.get(e.get('card'))
            sp = e.get('spec')
            f = markdown.markdown(sp.get('front'), extensions=exts)
            b = markdown.markdown(sp.get('back'), extensions=exts)

            deck.add_note(Note(
                model=s, 
                fields=[e.get('metadata').get('title'), f, b, e.get('metadata').get('resource')],
                tags=e.get('metadata').get('tags'),
            ))

        return deck
    except Exception as ex:
        print(f"Error processing {file_path}: {ex}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Anki decks from YAML files or directories")
    parser.add_argument('paths', nargs='+', help='YAML files or directories containing YAML files')
    args = parser.parse_args()

    templates = load_templates()

    models = {
        'Basic': templates[0],
        'Prompt': templates[1],
        'Cloze': templates[2],
    }

    for path in args.paths:
        path_obj = Path(path)

        if path_obj.is_dir():
            yaml_files = path_obj.glob('*.yml')
        elif path_obj.is_file() and path_obj.suffix == '.yml':
            yaml_files = [path_obj]
        else:
            print(f"Invalid file or directory path: {path}")
            continue

        for yaml_file in yaml_files:
            deck = process_yaml_file(yaml_file, models)
            if deck:
                n = slugify(deck.name)
                deck_filename = f'{n}.apkg'
                deck.write_to_file(deck_filename)
                print(f"Deck '{deck.name}' written to {deck_filename}")

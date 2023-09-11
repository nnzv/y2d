#!/usr/bin/env python3

# Copyright 2023 Enzo Venturi. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import argparse
import markdown
import yaml
import os
import logging
from importlib.metadata import metadata

from typing import List, Optional
from slugify import slugify
from pathlib import Path
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
from genanki import Package, Model, Note, Deck

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

class AnkiDeckGenerator:

    COMMON_CSS = (
        ".card {font-family: arial; font-size: 20px; color: black; background-color: white;}"
        ".card table, th, td {border: 1px solid black; border-collapse: collapse;}"
    )

    def __init__(self):
        self.cli_args = None
        self.CARD_TEMPLATES = [
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
                "css": self.COMMON_CSS
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
                "css": self.COMMON_CSS
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
                "css": self.COMMON_CSS + (
                    " .cloze {font-weight: bold; color: blue;}"
                ),
            },
        ]

    def load_templates(self) -> List[Model]:
        """
        Load Anki card templates from a list of dictionaries.

        Returns:
            list: List of Anki card models.
        """
        logging.info("Loading Anki card templates")

        # Initialize the CSS to append with an empty string by default
        c = ""

        if "codehilite" in self.cli_args.md_exts:
            try:
                style = self.cli_args.pygment_style
                fmt = HtmlFormatter(style=style, full=True, cssclass="codehilite")
            except ClassNotFound as ex:
                logger.warning(f"Pygments style '{style}' not found. Using the default style.")
                fmt = HtmlFormatter(style="default", full=True, cssclass="codehilite")

            # Assign the Pygments style if code highlighting is enabled
            c = fmt.get_style_defs()

        return [
            Model(
                model_id=x["model_id"],
                name=x["name"],
                fields=x["fields"],
                templates=x["templates"],
                css=x["css"] + c
            )
            for x in self.CARD_TEMPLATES
        ]

    def process_yaml_file(self, file_path: str, models: dict) -> Optional[Deck]:
        """
        Process a YAML file and create an Anki deck from its contents.

        Args:
            file_path (str): The path to the YAML file.
            models (dict): A dictionary mapping card names to Anki card templates.

        Returns:
            Deck: Anki deck created from the YAML file.
        """
        logging.info(f"Processing YAML file: {file_path}")

        try:
            with open(file_path, 'r') as file:
                d = yaml.safe_load(file)

                deck = Deck(
                    name=d['metadata']['name'],
                    deck_id=d['id'],
                    description=d['metadata']['description']
                )

                for e in d['cards']:
                    s = models.get(e.get('card'))
                    sp = e.get('spec')
                    f = markdown.markdown(sp.get('front'), extensions=self.cli_args.md_exts)
                    b = markdown.markdown(sp.get('back'), extensions=self.cli_args.md_exts)

                    deck.add_note(Note(
                        model=s, 
                        fields=[e.get('metadata').get('title'), f, b, e.get('metadata').get('resource')],
                        tags=e.get('metadata').get('tags'),
                    ))
                return deck
        except yaml.YAMLError as yaml_error:
            logger.warning(f"YAML error in {file_path}: {yaml_error}")
        except Exception as ex:
            logger.warning(f"Error processing {file_path}: {ex}")

        return None

    def generate_decks(self, paths: List[str]) -> None:
        """
        Generate Anki decks from YAML files or directories.

        Args:
            paths (list): List of YAML files or directories containing YAML files.
        """
        logging.info("Generating Anki decks")

        templates = self.load_templates()

        models = {
            'Basic': templates[0],
            'Prompt': templates[1],
            'Cloze': templates[2],
        }

        for path in paths:
            self.process_path(path, models)

    def process_path(self, path: str, models: dict) -> None:
        """
        Process a directory or file path.

        Args:
            path (str): The directory or file path.
            models (dict): A dictionary mapping card names to Anki card templates.
        """

        path_obj = Path(path)

        if not path_obj.exists():
            logger.warning(f"Path does not exist: {path}")
            return

        if path_obj.is_dir():
            yaml_files = list(path_obj.glob('*.yaml'))
        elif path_obj.is_file() and path_obj.suffix == '.yaml':
            yaml_files = [path_obj]
        else:
            logger.warning(f"Invalid file or directory path: {path}")
            return

        for yaml_file in yaml_files:
            deck = self.process_yaml_file(yaml_file, models)
            if deck:
                self.save_deck(deck)

    def save_deck(self, deck: Deck) -> None:
        """
        Save an Anki deck to apkg file.

        Args:
            deck (Deck): Anki deck to be saved.
        """
        logging.info(f"Saving Anki deck: {deck.name}")

        try:
            if deck:
                slug = slugify(deck.name)
                apkg = Path(f'{slug}.apkg')
                while apkg.exists() and not self.cli_args.force:
                    u = input(f"File '{apkg}' already exists. Overwrite? (y/n): ").strip().lower()
                    if u == 'y':
                        break
                    elif u == 'n':
                        logger.warning(f"Deck '{deck.name}' not saved.")
                        return
                    else:
                        print(f"Invalid input '{u}'. Please enter 'y' for yes or 'n' for no.")
                deck.write_to_file(apkg)
                logger.info(f"Deck '{deck.name}' written to {apkg}")
        except Exception as ex:
            logger.warning(f"Error saving deck: {ex}")

def main() -> None:
    m = metadata('y2d')
    p = argparse.ArgumentParser(prog=m['name'], description=m['description'])
    p.add_argument('paths', nargs='+', help="YAML files or directories containing YAML files")
    p.add_argument('--md-exts', nargs='+', default=["extra", "codehilite"], help='list of Markdown extensions to enable')
    p.add_argument('--pygment-style', default='default', help='style of Pygments formatter')
    p.add_argument('--version', action='version', version=f'%(prog)s {m["version"]}')
    p.add_argument('--force', action='store_true', help='overwrite existing files without prompting')

    a = p.parse_args()

    d = AnkiDeckGenerator()
    d.cli_args = a
    d.generate_decks(a.paths)

if __name__ == '__main__':
    main()

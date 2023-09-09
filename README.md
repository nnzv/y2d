<!-- Copyright 2023 Enzo Venturi. All rights reserved. -->
<!-- Use of this source code is governed by a BSD-style -->
<!-- license that can be found in the LICENSE file. -->

# Effortless Anki Flashcard Creation

Creating Anki flashcards can be simple and efficient with this approach.

## Key Features

* **YAML Deck Setup**: Define decks using YAML code.
* **Markdown Formatting**: Format 'back' and 'front' fields with Markdown.
* **Custom Titles and Descriptions**: Personalize each deck with titles and descriptions.
* **Code Highlighting**: Highlight code using Markdown extensions.
* **Three Card Types**: Create Basic, Cloze, and Prompt cards.
    1. Basic: Both front and back flashcards.
    2. Cloze: Supports Cloze deletion notation.
    3. Prompt: Engage users by prompting them for answers.
* **Tagging**: Efficiently organize cards with tags.

## Requirements

* Python 3

## Demonstration

1. Set Up a Virtual Environment
   ```sh
   % python3 -m venv venv
   ```

2. Activate the Environment
   ```sh
   % source venv/bin/activate
   ```

3. Install Dependencies
   ```sh
   % python3 -r requirements.txt
   ```

4. Test the Workflow
   ```sh
   % python3 cli.py dev-lang
   ```

When you provide a directory as an argument to the 'cli.py' script, each .yml file in that directory becomes a deck in `.apkg` file format. While adding support for `.yaml` extensions is 
possible, it's not a priority. This project is open source, so _feel free to fork and customize it_!

To create a standalone deck:
```sh
% python3 cli.py dev-lang/go.yml
```

For a combination of complex decks:
```sh
% python3 cli.py dev-lang/go.yml another-directory/card.yml
```

## Flashcard Structure

To create a flashcard, follow this YAML structure:

```yaml
id: 637500
metadata:
  name: "Get started with Go"
  description: |
    A brief introduction to Go programming.
cards:
  - card: Basic
    metadata:
      title: Write some code
      resource: https://go.dev/doc/tutorial/getting-started#code
      tags: []
    spec:
      front: |
        Steps to create a "hello world" Go program?
      back: |
        Create a directory, navigate to it, and initialize a Go module using

        `go mod init example/hello`
```

Here's what each part does:

- `id`: This is a unique identifier for your deck.
- `metadata`:
  - `name`: Specify the title or name of your deck.
  - `description`: Add a short and concise description of your deck.
- `cards`: This section contains an array of individual flashcard entries.
  - `card`: Choose the type of flashcard you want to create (e.g., Basic, Cloze, or Prompt).
  - `metadata`:
    - `title`: Give your flashcard a title or heading.
    - `resource`: Optionally, include a link to related content.
    - `tags`: Use tags to categorize and organize your flashcards.
  - `spec`:
    - `front`: The content displayed on the front side of the flashcard, typically a question.
    - `back`: The content displayed on the back side of the flashcard, which provides the answer or additional information.

After defining your flashcards, you can organize them in a directory to keep them alongside other decks. This choice is yours and helps you maintain a well-organized Anki card collection.

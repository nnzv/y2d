<!-- Copyright 2023 Enzo Venturi. All rights reserved. -->
<!-- Use of this source code is governed by a BSD-style -->
<!-- license that can be found in the LICENSE file. -->

# Sypnosis

I made this project to simplify Anki deck creation using YAML text files. Now, let's explore its key features.

## Automation

This eliminates the need for manual intervention. You can specify the location of your YAML files to the program, which 
will then autonomously convert them into Anki decks.

## Simplicity

This project keeps things easy and uncomplicated in a few ways:

1. **Card Templates**: Instead of having a ton of different card styles to choose from, it offers just three: "Basic," "Prompt," and "Cloze." These are like different layouts for your flashcards. You pick the one that fits your needs best.
2. **Markdown**: Easily style your text with Markdown, currently available for ".spec.front" and ".spec.back" fields. To expand this support to other areas, consider forking the project.
3. **Code Highlighting**: If you're into programming, this project also helps you make your code look good in your flashcards. 

# Getting Started

To begin using this Anki deck creator, ensure you have Python 3 installed on your system. Follow these simple steps to set up your environment and install the necessary dependencies:

1. Create a Python virtual environment:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install the required dependencies:

   ```sh
   pip3 install -r requirements.txt
   ```

# Quick Demonstration

Generate your first Anki deck with this simple command:

```sh
python3 cli.py dev-lang
```

You'll receive a confirmation log message like this:

```
Deck 'Get started with Go' written to get-started-with-go.apkg
```

Import the generated `.apkg` file into Anki, and you've successfully created and imported your first deck.

# Workflow

Here's how the workflow unfolds:

1. Organize your decks effortlessly by adding directories as needed.

2. Within each directory, define your decks using YAML files. For instance, in the 'dev-lang' directory, you'll discover a deck named 'go.yml'.

   ```
   .
   |-- cli.py
   `-- dev-lang
       `-- go.yml
   ```

3. If you want to create multiple decks, it's as simple as running this command:

   ```sh
   python3 cli.py dev-lang/go.yml another-category/deck.yml
   ```

# Flashcard Structure

To craft flashcards using this project, follow the YAML structure provided below as a guideline:

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

This structure is composed of the following elements:

- `id`: A unique identifier for your deck.
- `metadata`:
  - `name`: The title or name of your deck.
  - `description`: A concise deck description.
- `cards`: An array of individual flashcard entries.
  - `card`: Choose the type of flashcard (e.g., Basic, Cloze, or Prompt).
  - `metadata`:
    - `title`: Flashcard title or heading.
    - `resource`: Optionally, include a link to related content.
    - `tags`: Use tags for easy categorization.
  - `spec`:
    - `front`: Content displayed on the front side (usually a question).
    - `back`: Content displayed on the back side (providing the answer or additional information).

With this structure, you can create well-organized flashcards for your Anki card collection.

# License

Source files are distributed under the BSD-style license found in the `LICENSE` file.

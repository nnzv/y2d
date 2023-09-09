Simplify your Anki flashcard workflow creation effortlessly with this approach.

## Key Features

* **YAML Deck Configuration**: Define decks using YAML code.
* **Markdown Formatting**: Format 'back' and 'front' fields with Markdown.
* **Title and Description Support**: Customize each deck with a title and description.
* **Code Highlighting**: Highlight code using Markdown extensions.
* **Three Card Types**: Create Basic, Cloze, and Prompt cards.
    1. Basic: Front and back flashcards.
    2. Cloze: Supports Cloze deletion notation.
    3. Prompt: Ask users for answers.
* **Tagging**: Organize cards efficiently with tags.

## Requirements

* Python 3

## Demonstration

1. Create a Virtual Environment
   ```sh
   % python3 -m venv venv
   ```

2. Activate the Environment
   ```sh
   % source venv/bin/activate
   ```

3. Install Requirements
   ```sh
   % python3 -r requirements.txt
   ```

4. Test Run
   ```sh
   % python3 cli.py dev-lang
   ```

Organize decks into directories for effective management. When you provide a directory as an argument to the 'cli.py' script, each .yml file in that directory 
becomes a deck in `.apkg` file format. While adding support for `.yaml` extensions is possible, it's not a priority. This project is open source, so _feel free 
to fork and customize it_!

To create a standalone deck:
```sh
% python3 cli.py dev-lang/go.yml
```

For a combination of complex decks:
```sh
% python3 cli.py dev-lang/go.yml,another/card.yml
```

## Flashcard Structure

To create a flashcard, you need to follow a specific YAML structure like the example below. This structure helps generate a `.apkg` file, which is the Anki 
deck format.

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

Here's a breakdown of what each part does:

- `id`: This is a unique identifier for your deck.
- `metadata`:
  - `name`: Specify the title or name of your deck.
  - `description`: Add a short and concise description of your deck.
- `cards`: This section contains an array of individual flashcard entries.
  - `card`: Choose the type of flashcard you want to create (e.g., Basic, Cloze, or Prompt).
  - `metadata`:
    - `title`: Give your flashcard a title or heading.
    - `resource`: Optionally, you can include a link to related content.
    - `tags`: Use tags to categorize and organize your flashcards.
  - `spec`:
    - `front`: The content displayed on the front side of the flashcard, typically a question.
    - `back`: The content displayed on the back side of the flashcard, which provides the answer or additional information.

Once you've defined your flashcards, you can organize them in a directory if you want to keep them alongside other decks. The choice is yours, and it helps you stay organized as you build your Anki card collection.

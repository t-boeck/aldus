# Aldus: The Bilingual Book Maker

Aldus is a tool for generating bilingual (English–Chinese) books. It processes plain text input, translates it using an LLM (like DeepSeek or GPT-4), and assembles it into a professional LaTeX document with parallel columns.

## Features

- **Text Processing**: Automatically splits text into paragraphs and sentences.
- **AI Translation**: Uses LLMs to translate text while preserving style and tone.
- **Bilingual Layout**: Generates a LaTeX document with English and Chinese side-by-side using the `paracol` package.
- **PDF Generation**: Compiles the LaTeX document into a PDF (requires local LaTeX installation or Docker).
- **Customizable**:
    - **API Key**: Bring your own API key (DeepSeek, OpenAI).
    -   **System Prompt**: Customize the translator's persona and instructions.
-   **Cost Effective**: A 400-page book translated with DeepSeek Chat costs approximately $0.25.

## Running Locally

### Prerequisites

1.  **Python 3.10+**
2.  **LaTeX Distribution** (for PDF generation):
    -   Must include `xelatex` and Chinese language support (`ctex` package).
    -   *Mac*: Install [MacTeX](https://www.tug.org/mactex/).
    -   *Linux*: Install `texlive-xetex`, `texlive-lang-chinese`.

### Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Web App

1.  Start the Flask application:
    ```bash
    python -m aldus.app
    ```
2.  Open your browser to [http://localhost:5000](http://localhost:5000).
3.  Upload your English `.txt` file, enter your API Key, and click "Translate".

## Running with Docker (Recommended)

Docker is the easiest way to run Aldus because it handles the complex LaTeX dependencies for you.

1.  **Build the image**:
    ```bash
    docker build -t aldus .
    ```

2.  **Run the container**:
    ```bash
    docker run -p 5000:5000 aldus
    ```

3.  Open [http://localhost:5000](http://localhost:5000).

## Project Structure

-   `aldus/`: The Flask web application.
    -   `app.py`: Main application logic.
    -   `templates/`: HTML templates.
-   `scripts/`: Core processing logic.
    -   `main.py`: CLI entry point (alternative to web app).
    -   `translator.py`: Handles LLM interaction.
    -   `latex_utils.py`: Generates and compiles LaTeX.
    -   `text_utils.py`: Text splitting and formatting.
# Aldus: The Bilingual Book Maker

Aldus is a tool for generating bilingual books, showing both languages side by side. It processes plain text input, translates it using LLMs (like DeepSeek or GPT-4), and assembles it into a LaTeX document with parallel columns.

## Features

- **Multi-Language Support**: Translate between English, Chinese, Spanish, and French.
- **Dynamic Layout**: Automatically adjusts column widths based on language compactness (e.g., wider columns for English vs. Chinese).
- **AI Translation**: Uses LLMs to translate text while preserving style, tone, and nuance.
- **Advanced Context**: Optional inputs for Author, Year, and Genre to guide the AI's translation style.
- **Customizable Formatting**: Choose font sizes (12pt, 14pt, 16pt, 17pt) to suit your reading preference.
- **Library**: A built-in library to view, download, and manage your generated files.
- **Compile Tool**: A utility to compile any `.tex` file into a PDF directly within the app.
- **Robust Processing**: Handles text splitting, bolding of first words for readability, and LaTeX generation.
- **Cost Effective**: A 400-page book translated with DeepSeek Chat costs approximately $0.25.

## Running Locally

> **New to Docker or GitHub?**  
> Check out our **[Beginner's Setup Guide](SETUP_GUIDE.md)** for step-by-step instructions on installing the necessary software and running the app.

### Prerequisites

1.  **Python 3.10+**
2.  **LaTeX Distribution** (for PDF generation):
    -   Must include `xelatex` and language support packages (`ctex`, `babel`, `texlive-lang-spanish`, `texlive-lang-french`).
    -   *Mac*: Install [MacTeX](https://www.tug.org/mactex/).
    -   *Linux*: Install `texlive-xetex`, `texlive-lang-chinese`, `texlive-lang-spanish`, `texlive-lang-french`, `texlive-latex-extra`.

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

## Running with Docker (Recommended)

Docker is the easiest way to run Aldus because it handles the complex LaTeX dependencies for you.

1.  **Build the image**:
    ```bash
    docker build -t aldus .
    ```

2.  **Run the container**:
    ```bash
    docker run -p 5000:5000 -v $(pwd)/aldus/output:/app/aldus/output aldus
    ```
    *(Optional: The `-v` flag mounts the output directory so files persist on your host machine)*

3.  Open [http://localhost:5000](http://localhost:5000).

## Project Structure & File Descriptions

### `aldus/` (Web Application)
-   **`app.py`**: The core Flask application. Handles routing (`/`, `/start`, `/progress`, `/library`, `/compile`), job management, and orchestrates the translation pipeline.
-   **`templates/`**:
    -   `base.html`: The base layout template with the navigation bar and common styles.
    -   `index.html`: The main landing page with the upload form and configuration options.
    -   `progress.html`: Displays real-time translation progress, logs, and download links.
    -   `library.html`: Lists all generated files (PDF, TeX, TXT) with metadata and download buttons.
    -   `compile.html`: A utility page to upload and compile raw `.tex` files.
-   **`static/`**: Contains static assets like images (`aldus.png`, `favicon.png`).
-   **`output/`**: The destination folder for all generated files.

### `scripts/` (Core Logic)
-   **`translator.py`**: Handles interactions with the LLM API (OpenAI/DeepSeek). Manages the system prompt and translation requests.
-   **`latex_utils.py`**: Responsible for generating the LaTeX code. It handles:
    -   Document structure (`extarticle`).
    -   Dynamic package loading (`ctex`, `babel`).
    -   Column ratio calculation based on language pairs.
    -   PDF compilation using `xelatex`.
-   **`text_utils.py`**: Utilities for text processing:
    -   Splitting text into paragraphs and sentences.
    -   Bolding the first word of sentences (supports English and Chinese tokenization).
    -   Sanitizing text for LaTeX compatibility.

### Root Files
-   **`Dockerfile`**: Defines the Docker image, installing Python, Flask, and the full TeX Live distribution with necessary language packs.
-   **`requirements.txt`**: Lists Python dependencies (`flask`, `openai`, `requests`, `gunicorn`, `jieba`).
-   **`README.md`**: This documentation file.
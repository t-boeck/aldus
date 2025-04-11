# Book Maker

Book Maker is a small, personal project for generating bilingual (English–Chinese) books. The tool processes plain text input files by splitting them into paragraphs and sentences, bolds the first word of each sentence (with special handling for Chinese text), and assembles everything into a LaTeX document that uses parallel columns for English and Chinese.

## Features

- **Text Processing**:  
  - Splits texts into paragraphs (using double newlines).
  - Splits paragraphs into sentences based on punctuation (supports both English and Chinese punctuation).
  - Automatically bolds the first word (or first Chinese word/character) of each sentence.

- **LaTeX Generation**:  
  - Assembles the processed text into a LaTeX file using the `paracol` package for parallel bilingual columns.
  - Sets line spacing and formatting for each language.
  - Supports customizations like column ratios and margin settings.

- **(Planned) Translation**:  
  - Future functionality will include automatic translation of an English text into Chinese using an LLM API or other translation service.
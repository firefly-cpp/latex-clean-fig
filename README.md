# latex-clean-fig

## Motivation

The package provides a simple command-line tool to help authors clean up unused image files in a project directory before submitting a paper. Multiple versions of figures often accumulate in the folder during the writing process, making it cluttered and difficult to manage. This tool scans the LaTeX file for figures included using the \includegraphics command and compares them against the image files in the specified folder. It identifies unused images and removes them, leaving only the files referenced in the LaTeX document. This is especially useful for ensuring the project directory remains tidy and submission-ready.

## 📦 Installation

### pip

Install latex-clean-fig with pip:

```sh
pip install latex-clean-fig
```

### How to use?

```sh
clean-fig TEX_FILE FOLDER
```
where:

- TEX_FILE: Path to your LaTeX file.
- FOLDER: Path to the folder containing image files.

This will scan TEX_FILE for included figures and remove any unused image files from the FOLDER directory.

## 🔑 License

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This package is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!

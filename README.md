<h1 align="center">
    latex-clean-fig
</h1>

<p align="center">
    <img alt="PyPI version" src="https://img.shields.io/pypi/v/latex-clean-fig.svg" />
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/latex-clean-fig.svg">
    <a href="https://pepy.tech/project/latex-clean-fig">
        <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/latex-clean-fig.svg">
    </a>
    <img alt="Downloads" src="https://static.pepy.tech/badge/latex-clean-fig">
    <img alt="latex-clean-fig" src="https://github.com/firefly-cpp/latex-clean-fig/actions/workflows/test.yml/badge.svg" />
</p>

<p align="center">
    <img alt="Repository size" src="https://img.shields.io/github/repo-size/firefly-cpp/latex-clean-fig" />
    <img alt="License" src="https://img.shields.io/github/license/firefly-cpp/latex-clean-fig.svg" />
    <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/w/firefly-cpp/latex-clean-fig.svg">
    <a href="https://isitmaintained.com/project/firefly-cpp/latex-clean-fig">
        <img alt="Percentage of issues still open" src="https://isitmaintained.com/badge/open/firefly-cpp/latex-clean-fig.svg">
    </a>
    <a href="https://isitmaintained.com/project/firefly-cpp/latex-clean-fig">
        <img alt="Average time to resolve an issue" src="https://isitmaintained.com/badge/resolution/firefly-cpp/latex-clean-fig.svg">
    </a>
    <img alt="GitHub contributors" src="https://img.shields.io/github/contributors/firefly-cpp/latex-clean-fig.svg"/>
</p>

<p align="center">
    <a href="#-motivation">🎯 Motivation</a> •
    <a href="#-installation">📦 Installation</a> •
    <a href="#-license">🔑 License</a>
</p>

## 🎯 Motivation

The package provides a simple command-line tool to help authors clean up unused image files in a project directory before submitting a paper. Multiple versions of figures often accumulate in the folder during the writing process, making it cluttered and difficult to manage. This tool scans the LaTeX file for figures included using the \includegraphics command and compares them against the image files in the specified folder. It identifies unused images and removes them, leaving only the files referenced in the LaTeX document. This is especially useful for ensuring the project directory remains tidy and submission-ready.

## 📦 Installation

### pip

Install `latex-clean-fig` with pip:

```sh
pip install latex-clean-fig
```

### How to use?

```sh
clean-fig TEX_FILE FOLDER
```
where:

- `TEX_FILE`: Path to your LaTeX file.
- `FOLDER`: Path to the folder containing image files.

This will scan TEX_FILE for included figures and remove any unused image files from the FOLDER directory.

## 🔑 License

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This package is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!

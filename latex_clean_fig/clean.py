import os
import re
import typer

app = typer.Typer()

# Function to extract included images from LaTeX file
def extract_included_images(tex_file: str, base_dir: str = None, visited: set = None):
    if visited is None:
        visited = set()

    # Determine the absolute path of the current file
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(tex_file))
        file_path = os.path.abspath(tex_file)
    else:
        # If it's an included file, resolve relative to base_dir
        if not os.path.isabs(tex_file):
            file_path = os.path.join(base_dir, tex_file)
        else:
            file_path = tex_file
        
        # Handle missing extension
        if not os.path.exists(file_path) and os.path.exists(file_path + ".tex"):
            file_path += ".tex"

    # Avoid cycles and reprocessing
    if file_path in visited:
        return set()
    
    if not os.path.exists(file_path):
        return set()

    visited.add(file_path)

    with open(file_path, 'r', encoding="utf-8", errors="ignore") as file:
        content = file.read()

    # Remove comments to avoid matching commented-out images
    # Protect escaped backslashes and percents
    content = content.replace('\\\\', '__DBL_BS__')
    content = content.replace('\\%', '__ESC_PCT__')
    # Remove comments
    content = re.sub(r'%.*', '', content)
    # Restore protected characters
    content = content.replace('__ESC_PCT__', '\\%')
    content = content.replace('__DBL_BS__', '\\\\')

    # Regex to match \includegraphics{...} or \includegraphics[...]{...}
    image_pattern = re.compile(
        r"\\includegraphics(?:\s*\[.*?\])?\s*\{\s*([^}]+?)\s*\}"
    )

    # Regex to match \includegraphics{...} or \includegraphics[...]{...}
    svg_image_pattern = re.compile(
        r"\\includesvg(?:\s*\[.*?\])?\s*\{\s*([^}]+?)\s*\}"
    )

    # Regex to match \input{...} or \include{...}
    include_pattern = re.compile(
        r"\\(?:input|include)(?:\s*\[.*?\])?\s*\{\s*([^}]+?)\s*\}"
    )

    images = set()
    for match in image_pattern.findall(content):
        # Normalize: lowercase + strip directories
        basename = os.path.basename(match.strip()).lower()
        stem, _ = os.path.splitext(basename)

        images.add(match)  # e.g. myplot.pdf
        # images.add(stem)      # e.g. myplot

    for match in svg_image_pattern.findall(content):
        # Normalize: lowercase + strip directories
        basename = os.path.basename(match.strip()).lower()
        stem, _ = os.path.splitext(basename)

        images.add(match)  # e.g. myplot.svg
        # images.add(stem)      # e.g. myplot

    for match in include_pattern.findall(content):
        included_file = match.strip()
        images.update(extract_included_images(included_file, base_dir, visited))

    return images

# Function to find and remove unused images
def remove_unused_images(folder: str, tex_file: str, dry_run: bool = False):
    tex_file_root = os.path.dirname(tex_file)
    # Extract images used in the LateX file
    included_images = extract_included_images(tex_file)

    # Add logging for debug purposes
    #TODO: Make it optional
    typer.echo(f"Detected included images: {included_images}")

    # List all files in the folder
    folder_files = os.listdir(folder)

    # Keep track of removed files
    removed_files = []
    total_files = 0
    for included_image in included_images:
        typer.echo(f"Looking for: {os.path.join(tex_file_root, included_image.lower())}")

    for root, dirs, files in os.walk(folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file1, file_ext = os.path.splitext(file_name)
            normalized_file1 = file1.lower()

            if file_ext.lower() in {'.png', '.jpg', '.jpeg', '.pdf', '.eps', '.svg'}:
                total_files += 1
                # Check for matches with extensions
                matched = any(
                    normalized_file1 == os.path.splitext(os.path.basename(included_image))[0].lower()
                    for included_image in included_images
                )

                if not matched:
                    typer.echo(f"Removing unused image: {file_path}")
                    if not dry_run:
                        os.remove(file_path)
                    removed_files.append(file_name)

    return included_images, removed_files, total_files

@app.command()
def clean_images(tex_file: str = typer.Argument(..., help="Path to the LaTeX file."),
                 folder: str = typer.Argument(..., help="Path to the folder containing images."),
                 dry_run: bool = typer.Option(False, help="Run in dry-run mode without removing files.")):
    """Remove unused images from a folder based on a LaTeX file."""
    # Check if both path exist
    if not os.path.exists(tex_file):
        typer.echo("Error: The LaTeX file does not exist.", err=True)
        raise typer.Exit(code=1)
    if not os.path.isdir(folder):
        typer.echo("Error: The folder path is not valid.", err=True)
        raise typer.Exit(code=1)

    # Remove unused images
    included_images, removed_files, total_files = remove_unused_images(folder, tex_file, dry_run=dry_run)

    # Print stats
    typer.echo(f"Statistics:")
    typer.echo(f"- Total included images found in LaTeX file: {len(included_images)}")
    typer.echo(f"- Total image files found in folder: {total_files}")
    typer.echo(f"- Total unused images removed: {len(removed_files)}")

    if removed_files:
        typer.echo("The following unused images were removed:")
        for file in removed_files:
            typer.echo(f"- {file}")
    else:
        typer.echo("No unused images were found.")

if __name__ == "__main__":
    app()

import os
import re
import typer

app = typer.Typer()

# Function to extract included images from LaTeX file
def extract_included_images(tex_file: str):
    with open(tex_file, 'r') as file:
        content = file.read()

    # Regex to match \includegraphics{...} or \includegraphics[...]{...} # TODO: check the other libraries
    image_pattern = re.compile(r"\\includegraphics(?:\[.*?\])?\{(.+?)\}")

    # Extract all image paths (normalize names to lowercase)
    images = set(match.lower() for match in image_pattern.findall(content))
    return images

# Function to find and remove unused images
def remove_unused_images(folder: str, tex_file: str):
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

    for file_name in folder_files:
        file_path = os.path.join(folder, file_name)

        # Check if file is an image (by extension) and not in included images
        if os.path.isfile(file_path):
            file1, file_ext = os.path.splitext(file_name)
            normalized_file1 = file1.lower()

            if file_ext.lower() in {'.png', '.jpg', '.jpeg', '.pdf', '.eps'}:
                total_files += 1
                # Check for matches with extensions
                matched = any(
                    normalized_file1 == included_image.lower() or
                    file_name.lower() == included_image.lower()
                    for included_image in included_images
                )

                if not matched:
                    typer.echo(f"Removing unused image: {file_name}")
                    os.remove(file_path)
                    removed_files.append(file_name)

    return included_images, removed_files, total_files

@app.command()
def clean_images(tex_file: str = typer.Argument(..., help="Path to the LaTeX file."),
                 folder: str = typer.Argument(..., help="Path to the folder containing images.")):
    """Remove unused images from a folder based on a LaTeX file."""
    # Check if both path exist
    if not os.path.exists(tex_file):
        typer.echo("Error: The LaTeX file does not exist.", err=True)
        raise typer.Exit(code=1)
    if not os.path.isdir(folder):
        typer.echo("Error: The folder path is not valid.", err=True)
        raise typer.Exit(code=1)

    # Remove unused images
    included_images, removed_files, total_files = remove_unused_images(folder, tex_file)

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

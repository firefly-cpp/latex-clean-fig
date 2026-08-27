import os
import tempfile

from latex_clean_fig.clean import remove_unused_images


# An image referenced with its file extension must not be removed
def test_image_referenced_with_extension_is_kept():
    latex_content = """
    \\includegraphics{figure1.png}
    """

    # Create a temporary LaTeX file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tex") as temp_tex_file:
        temp_tex_file.write(latex_content.encode("utf-8"))
        tex_file_path = temp_tex_file.name

    # Create a temporary directory with one used and one unused image
    with tempfile.TemporaryDirectory() as temp_dir:
        open(os.path.join(temp_dir, "figure1.png"), "w").close()
        open(os.path.join(temp_dir, "unused.png"), "w").close()

        # Only the unused image may be reported
        _, removed, _ = remove_unused_images(temp_dir, tex_file_path, dry_run=True)
        assert removed == ["unused.png"], f"Expected ['unused.png'], got {removed}"

    os.remove(tex_file_path)


# With graphicspath the reference carries no folder, but the file lives in a subfolder
def test_image_in_subfolder_is_kept():
    latex_content = """
    \\graphicspath{ {./images/} }
    \\includegraphics{logo.pdf}
    """

    with tempfile.TemporaryDirectory() as project_dir:
        # Create the LaTeX file in the project root
        tex_file_path = os.path.join(project_dir, "main.tex")
        with open(tex_file_path, "w", encoding="utf-8") as f:
            f.write(latex_content)

        # Create the images subfolder with one used and one unused image
        images_dir = os.path.join(project_dir, "images")
        os.makedirs(images_dir)
        open(os.path.join(images_dir, "logo.pdf"), "w").close()
        open(os.path.join(images_dir, "unused.pdf"), "w").close()

        # Only the unused image may be reported
        _, removed, _ = remove_unused_images(images_dir, tex_file_path, dry_run=True)
        assert removed == ["unused.pdf"], f"Expected ['unused.pdf'], got {removed}"
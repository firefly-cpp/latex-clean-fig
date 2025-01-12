import tempfile
import os
from latex_clean_fig.clean import remove_unused_images

def test_remove_unused_images():
    # Simulate LaTeX file
    latex_content = """
    \\includegraphics{figure1}
    \\includegraphics{figure2}
    """

    # Create a temporary LaTeX file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tex") as temp_tex_file:
        temp_tex_file.write(latex_content.encode("utf-8"))
        tex_file_path = temp_tex_file.name

    # Create a temporary directory with images
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create image files
        included_images = ["figure1.png", "figure2.jpg"]
        unused_images = ["unused1.png", "unused2.jpg"]
        for image in included_images + unused_images:
            open(os.path.join(temp_dir, image), "w").close()

        # Call remove_unused_images
        included, removed, total_files = remove_unused_images(temp_dir, tex_file_path)
        assert included == {"figure1", "figure2"}, f"Expected {{'figure1', 'figure2'}}, got {included}"
        assert sorted(removed) == sorted(unused_images), f"Expected {unused_images}, got {removed}"
        assert total_files == len(included_images + unused_images), f"Expected {len(included_images + unused_images)}, got {total_files}"

    os.remove(tex_file_path)

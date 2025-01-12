import tempfile
import os
from latex_clean_fig.clean import extract_included_images

def test_extract_included_images():
    latex_content = """
    \\documentclass{article}
    \\usepackage{graphicx}
    \\begin{document}
    \\includegraphics{figure1}
    \\includegraphics[width=0.5\\textwidth]{figure2}
    \\end{document}
    """

    # Create a temporary LaTeX file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".tex") as temp_file:
        temp_file.write(latex_content.encode("utf-8"))
        temp_file_path = temp_file.name

    try:
        # Extract included images
        images = extract_included_images(temp_file_path)
        assert images == {"figure1", "figure2"}, f"Expected {{'figure1', 'figure2'}}, got {images}"
    finally:
        os.remove(temp_file_path)

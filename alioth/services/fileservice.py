import pymupdf
import logging
from typing import Optional, Tuple
from enum import Enum, auto
import re
import base64
import tkinter as tk

from pymupdf.extra import page_count

log = logging.getLogger(__name__)

# you have to specify a path, and now this serves as the
# location where you can do read or write, and that permission
# will be instantiated at init
class FileService():
    def __init__(self, file_path: str):
        self._file_path = file_path
        return

    # create a file service object that exists as a
    # representation of the file in the system
    # then it cannot return any pymupdf specific
    # data structures only generic python objects

    # either we want to get the list of all the blocks
    # in a file with their associated metadata or we
    # want to retrieve a specific page with highlighting

    def get_block_list(self):
        doc = pymupdf.open(self._file_path)
        blocks_list = []
        for pnum, page in enumerate(doc):
            page_blocks = page.get_text("blocks")
            for b in page_blocks:
                x0, x1, y0, y1, text, bid, btype = b
                text = text.replace("\n", "")

                block_dict = {
                    "text": text,
                    "pnum": pnum,
                    "bbox": (x0, x1, y0, y1),
                }
                blocks_list.append(block_dict)
        doc.close()
        return blocks_list

    def get_highlighted_block(self, block, save_path: str):
        doc = pymupdf.open(self._file_path)
        page = doc[block["pnum"]]
        highlight = page.add_highlight_annot(block["bbox"])
        doc.save(save_path, garbage = 4, deflate = True, clean = True)
        doc.close()

    def live_highlight_view(self, block: dict, zoom: float = 2.0, window_title: Optional[str] = None):
        """
        Open a live Tkinter window to display the PDF page with highlight.
        - Scrollable and zoomable.
        - Highlight is temporary and not saved to disk.

        Args:
            block: dict with keys { "pnum": int, "bbox": (x0, y0, x1, y1), ... }
            zoom: initial zoom scale (1.0 = 72 DPI).
            window_title: optional title for the window.
        """
        import tkinter as tk
        from tkinter import Scrollbar, Canvas
        import base64
        import pymupdf

        # Load the document
        doc = pymupdf.open(self._file_path)
        page = doc[block["pnum"]]
        rect = pymupdf.Rect(block["bbox"])
        page.add_highlight_annot(rect)

        # Tkinter setup
        root = tk.Tk()
        root.title(window_title or f"Page {block['pnum'] + 1}")

        # Scrollable canvas
        canvas = Canvas(root, highlightthickness=0)
        hbar = Scrollbar(root, orient="horizontal", command=canvas.xview)
        vbar = Scrollbar(root, orient="vertical", command=canvas.yview)
        canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        hbar.grid(row=1, column=0, sticky="ew")
        vbar.grid(row=0, column=1, sticky="ns")
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        def render(scale):
            mat = pymupdf.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat, annots=True)
            png_bytes = pix.tobytes("png")
            b64_png = base64.b64encode(png_bytes)
            photo = tk.PhotoImage(data=b64_png)
            canvas.delete("all")
            canvas.img = photo
            canvas.create_image(0, 0, image=photo, anchor="nw")
            canvas.config(scrollregion=(0, 0, pix.width, pix.height))

        # Initial render
        render(zoom)

        # Zoom controls with +/- keys
        def zoom_in(event=None):
            nonlocal zoom
            zoom *= 1.25
            render(zoom)

        def zoom_out(event=None):
            nonlocal zoom
            zoom /= 1.25
            render(zoom)

        root.bind("<plus>", zoom_in)
        root.bind("<equal>", zoom_in)  # for '=' key on US keyboard
        root.bind("<minus>", zoom_out)

        root.mainloop()
        doc.close()


"""
def show_highlighted_block(self, block: dict, zoom: float = 2.0, window_title: Optional[str] = None):
    Open a small window to display the page containing `block` with that block highlighted.
    - Does not save anything to disk.
    - Closes when the window is closed by the user.

    Args:
        block: dict with keys { "pnum": int, "bbox": (x0, x1, y0, y1), ... }
        zoom: render scale (1.0 = 72 DPI). Use 2.0 for better readability.
        window_title: optional title for the preview window.
    import base64
    import tkinter as tk

    # Load the page and add a temporary highlight annotation (not persisted)
    doc = pymupdf.open(self._file_path)
    try:
        page = doc[block["pnum"]]
        # Ensure bbox is interpreted as a rectangle (no persistence without save())
        rect = pymupdf.Rect(block["bbox"])
        page.add_highlight_annot(rect)

        # Render page with annotations to an in-memory image
        mat = pymupdf.Matrix(zoom/2, zoom/2)
        pix = page.get_pixmap(matrix=mat, annots=True)  # includes highlight
    finally:
        # No save: nothing gets written to the original file
        doc.close()

    # Convert to PNG bytes for Tkinter PhotoImage
    png_bytes = pix.tobytes("png")
    b64_png = base64.b64encode(png_bytes)

    # Create a simple Tk window to show the image
    root = tk.Tk()
    root.title(window_title or f"Page {block['pnum'] + 1} preview")

    # Create Tk image from in-memory data (no files involved)
    photo = tk.PhotoImage(data=b64_png)
    label = tk.Label(root, image=photo)
    label.image = photo  # keep a reference to avoid garbage collection
    label.pack()

    # Fit window size to image
    root.geometry(f"{int(pix.width)}x{int(pix.height)}")

    # Start the UI loop; window closes when user closes it
    root.mainloop()
"""

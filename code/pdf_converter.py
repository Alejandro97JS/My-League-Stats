from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

class PDFPresentation:
    def __init__(self, filename, page_size=landscape(A4)):
        """
        Initializes the PDF presentation.
        :param filename: Name of the PDF file to create.
        :param page_size: Page size (default, landscape A4).
        """
        self.filename = filename
        self.page_size = page_size
        self.c = canvas.Canvas(filename, pagesize=page_size)
        self.width, self.height = page_size
        self._first_slide = True

    def add_image_slide(self, image_path, scale_to_fit=True):
        """
        Adds a slide that is just an image.
        :param image_path: Path to the image.
        :param scale_to_fit: If True, scales the image to fit the page.
        """
        if self._first_slide:
            self._first_slide = False
        else:
            self.c.showPage()
        img = ImageReader(image_path)
        iw, ih = img.getSize()
        if scale_to_fit:
            ratio = min(self.width / iw, self.height / ih)
            new_w = iw * ratio
            new_h = ih * ratio
            x = (self.width - new_w) / 2
            y = (self.height - new_h) / 2
            self.c.drawImage(img, x, y, width=new_w, height=new_h)
        else:
            x = (self.width - iw) / 2
            y = (self.height - ih) / 2
            self.c.drawImage(img, x, y)
    

    def add_text_slide(self, text, font="Helvetica-Bold", font_size=36, margin=40, body_font_size=None):
        """
        Adds a slide with centered, wrapped text. The first line (before first '\n') is the title (large font), the rest is body (smaller font).
        :param text: Text to display. First line is title, rest is body.
        :param font: Font of the text.
        :param font_size: Font size for the title.
        :param margin: Margin from page sides.
        :param body_font_size: Font size for the body text (default: font_size * 0.6)
        """
        if self._first_slide:
            self._first_slide = False
        else:
            self.c.showPage()
        max_width = self.width - 2 * margin
        if body_font_size is None:
            body_font_size = int(font_size * 0.6)

        # Split into title and body
        if '\n' in text:
            title, body = text.split('\n', 1)
        else:
            title, body = text, ""

        # Prepare title lines (wrap if needed)
        self.c.setFont(font, font_size)
        title_lines = []
        words = title.split()
        current_line = ""
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if stringWidth(test_line, font, font_size) <= max_width:
                current_line = test_line
            else:
                if current_line:
                    title_lines.append(current_line)
                current_line = word
        if current_line:
            title_lines.append(current_line)

        # Prepare body lines (wrap and respect explicit newlines)
        body_lines = []
        if body:
            self.c.setFont(font, body_font_size)
            paragraphs = body.split('\n')
            for para in paragraphs:
                words = para.split()
                current_line = ""
                for word in words:
                    test_line = current_line + (" " if current_line else "") + word
                    if stringWidth(test_line, font, body_font_size) <= max_width:
                        current_line = test_line
                    else:
                        if current_line:
                            body_lines.append(current_line)
                        current_line = word
                if current_line:
                    body_lines.append(current_line)
                # After each paragraph, add a blank line (except after last)
                if para != paragraphs[-1]:
                    body_lines.append("")

        # Calculate total height for centering
        total_height = len(title_lines) * font_size * 1.2 + (len(body_lines) * body_font_size * 1.2 if body_lines else 0)
        y = (self.height + total_height) / 2 - font_size

        # Draw title lines
        self.c.setFont(font, font_size)
        for line in title_lines:
            text_width = stringWidth(line, font, font_size)
            x = (self.width - text_width) / 2
            self.c.drawString(x, y, line)
            y -= font_size * 1.2

        # Draw body lines
        if body_lines:
            self.c.setFont(font, body_font_size)
            for line in body_lines:
                text_width = stringWidth(line, font, body_font_size)
                x = (self.width - text_width) / 2
                self.c.drawString(x, y, line)
                y -= body_font_size * 1.2

    def save(self):
        """
        Saves the PDF to disk.
        """
        self.c.save()
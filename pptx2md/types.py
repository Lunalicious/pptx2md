from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

from pydantic import BaseModel


class ConversionConfig(BaseModel):
    """Configuration for PowerPoint to Markdown conversion."""

    pptx_path: Path
    """Path to the pptx file to be converted"""

    output_path: Path
    """Path of the output file"""

    image_dir: Optional[Path]
    """Where to put images extracted"""

    title_path: Optional[Path]
    """Path to the custom title list file"""

    image_width: Optional[int] = None
    """Maximum image width in px"""

    disable_image: bool = False
    """Disable image extraction"""

    disable_wmf: bool = False
    """Keep wmf formatted image untouched (avoid exceptions under linux)"""

    disable_color: bool = False
    """Do not add color HTML tags"""

    disable_escaping: bool = False
    """Do not attempt to escape special characters"""

    disable_notes: bool = False
    """Do not add presenter notes"""

    enable_slides: bool = False
    """Deliniate slides with `\n---\n`"""

    is_wiki: bool = False
    """Generate output as wikitext (TiddlyWiki)"""

    is_mdk: bool = False
    """Generate output as madoko markdown"""

    is_qmd: bool = False
    """Generate output as quarto markdown presentation"""

    min_block_size: int = 15
    """The minimum character number of a text block to be converted"""

    page: Optional[int] = None
    """Only convert the specified page"""

    custom_titles: dict[str, int] = {}
    """Mapping of custom titles to their heading levels"""


class ElementType(str, Enum):
    TITLE = "title"
    LIST_ITEM = "list_item"
    PARAGRAPH = "paragraph"
    IMAGE = "image"
    TABLE = "table"
    NOTE = "note"
    COLUMN_START = "column_start"
    COLUMN_END = "column_end"


class TextStyle(BaseModel):
    is_accent: bool = False
    is_strong: bool = False
    color_rgb: Optional[str] = None
    hyperlink: Optional[str] = None


class TextRun(BaseModel):
    text: str
    style: TextStyle


class Position(BaseModel):
    left: float
    top: float
    width: float
    height: float


class BaseElement(BaseModel):
    type: ElementType
    position: Optional[Position] = None
    style: Optional[TextStyle] = None


class TitleElement(BaseElement):
    type: ElementType = ElementType.TITLE
    content: str
    level: int


class ListItemElement(BaseElement):
    type: ElementType = ElementType.LIST_ITEM
    content: List[TextRun]
    level: int = 1


class ParagraphElement(BaseElement):
    type: ElementType = ElementType.PARAGRAPH
    content: List[TextRun]


class ImageElement(BaseElement):
    type: ElementType = ElementType.IMAGE
    path: str
    width: Optional[int] = None
    original_ext: str = ""  # For tracking original file extension (e.g. wmf)
    alt_text: str = ""  # For accessibility


class TableElement(BaseElement):
    type: ElementType = ElementType.TABLE
    content: List[List[List[TextRun]]]  # rows -> cols -> rich text


class NoteElement(BaseElement):
    type: ElementType = ElementType.NOTE
    content: List[TextRun]


class ColumnStartElement(BaseElement):
    type: ElementType = ElementType.COLUMN_START
    width: str  # e.g. "50%"


class ColumnEndElement(BaseElement):
    type: ElementType = ElementType.COLUMN_END


SlideElement = Union[TitleElement, ListItemElement, ParagraphElement, ImageElement, TableElement, NoteElement,
                     ColumnStartElement, ColumnEndElement]


class Slide(BaseModel):
    elements: List[SlideElement]
    notes: List[str]


class ParsedPresentation(BaseModel):
    slides: List[Slide]
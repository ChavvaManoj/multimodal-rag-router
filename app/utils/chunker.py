# # Paragarph based chunking with semantic preservation
# def chunk_text(text: str, max_words: int = 150):
#     """
#     Context-Aware Chunking v2
#     1. Split by paragraphs/sections
#     2. Preserve semantic grouping
#     3. Fallback split oversized sections
#     """

#     chunks = []

#     # Split by paragraph / section breaks
#     sections = text.split("\n\n")

#     for section in sections:
#         section = section.strip()

#         if not section:
#             continue

#         words = section.split()

#         # If section fits, keep it whole
#         if len(words) <= max_words:
#             chunks.append(section)

#         # If too large, split further
#         else:
#             for i in range(0, len(words), max_words):
#                 chunk = " ".join(words[i:i + max_words])
#                 chunks.append(chunk)

#     return chunks


# Heading-aware chunking to preserve document structure
import re


def is_heading(line: str) -> bool:
    """
    Detect likely section headings
    """
    line = line.strip()

    if not line:
        return False

    # Heading patterns:
    # ALL CAPS
    # Ends with :
    # Short title-like lines
    if line.isupper():
        return True

    if line.endswith(":"):
        return True

    if len(line.split()) <= 6 and line.istitle():
        return True

    return False


def chunk_text(text: str, max_words: int = 150):
    """
    Heading-Aware Chunking v3
    1. Detect headings
    2. Group content under headings
    3. Fallback split large sections
    """

    lines = text.splitlines()

    chunks = []
    current_section = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # New heading starts new section
        if is_heading(line):
            if current_section:
                section_text = "\n".join(current_section)
                chunks.extend(split_large_section(section_text, max_words))

            current_section = [line]

        else:
            current_section.append(line)

    # Final section
    if current_section:
        section_text = "\n".join(current_section)
        chunks.extend(split_large_section(section_text, max_words))

    return chunks


def split_large_section(section_text: str, max_words: int):
    """
    Split oversized sections while preserving structure
    """
    words = section_text.split()

    if len(words) <= max_words:
        return [section_text]

    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks
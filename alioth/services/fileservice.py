from abc import ABC, abstractmethod
import pymupdf4llm
import pathlib
import logging
from pathlib import Path
from alioth.core.decorators import *
import re

log = logging.getLogger(__name__)

@try_catch(exit_on_error=False, default_return = None)
def get_chunks_from_file(file_path: str):
    log.info(f"attempting to read and chunk file: {Path(file_path).name}")
    result = pymupdf4llm.to_markdown(file_path)
    log.info(f"successfully read and chunked file: {Path(file_path).name}")
    return result

@try_catch(exit_on_error=False, default_return = None)
def save_chunks_to_markdown(save_path, chunks):
    log.info(f"attempting to save chunks to markdown file: {Path(save_path).name}")
    pathlib.Path(save_path).write_bytes(chunks.encode())
    log.info(f"successfully saved chunks to markdown file: {Path(save_path).name}")

@try_catch(exit_on_error=False, default_return = None)
def make_chunks_into_list(markdown) -> list[str]:
    log.info(f"attempting to split markdown into list of strings")
    result = re.split(r'(?=^#{1,6}\s)', markdown, flags=re.MULTILINE)
    log.info(f"successfully split markdown into list of strings")
    return result
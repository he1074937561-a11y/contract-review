import os
import uuid
from pathlib import Path

import fitz  # PyMuPDF
from docx import Document
from fastapi import HTTPException

from app.core.config import settings


def extract_text_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs)


def extract_text(file_path: str, file_type: str) -> str:
    if file_type == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_type == "docx":
        return extract_text_from_docx(file_path)
    return ""


def save_upload_file(upload_file, user_id: int) -> tuple[str, str, str]:
    upload_dir = Path(settings.UPLOAD_DIR) / str(user_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    original_name = upload_file.filename or "untitled"
    ext = Path(original_name).suffix.lower()

    # Validate file size
    content = upload_file.file.read()
    if len(content) > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="文件大小超过 50MB 限制")
    upload_file.file.seek(0)

    if ext == ".pdf":
        file_type = "pdf"
    elif ext in (".docx", ".doc"):
        file_type = "docx"
    else:
        raise HTTPException(status_code=400, detail="不支持的文件格式，请上传 PDF 或 Word 文档")

    save_name = f"{uuid.uuid4().hex}{ext}"
    file_path = str(upload_dir / save_name)
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path, original_name, file_type

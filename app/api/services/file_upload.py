import os
import uuid

from django.conf import settings

# Extension-to-category mapping
CATEGORY_MAP = {
    # Images
    ".jpg": "images",
    ".jpeg": "images",
    ".png": "images",
    ".gif": "images",
    ".bmp": "images",
    ".webp": "images",
    ".svg": "images",
    ".ico": "images",
    # Videos
    ".mp4": "videos",
    ".avi": "videos",
    ".mov": "videos",
    ".mkv": "videos",
    ".wmv": "videos",
    ".flv": "videos",
    ".webm": "videos",
    # Audio
    ".mp3": "audio",
    ".wav": "audio",
    ".ogg": "audio",
    ".flac": "audio",
    ".aac": "audio",
    ".wma": "audio",
    # PDFs
    ".pdf": "pdfs",
    # Documents
    ".doc": "documents",
    ".docx": "documents",
    ".txt": "documents",
    ".rtf": "documents",
    ".odt": "documents",
    ".md": "documents",
    ".csv": "documents",
    ".xls": "documents",
    ".xlsx": "documents",
    ".ppt": "documents",
    ".pptx": "documents",
    ".json": "documents",
    ".xml": "documents",
}

ALLOWED_EXTENSIONS = set(CATEGORY_MAP.keys())


class FileUploadService:
    @staticmethod
    def get_upload_root() -> str:
        return os.path.join(settings.MEDIA_ROOT, "uploads")

    @staticmethod
    def get_category(filename: str) -> str:
        _, ext = os.path.splitext(filename)
        return CATEGORY_MAP.get(ext.lower(), "others")

    @classmethod
    def save_file(cls, uploaded_file) -> dict:
        """Save an uploaded file to the appropriate category folder."""
        original_name = uploaded_file.name
        ext = os.path.splitext(original_name)[1].lower()

        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(
                f"File type '{ext}' is not allowed. "
                f"Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
            )

        category = cls.get_category(original_name)
        unique_name = f"{uuid.uuid4().hex[:8]}_{original_name}"
        category_dir = os.path.join(cls.get_upload_root(), category)
        os.makedirs(category_dir, exist_ok=True)

        file_path = os.path.join(category_dir, unique_name)
        with open(file_path, "wb") as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)

        return {
            "filename": original_name,
            "stored_name": unique_name,
            "category": category,
            "size": uploaded_file.size,
        }

    @classmethod
    def list_files(cls) -> list[dict]:
        """List all uploaded files grouped by category."""
        upload_root = cls.get_upload_root()
        files = []
        if not os.path.exists(upload_root):
            return files

        for category in sorted(os.listdir(upload_root)):
            category_path = os.path.join(upload_root, category)
            if not os.path.isdir(category_path):
                continue
            for filename in sorted(os.listdir(category_path)):
                file_path = os.path.join(category_path, filename)
                if os.path.isfile(file_path):
                    # Strip the uuid prefix to get original name
                    original_name = (
                        filename[9:]
                        if len(filename) > 9 and filename[8] == "_"
                        else filename
                    )
                    files.append(
                        {
                            "filename": original_name,
                            "stored_name": filename,
                            "category": category,
                            "size": os.path.getsize(file_path),
                        }
                    )
        return files

    @classmethod
    def get_file_path(cls, stored_name: str, category: str) -> str | None:
        """Get the full path of a stored file."""
        file_path = os.path.join(cls.get_upload_root(), category, stored_name)
        if os.path.isfile(file_path):
            return file_path
        return None

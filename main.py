import sys
from pathlib import Path
import pikepdf
from PIL import Image

# Supported extensions
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
PDF_EXTENSIONS = {".pdf"}


def clean_image_metadata(input_path: Path, output_path: Path) -> bool:
    """Strips EXIF data and metadata from image files by re-creating pixel data."""
    try:
        with Image.open(input_path) as img:
            # Rebuild clean image object without EXIF payload
            clean_img = Image.new(img.mode, img.size)
            clean_img.putdata(list(img.getdata()))
            clean_img.save(output_path)
        print(f"[SUCCESS] Image metadata cleaned: {output_path.name}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to process image {input_path.name}: {e}")
        return False


def clean_pdf_metadata(input_path: Path, output_path: Path) -> bool:
    """Clears Document Info dictionary and XMP metadata streams from PDF files."""
    try:
        with pikepdf.open(input_path) as pdf:
            # Wipe traditional Document Info (Author, Title, Creator, etc.)
            pdf.docinfo.clear()

            # Wipe embedded XMP metadata if available
            if hasattr(pdf, "open_metadata"):
                with pdf.open_metadata() as meta:
                    meta.clear()

            pdf.save(output_path)
        print(f"[SUCCESS] PDF metadata cleaned: {output_path.name}")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to process PDF {input_path.name}: {e}")
        return False


def process_file(file_path_str: str) -> None:
    """Detects file extension and routes to appropriate cleaner function."""
    file_path = Path(file_path_str).resolve()

    if not file_path.exists():
        print(f"[ERROR] File does not exist: {file_path}")
        return

    ext = file_path.suffix.lower()
    output_path = (
        file_path.parent / f"{file_path.stem}_cleaned{file_path.suffix}"
    )

    if ext in IMAGE_EXTENSIONS:
        clean_image_metadata(file_path, output_path)
    elif ext in PDF_EXTENSIONS:
        clean_pdf_metadata(file_path, output_path)
    else:
        print(f"[SKIP] Unsupported file type '{ext}'. Supported: Images and PDFs.")


def process_directory(directory_path_str: str) -> None:
    """Batch-cleans all supported images and PDFs in a specified folder."""
    dir_path = Path(directory_path_str).resolve()

    if not dir_path.is_dir():
        print(f"[ERROR] Path is not a directory: {dir_path}")
        return

    supported_files = [
        f
        for f in dir_path.iterdir()
        if f.is_file()
        and f.suffix.lower() in (IMAGE_EXTENSIONS | PDF_EXTENSIONS)
        and not f.name.endswith("_cleaned" + f.suffix)
    ]

    if not supported_files:
        print("[INFO] No supported image or PDF files found in directory.")
        return

    print(f"Found {len(supported_files)} file(s) to process...\n")
    for file in supported_files:
        output_path = file.parent / f"{file.stem}_cleaned{file.suffix}"
        if file.suffix.lower() in IMAGE_EXTENSIONS:
            clean_image_metadata(file, output_path)
        elif file.suffix.lower() in PDF_EXTENSIONS:
            clean_pdf_metadata(file, output_path)


if __name__ == "__main__":
    print("=" * 45)
    print("      METADATA CLEANER (Images & PDFs)     ")
    print("=" * 45)
    print("1. Process a Single File")
    print("2. Batch Process a Folder")
    choice = input("\nSelect an option (1 or 2): ").strip()

    if choice == "1":
        target = input("Enter path to file: ").strip("\"'")
        process_file(target)
    elif choice == "2":
        target = input("Enter path to directory: ").strip("\"'")
        process_directory(target)
    else:
        print("Invalid selection. Exiting.")


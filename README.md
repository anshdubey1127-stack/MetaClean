# Metadata Cleaner (Images & PDFs)

A lightweight Python tool that strips sensitive hidden metadata (EXIF data, GPS coordinates, author details, device models, and editing software) from images and PDF files without altering their visual contents.

---

## Features

- **Image Cleaning:** Removes EXIF, GPS location, camera details, and timestamps from `.jpg`, `.jpeg`, `.png`, `.bmp`, and `.webp` files
- **PDF Cleaning:** Clears standard document info dictionaries (Author, Title, Subject, Creator) and XMP metadata streams.
- **Batch Processing:** Clean an entire directory of files in one command.
- **Safe Outputs:** Generates a new file with `_cleaned` appended to the name, leaving your original files untouched.

---

## Tech Stack

- **Language:** Python 3.10+
- **Image Processing:** `Pillow`
- **PDF Processing:** `pikepdf`

---

## Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/anshdubey1127-stack/metadata-cleaner.git](https://github.com/anshdubey1127-stack/metadata-cleaner.git)
   cd metadata-cleaner

# Metadata Cleaner Drop Tool

A simple drag-and-drop utility that removes metadata from image files and creates a cleaned copy with `_clean` appended to the filename.

Designed for artists, photographers, AI image creators, and anyone who wants to remove embedded metadata before sharing images online.

## Features

* Drag-and-drop support (script or EXE)
* Creates a new file without modifying the original
* Preserves image content while rebuilding the file
* Automatically appends `_clean` to output filenames
* Supports:
  * JPG / JPEG
  * PNG
  * WEBP
  * BMP
  * TIFF
* Multiple metadata removal methods with automatic fallback:
  1. ImageMagick (`-strip`)
  2. FFmpeg (`-map_metadata -1`)
  3. Pillow BMP pixel round-trip
  4. Pillow pixel-only image rebuild
* Supports cleaning multiple files at once

## Why Multiple Cleaning Methods?

Modern images can contain metadata stored in many different ways, including:

* EXIF
* XMP
* IPTC
* ICC Profiles
* C2PA Content Credentials
* JUMBF Containers
* Application-Specific Metadata

Different tools remove different metadata structures. This utility attempts several cleaning methods automatically, starting with the most aggressive options available on your system.

## Usage

### Option 1: Python Script

Drag one or more image files onto:

```text
metadata_cleaner_drop_tool.py
```

### Option 2: Standalone EXE

Drag one or more image files onto:

```text
MetadataCleaner.exe
```

The cleaned image will be saved beside the original:

```text
photo.png
photo_clean.png
```

If a cleaned file already exists:

```text
photo_clean.png
photo_clean_2.png
photo_clean_3.png
```

## Optional Dependencies

The program works with Pillow alone, but better results are often achieved when additional tools are installed.

### ImageMagick

https://imagemagick.org/

Recommended because it can strip many metadata structures directly.

### FFmpeg

https://ffmpeg.org/

Provides an additional metadata-removal method and serves as a fallback if ImageMagick is unavailable.

## Building the EXE

Run:

```bat
build_exe.bat
```

The executable will be generated in:

```text
dist/MetadataCleaner.exe
```

## Notes

* The original image is never modified.
* Metadata removal results can vary depending on image format and embedded data structure.
* Some proprietary metadata formats may survive certain cleaning methods, which is why multiple fallback approaches are used.
* For best results, install ImageMagick and FFmpeg.

## License

MIT License

---

### GitHub Tagline

Drag-and-drop image metadata cleaner that removes EXIF and other embedded metadata using ImageMagick, FFmpeg, and pixel-rebuild fallbacks while preserving the original image.

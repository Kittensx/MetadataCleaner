Metadata Cleaner Drop Tool v2

This version is more aggressive than the first Pillow-only version.

What it does:
* Accepts drag-and-drop files.
* Creates a new file ending in _clean.
* Tries ImageMagick first if available.
* Tries FFmpeg second if available.
* Falls back to a Pillow raw pixel rebuild.
* Uses a BMP-style internal roundtrip as an extra metadata-destruction step.

Important:
Pillow alone may not remove C2PA/JUMBF data. For best results, install ImageMagick or FFmpeg.

Recommended install:
1. Install ImageMagick:
   https://imagemagick.org/script/download.php#windows

2. During install, enable:
   Add application directory to your system path

3. Optional: install FFmpeg and add it to PATH.

Build the EXE:
1. Extract this ZIP.
2. Open Command Prompt in the extracted folder.
3. Run:
   build_exe.bat

The EXE will appear here:
dist\MetadataCleaner.exe

Use:
Drag one or more images onto MetadataCleaner.exe.
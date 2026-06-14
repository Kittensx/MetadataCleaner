"""
Metadata Cleaner Drop Tool v2

Drag image files onto this script or onto the built EXE.

This version is more aggressive than a simple Pillow save:
1. Tries ImageMagick if installed.
2. Tries FFmpeg if installed.
3. Uses Pillow pixel-only rebuild.
4. Optionally round-trips through BMP-style raw pixels internally.

Clean files are saved beside the original with _clean added.
"""

from pathlib import Path
from PIL import Image
import shutil
import subprocess
import sys
import tempfile


SUPPORTED_EXTENSIONS = {
  ".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"
}


def run_command(cmd):
  try:
    result = subprocess.run(
      cmd,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
      text=True,
      check=False
    )
    return result.returncode == 0, result.stdout, result.stderr
  except Exception as exc:
    return False, "", str(exc)


def clean_with_imagemagick(input_path, output_path):
  magick = shutil.which("magick")
  if not magick:
    return False, "ImageMagick not found"

  ext = output_path.suffix.lower()

  if ext == ".png":
    cmd = [
      magick,
      str(input_path),
      "-alpha", "on",
      "-strip",
      "PNG32:" + str(output_path)
    ]
  elif ext in {".jpg", ".jpeg"}:
    cmd = [
      magick,
      str(input_path),
      "-strip",
      "-quality", "95",
      str(output_path)
    ]
  else:
    cmd = [
      magick,
      str(input_path),
      "-strip",
      str(output_path)
    ]

  ok, out, err = run_command(cmd)
  return ok and output_path.exists(), err or out


def clean_with_ffmpeg(input_path, output_path):
  ffmpeg = shutil.which("ffmpeg")
  if not ffmpeg:
    return False, "FFmpeg not found"

  ext = output_path.suffix.lower()

  if ext in {".jpg", ".jpeg"}:
    temp_output = output_path
    cmd = [
      ffmpeg,
      "-y",
      "-i", str(input_path),
      "-map_metadata", "-1",
      "-q:v", "2",
      str(temp_output)
    ]
  else:
    cmd = [
      ffmpeg,
      "-y",
      "-i", str(input_path),
      "-map_metadata", "-1",
      str(output_path)
    ]

  ok, out, err = run_command(cmd)
  return ok and output_path.exists(), err or out


def clean_with_pillow_pixel_rebuild(input_path, output_path):
  with Image.open(input_path) as img:
    img.load()

    ext = output_path.suffix.lower()

    if ext in {".jpg", ".jpeg"}:
      work = img.convert("RGB")
      clean = Image.new("RGB", work.size)
      clean.putdata(list(work.getdata()))
      clean.save(output_path, quality=95, optimize=True)

    elif ext == ".png":
      work = img.convert("RGBA")
      clean = Image.new("RGBA", work.size)
      clean.putdata(list(work.getdata()))
      clean.save(output_path, optimize=True)

    elif ext == ".webp":
      work = img.convert("RGBA")
      clean = Image.new("RGBA", work.size)
      clean.putdata(list(work.getdata()))
      clean.save(output_path, quality=95, method=6)

    else:
      work = img.convert("RGBA")
      clean = Image.new("RGBA", work.size)
      clean.putdata(list(work.getdata()))
      clean.save(output_path)

  return output_path.exists()


def clean_with_bmp_roundtrip(input_path, output_path):
  with tempfile.TemporaryDirectory() as temp_dir:
    temp_bmp = Path(temp_dir) / "pixel_only_temp.bmp"

    with Image.open(input_path) as img:
      img.load()
      work = img.convert("RGBA")
      clean = Image.new("RGBA", work.size)
      clean.putdata(list(work.getdata()))
      clean.save(temp_bmp)

    with Image.open(temp_bmp) as bmp:
      bmp.load()
      ext = output_path.suffix.lower()

      if ext in {".jpg", ".jpeg"}:
        final = bmp.convert("RGB")
        final.save(output_path, quality=95, optimize=True)
      elif ext == ".png":
        final = bmp.convert("RGBA")
        final.save(output_path, optimize=True)
      elif ext == ".webp":
        final = bmp.convert("RGBA")
        final.save(output_path, quality=95, method=6)
      else:
        final = bmp.convert("RGBA")
        final.save(output_path)

  return output_path.exists()


def unique_output_path(input_path):
  base = input_path.with_name(f"{input_path.stem}_clean{input_path.suffix}")
  if not base.exists():
    return base

  for i in range(2, 1000):
    candidate = input_path.with_name(f"{input_path.stem}_clean_{i}{input_path.suffix}")
    if not candidate.exists():
      return candidate

  raise RuntimeError("Too many clean output files already exist.")


def clean_image(input_path):
  input_path = Path(input_path)

  if not input_path.exists():
    raise FileNotFoundError(f"File not found: {input_path}")

  if input_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
    raise ValueError(f"Unsupported file type: {input_path.suffix}")

  output_path = unique_output_path(input_path)

  attempts = []

  ok, msg = clean_with_imagemagick(input_path, output_path)
  attempts.append(("ImageMagick", ok, msg))
  if ok:
    return output_path, attempts

  ok, msg = clean_with_ffmpeg(input_path, output_path)
  attempts.append(("FFmpeg", ok, msg))
  if ok:
    return output_path, attempts

  try:
    ok = clean_with_bmp_roundtrip(input_path, output_path)
    attempts.append(("Pillow BMP roundtrip", ok, ""))
    if ok:
      return output_path, attempts
  except Exception as exc:
    attempts.append(("Pillow BMP roundtrip", False, str(exc)))

  try:
    ok = clean_with_pillow_pixel_rebuild(input_path, output_path)
    attempts.append(("Pillow pixel rebuild", ok, ""))
    if ok:
      return output_path, attempts
  except Exception as exc:
    attempts.append(("Pillow pixel rebuild", False, str(exc)))

  details = "\n".join(f"{name}: {'OK' if ok else 'FAILED'} {msg}" for name, ok, msg in attempts)
  raise RuntimeError("All cleaning methods failed:\n" + details)


def main():
  if len(sys.argv) < 2:
    print("Drag one or more image files onto this script or EXE.")
    print("Supported: jpg, jpeg, png, webp, bmp, tif, tiff")
    print()
    print("Optional but recommended:")
    print("- Install ImageMagick and make sure magick.exe is on PATH.")
    print("- Install FFmpeg and make sure ffmpeg.exe is on PATH.")
    input("\nPress Enter to close...")
    return 0

  print("Metadata Cleaner v2")
  print("-------------------")

  failures = 0

  for arg in sys.argv[1:]:
    path = Path(arg)
    try:
      output, attempts = clean_image(path)
      print(f"\nCleaned: {path.name}")
      print(f"Output:  {output.name}")
      print("Methods tried:")
      for name, ok, msg in attempts:
        print(f"  - {name}: {'OK' if ok else 'skipped/failed'}")
    except Exception as exc:
      failures += 1
      print(f"\nFailed: {path.name}")
      print(exc)

  print("\nDone.")
  input("Press Enter to close...")
  return 1 if failures else 0


if __name__ == "__main__":
  raise SystemExit(main())
# Nokia 9110 Communicator Ringtone Fixer (`.rng`)

Tools for fixing and extracting valid Nokia `.rng` ringtones sent via Infrared (IrDA) directly from a **Nokia 9110 Communicator** to modern PCs or legacy machines. Written by Claude Pro on the basis of older, unpublished scripts by Gemini (modern) and Gemini+ChatGPT (legacy).

## The Problem

When sending a custom ringtone via Infrared (IrDA) directly from a Nokia 9110 Communicator to a PC or non-Communicator device, the transferred file contains proprietary Nokia wrapper header bytes prepended to the actual ringtone payload. As a result, Symbian phones newer than the Nokia 9210 Communicator flag the file as corrupt or unplayable.

To get a playable ringtone file directly off a Nokia 9110 **without using these scripts**, you *must* send it via IrDA to a **Nokia 9210 Communicator** specifically. The 9210 handles the proprietary stream correctly and allows saving a clean file. Without access to a Nokia 9210 Communicator or this cleanup logic, extracting a functional ringtone file directly onto a PC is, as far as I know, impossible.

## How It Works

The scripts process the raw files in **the folder the script itself is in** (not the folder you run it from). For each file, they search for the Nokia binary ringtone magic byte sequence (`\x02J:`), strip away the preceding wrapper data, and save a clean, playable `.rng` file next to the original.

* **Non-destructive:** Creates new `.rng` files and leaves the original transfer files untouched. An existing `.rng` file is never overwritten.
* **Smart filtering:** Only files without an extension (no `.` in the name) are considered, which also skips the scripts themselves and any `.rng` outputs. Files that are already clean, or that contain no ringtone payload, are skipped.

## Included Scripts

Both scripts do exactly the same thing; they differ only in which Python versions they run on.

| File                    | Compatible Python Versions | Target Environment                                             |
| ----------------------- | -------------------------- | -------------------------------------------------------------- |
| `convert_rng.py`        | Python 3.x, 2.6–2.7        | Modern OS (Windows, macOS, Linux)                              |
| `convert_rng_legacy.py` | Python 1.5.2–2.7           | Vintage laptops / retro PCs (Windows 95/98/2000, legacy Linux) |

`convert_rng_legacy.py` does **not** run on Python 3, and `convert_rng.py` does not run on Python 2.5 or older.

The scripts have been tested on Python 1.5.2, 2.0, 2.7 and 3.13 (on Linux).

## Usage Instructions

### 1. Python 3 (Modern Machines)

Place `convert_rng.py` in the folder containing your raw transferred files (received via IrDA, usually lacking a file extension).

Open a terminal or command prompt and run:

```bash
python convert_rng.py
```

The clean `.rng` files will be generated alongside your originals, named after the original with `.rng` added (for example `ringtone` → `ringtone.rng`).

### 2. Python 1.5–2.x / Vintage Hardware (IrDA Laptops)

`convert_rng_legacy.py` avoids every language feature newer than Python 1.5.2: no string methods, no `with` statements, no `True`/`False`, no `print()` function and no `str.format()`. This maximizes the chances of running natively on old laptops with IrDA ports running legacy operating systems and old Python versions.

Place `convert_rng_legacy.py` in the folder with your raw transfers.

Run via command line:

```bash
python convert_rng_legacy.py
```

### 3. Converting a Single File Interactively

Both scripts also provide a `convert_file(input_path, output_path)` function for converting one file from the Python prompt, with any input and output names you like:

```python
>>> import convert_rng          # or: import convert_rng_legacy
>>> convert_rng.convert_file('ringtone', 'my_tone.rng')
```

Unlike the folder mode, `convert_file` overwrites the output file if it already exists. If the input contains no ringtone, it raises `ValueError` and writes nothing.

### 4. Example

The file `Aleksille taikinaa` (a Finnish folk tune) is a real, unmodified transfer, sent via IrDA directly from a Nokia 9110 Communicator to a Windows XP laptop. As received, it is not a valid ringtone: Symbian phones (at least those other than the Nokia 9210 Communicator) cannot use it.

To try the scripts, put either `convert_rng.py` or `convert_rng_legacy.py` in the same folder as `Aleksille taikinaa` and run it. The script creates `Aleksille taikinaa.rng`, a clean ringtone file that plays normally.

## License

**MIT License** — feel free to modify, distribute, and integrate into retro-computing projects.

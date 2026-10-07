# Nokia 9110 Communicator ringtone fixer - legacy version
# Runs on Python 1.5.2 through 2.7. Does NOT run on Python 3
# (use convert_rng.py there).
# Written by Claude Pro on the basis of an older (unpublished) version by Gemini and ChatGPT.
#
# Converts raw ringtone files received via IrDA from a Nokia 9110
# Communicator into clean, playable .rng files by stripping the wrapper
# bytes in front of the ringtone payload.
#
# Compatibility notes (keep these when editing):
# - string.find() instead of str.find(): string methods only exist from 1.6
# - no 'with', True/False, sorted(), str.format() or print()
# - os.path.abspath() is not in 1.5/1.5.1, so a fallback is provided

import os
import sys
import string

# A Nokia binary ringtone (Smart Messaging) starts with these bytes
MAGIC = '\002J:'


def convert_9110_to_clean_rng(wrapped_data):
    pos = string.find(wrapped_data, MAGIC)

    if pos == -1:
        raise ValueError("Could not locate the raw Nokia ringtone payload.")

    # Keep everything from the magic bytes to the end of the data
    return wrapped_data[pos:]


def convert_file(input_path, output_path):
    """
    Converts a single file. Not used by process_folder(); meant for
    interactive use, e.g.:
        >>> import convert_rng_legacy
        >>> convert_rng_legacy.convert_file('ringtone', 'ringtone.rng')
    Raises ValueError (and writes nothing) if no ringtone is found.
    Overwrites output_path if it exists.
    """
    k = open(input_path, 'rb')
    try:
        data = k.read()
    finally:
        k.close()

    clean = convert_9110_to_clean_rng(data)

    k = open(output_path, 'wb')
    try:
        k.write(clean)
    finally:
        k.close()


def is_conversion_necessary(input_path):
    """
    Checks if the file needs conversion.
    Returns (1, clean_data) if it does, or (0, None) if it is
    already clean or contains no ringtone.
    """
    try:
        k = open(input_path, 'rb')
        try:
            original_data = k.read()
        finally:
            k.close()

        clean_data = convert_9110_to_clean_rng(original_data)

        # Only convert if the cleaned data actually differs from the original
        if clean_data != original_data:
            return 1, clean_data

    except ValueError:
        # Magic bytes not found; skip the file
        pass

    return 0, None


def absolute_path(path):
    if hasattr(os.path, 'abspath'):
        return os.path.abspath(path)
    return os.path.normpath(os.path.join(os.getcwd(), path))


def get_script_dir():
    try:
        script_path = __file__
    except NameError:
        # __file__ may be missing (very old versions, interactive use)
        if sys.argv and sys.argv[0]:
            script_path = sys.argv[0]
        else:
            return os.getcwd()
    return os.path.dirname(absolute_path(script_path))


def process_folder():
    # Process the folder this script is located in
    script_dir = get_script_dir()

    filenames = os.listdir(script_dir)
    filenames.sort()

    for filename in filenames:
        input_path = os.path.join(script_dir, filename)

        # Only look at files without an extension
        if os.path.isfile(input_path) and '.' not in filename:
            output_path = input_path + '.rng'

            # Never overwrite an existing .rng file
            if os.path.exists(output_path):
                print "Skipped (Target .rng file already exists): %s" % filename
                continue

            needed, clean_data = is_conversion_necessary(input_path)

            if needed:
                print "Converting: %s -> %s.rng" % (filename, filename)
                # Write a new .rng file; the original is left untouched
                k = open(output_path, 'wb')
                try:
                    k.write(clean_data)
                finally:
                    k.close()
            else:
                print "Skipped (Already clean or invalid): %s" % filename


if __name__ == '__main__':
    process_folder()

# Nokia 9110 Communicator ringtone fixer - modern version
# Runs on Python 3.x (and also on Python 2.6-2.7).
# Written by Claude Pro on the basis of an older (unpublished) version by Gemini.
#
# Converts raw ringtone files received via IrDA from a Nokia 9110
# Communicator into clean, playable .rng files by stripping the wrapper
# bytes in front of the ringtone payload.

import os

# A Nokia binary ringtone (Smart Messaging) starts with these bytes
MAGIC = b'\x02J:'


def convert_9110_to_clean_rng(wrapped_data):
    pos = wrapped_data.find(MAGIC)

    if pos == -1:
        raise ValueError("Could not locate the raw Nokia ringtone payload.")

    # Keep everything from the magic bytes to the end of the data
    return wrapped_data[pos:]


def convert_file(input_path, output_path):
    """
    Converts a single file. Not used by process_folder(); meant for
    interactive use, e.g.:
        >>> import convert_rng
        >>> convert_rng.convert_file('ringtone', 'ringtone.rng')
    Raises ValueError (and writes nothing) if no ringtone is found.
    Overwrites output_path if it exists.
    """
    with open(input_path, 'rb') as k:
        data = k.read()

    clean = convert_9110_to_clean_rng(data)

    with open(output_path, 'wb') as k:
        k.write(clean)


def is_conversion_necessary(input_path):
    """
    Checks if the file needs conversion.
    Returns (True, clean_data) if it does, or (False, None) if it is
    already clean or contains no ringtone.
    """
    try:
        with open(input_path, 'rb') as k:
            original_data = k.read()

        clean_data = convert_9110_to_clean_rng(original_data)

        # Only convert if the cleaned data actually differs from the original
        if clean_data != original_data:
            return True, clean_data
    except ValueError:
        # Magic bytes not found; skip the file
        pass

    return False, None


def process_folder():
    # Process the folder this script is located in
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for filename in sorted(os.listdir(script_dir)):
        input_path = os.path.join(script_dir, filename)

        # Only look at files without an extension
        if os.path.isfile(input_path) and '.' not in filename:
            output_path = input_path + '.rng'

            # Never overwrite an existing .rng file
            if os.path.exists(output_path):
                print("Skipped (Target .rng file already exists): {0}".format(filename))
                continue

            needed, clean_data = is_conversion_necessary(input_path)

            if needed:
                print("Converting: {0} -> {0}.rng".format(filename))
                # Write a new .rng file; the original is left untouched
                with open(output_path, 'wb') as k:
                    k.write(clean_data)
            else:
                print("Skipped (Already clean or invalid): {0}".format(filename))


if __name__ == '__main__':
    process_folder()

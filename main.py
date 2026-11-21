"""make.fun entry: The Poster for a Place That Isn't There (VELMORA).

Standard library only, no network. The poster image is committed next
to this file, so every run writes exactly the same bytes to
/output/entry.png (or $OUTPUT_DIR/entry.png when set, for local tests).
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    # /output is the harness location; OUTPUT_DIR only exists for
    # local testing. The gate requires a whole PNG/JPEG, 1024x1024,
    # at most 1,048,576 bytes -- entry.png already meets all three.
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()

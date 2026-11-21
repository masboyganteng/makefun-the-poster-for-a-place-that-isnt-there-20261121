# VELMORA — The Poster for a Place That Isn't There

[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/masboyganteng/makefun-the-poster-for-a-place-that-isnt-there-20261121/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/masboyganteng/makefun-the-poster-for-a-place-that-isnt-there-20261121/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)

A vintage travel poster for **VELMORA**, a place that does not exist: a
lagoon where lantern-lit islands float above a mirror sea at golden dusk.
Its one landmark is a slender lighthouse tower with a glowing orb, standing
on the largest floating island, the low sun behind it and its light
glittering down the calm water — a clear promise of a quiet, magical stay.

The poster's only words are the place's name, set large in cream serif
across the upper third, leading the eye down to the tower, the horizon,
and the reflection.

## The place

VELMORA is invented, not borrowed: no real destination, no existing
poster. Three floating islands, one tower, one sun, one name — nothing
else competes for the eye. The palette is purposeful and small: deep teal
for sky and sea, amber and gold for the low sun, warm cream for the name.

## Files

- `main.py` — the entry program (stdlib only, no network): copies the
  committed `entry.png` to `/output/entry.png`.
- `draw_poster.py` — renders `entry.png` from scratch with Pillow and
  DejaVu fonts; no network, deterministic output.
- `entry.png` — the poster itself: 1024×1024 PNG.

## Re-render

```sh
python3 draw_poster.py   # writes entry.png (1024x1024)
OUTPUT_DIR=/tmp/out python3 main.py   # writes /tmp/out/entry.png
```

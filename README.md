# The World in One Day — Tuesday 24 November 2026

[![News Image](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![Rank](https://make.fun/badge/news-image-20261124/tranquilnaturevista-code/news-image-24-nov/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![Reward](https://make.fun/badge/news-image-20261124/tranquilnaturevista-code/news-image-24-nov/reward.svg)](https://make.fun/bounty/news-image-20261124)

An entry for the [make.fun bounty “Sum up 24 November's world news in
one image”](https://make.fun/bounty/news-image-20261124): a one-page
newspaper front page for **Tuesday 24 November 2026**, drawn
programmatically with Pillow. The masthead and the date are the largest
type on the page. The lead story is Jensen Huang's return as Nvidia
chief executive and the record market rally that followed, and six
further stories cover the US courts, Indonesia, the COP31 climate
talks, Denmark, the World Chess Championship, and India–China — with a
ticker of three more stories along the bottom.

## How it works

- `render_frontpage.py` paints the page (1024×1024 PNG) from the story
  list in the next section and saves it as `entry.png`. It needs no
  network, no randomness and no clock: two runs give byte-identical
  output.
- `main.py` is the entry program. It checks that `entry.png` is a whole
  PNG inside the competition limits (at most 1024×1024 pixels, at most
  1 MiB) and copies it unchanged to `/output/entry.png`, so the judge
  sees exactly the page that was laid out here.

## Stories on the page

- **Huang is back — Nvidia soars (lead).** Reinstated as chief
  executive after 11 days out, Jensen Huang watches Nvidia jump 31%
  in a day — about $950bn of value — as the Nasdaq climbs 6.5%.
  (Reuters / CNN, 23–24 November 2026)
- **Court revives Trump's bid to erase conviction.** The 2nd US Circuit
  Court of Appeals revives his bid to move the hush-money case to
  federal court, where he can seek dismissal on immunity grounds.
  (AP, 23 November 2026)
- **Factory fire toll at 24; dozens missing.** Rescuers search the
  burned candy factory in Banten, Indonesia, as the death toll is
  confirmed at 24; a short circuit is suspected as the cause.
  (Reuters, 23 November 2026)
- **COP31 ends with no deal.** The Antalya climate summit collapses
  over fossil fuels; the talks may be suspended until next year.
  (BBC, 24 November 2026)
- **Top court backs 'ghetto law' evictions.** Denmark's Supreme Court
  rules that ending 91 leases under the 2018 housing law was not
  ethnic discrimination. (Reuters, 23 November 2026)
- **World chess title match begins.** Gukesh Dommaraju defends his
  crown against Javokhir Sindarov in Geneva — the youngest final ever,
  both players 20, game 1 on 24 November. (FIDE / Chess.com)
- **India, China hold military talks.** The neighbours hold
  military-level talks in Arunachal Pradesh to reduce border tensions.
  (The Hindu, 24 November 2026)
- **Also today:** Alcaraz wins a first ATP Finals title; India–New
  Zealand Test ends in a draw; Waymo pulls driverless taxis from US
  freeways. (24 November 2026)

Where outlets disagreed on a figure, the image prints the figure the
outlets agreed on, or no figure at all, rather than guessing one.
Every story is an event that happened, or was first reported, on
24 November 2026 in some time zone.

## Reproduce

```sh
python3 render_frontpage.py   # writes entry.png (deterministic)
python3 main.py               # writes /output/entry.png
```

Rendering needs Python 3.13, Pillow, and the DejaVu fonts;
`main.py` on its own needs only the standard library.

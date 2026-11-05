# Aisyn Bekali — personal portfolio

**Student:** Aisyn Bekali · **Group:** SE-2517  
Endterm Assignment: Full Interactive Website

## Run

Open `index.html` in a modern browser for an offline preview. All illustrations,
Bootstrap 5.3.3, and jQuery 3.7.1 are bundled locally. No build, npm installation,
API key, account, or internet connection is required.

For development and consistent localStorage behavior, run from this folder:

```sh
python3 -m http.server 8000
```

Then open `http://localhost:8000` in your browser. Stop the server with Ctrl+C.

## Pages

- `index.html`: introduction, selected concepts, links to the journal.
- `projects.html`: category filters, saved projects, project detail modals.
- `about.html`: student introduction and the technologies used in this website.
- `journal.html`: five learning reflections with jQuery slide animations.
- `contact.html`: accessible client-side form validation and a local confirmation.

## Criteria map

| Criterion | Evidence |
| --- | --- |
| Structure & pages (15%) | Five separate HTML pages with header, nav, main, footer |
| Consistent design (5%) | Shared custom stylesheet, colors, typography, navigation |
| Responsive layout (10%) | Desktop 1440px, tablet 768px, mobile 390px screenshots and checks |
| Bootstrap Grid (5%) | `container`, `row`, `col-lg-6`, `col-md-6 col-lg-4`, `col-md-4` |
| JavaScript (10%) | Filtering, localStorage favorites, validation, character counter |
| jQuery animation (10%) | Journal panels use `slideDown` / `slideUp`; reduced-motion support |
| Interactive component (10%) | Bootstrap project modal; collapsible mobile menu |
| Defense (30%) | `docs/DEFENSE_RU.md`; student must personally demonstrate and explain |
| Report (5%) | Word report with screenshots, tasks, implementation and process summary |

## Implementation

`assets/css/style.css` contains the visual system and media queries.
`assets/js/main.js` contains all site behavior and explanatory comments.
`assets/images/` contains original SVG illustrations, not external photo links.
`assets/vendor/` contains the unchanged third-party libraries. See THIRD_PARTY.md.

Saved project IDs use `aisyn-portfolio-saved-v1` in localStorage. They can be
removed with the heart buttons or by clearing the site's browser storage. If
storage is unavailable or malformed, the site continues to work in memory.
No contact messages or personal form values are persisted or transmitted.

The three projects are explicitly labeled original **concept studies**. They
are not claims of completed client work, external live projects, or employment.
The contact form is intentionally a front-end demo, not a mail service.

## Validation

The browser checks are optional development tools; they are not needed to run
or submit the site. With Python Playwright and `/usr/bin/chromium` available,
start the local server and run:

```sh
python3 tests/browser_check.py
node --check assets/js/main.js
```

The script checks all five pages at three widths, local resources, mobile
navigation, filtering, persistence, empty states, the modal, focus restoration,
jQuery expansion/collapse, reduced motion, and invalid/valid form submissions.
It writes real screenshots to `screenshots/` and results to
`docs/test-results.json`. A failure raises an assertion and exits nonzero.

## Submission

Submit the project ZIP and the Word report before the LMS deadline. The report
is available as `.doc` and `.docx`. Read the source and rehearse the defense;
the prepared files do not replace the in-person assessment. Review all personal
wording and follow your institution's disclosure rules for assistance.

"""Generate the submission report after running tests/browser_check.py.
Requires python-docx and Pillow. Conversion to .doc uses LibreOffice separately.
"""
from pathlib import Path
import json
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'submission';OUT.mkdir(exist_ok=True)
results=json.loads((ROOT/'docs/test-results.json').read_text())
doc=Document()
from datetime import datetime, timezone
doc.core_properties.author='Aisyn Bekali'
doc.core_properties.title='Endterm Assignment — Personal Portfolio'
doc.core_properties.subject='SE-2517 — Interactive Website'
doc.core_properties.created=datetime(2026,11,5,tzinfo=timezone.utc)
doc.core_properties.modified=datetime(2026,11,5,tzinfo=timezone.utc)
sec=doc.sections[0];sec.top_margin=Inches(.65);sec.bottom_margin=Inches(.65);sec.left_margin=Inches(.8);sec.right_margin=Inches(.8)
normal=doc.styles['Normal'];normal.font.name='Calibri';normal.font.size=Pt(10);normal.paragraph_format.space_after=Pt(7)
for name in ['Title','Heading 1','Heading 2']:
 doc.styles[name].font.color.rgb=RGBColor.from_string('263C30')
footer=sec.footer.paragraphs[0];footer.text='AISYN BEKALI  /  SE-2517                                         ENDTERM  ·  PERSONAL PORTFOLIO';footer.style='Caption'
def para(text):doc.add_paragraph(text)
def title(text):doc.add_heading(text,1)
def pic(name,caption,max_h=6.8):
 path=ROOT/'screenshots'/name
 w,h=Image.open(path).size
 width=min(6.6,max_h*w/h)
 par=doc.add_paragraph();par.alignment=WD_ALIGN_PARAGRAPH.CENTER;par.add_run().add_picture(str(path),width=Inches(width))
 cap=doc.add_paragraph(caption,style='Caption');cap.alignment=WD_ALIGN_PARAGRAPH.CENTER
def new(title_text):doc.add_page_break();title(title_text)
doc.add_paragraph('FULL INTERACTIVE WEBSITE',style='Subtitle')
doc.add_heading('Personal portfolio\nAisyn Bekali',0)
para('Endterm Assignment Report')
para('Student: Aisyn Bekali\nGroup: SE-2517')
para('Project: A five-page personal portfolio exploring web design, front-end development, and learning through creative exercises.')
pic('index-desktop.png','Home page — actual Chromium screenshot.',4.6)
para('Stack: HTML5 · CSS3 · Bootstrap 5.3.3 · JavaScript · jQuery 3.7.1')
new('Part 1 — Project purpose and criteria')
para('Task: create a fully functional multi-page interactive website using the technologies covered in the course. The selected topic is a personal portfolio. It contains five separate pages connected by a consistent navigation bar and footer.')
para('The portfolio presents three clearly labeled interface concepts, not commercial commissions. The contact form demonstrates local validation and does not send email. These boundaries are visible in the interface.')
table=doc.add_table(rows=1, cols=3);table.style='Light Shading Accent 1'
for c,t in zip(table.rows[0].cells,['Criterion','Weight','Implementation / evidence']):c.text=t
rows=[('Structure & pages','15%','Home, Projects, About, Journal, Contact; each has header/main/footer.'),('Design consistency','5%','Shared cream/green/terracotta palette, typography, navigation and CSS.'),('Responsive layout','10%','All pages checked at 1440, 768 and 390 CSS pixels.'),('Bootstrap Grid','5%','container/row with col-lg-6, col-md-6 col-lg-4, col-md-4.'),('JavaScript','10%','Filters, saved projects, modal content, form validation, character count.'),('jQuery effects','10%','Journal notes expand/collapse using slideDown and slideUp.'),('Interactive component','10%','Bootstrap modal windows and collapsible mobile navigation.'),('Practice defense','30%','Prepared demonstration guide; in-person defense remains required.'),('Report','5%','This report: page screenshots, task explanations, tests and process.')]
for row in rows:
 for c,t in zip(table.add_row().cells,row):c.text=t
para('Project organization: root HTML pages; assets/css/style.css; assets/js/main.js; assets/images/ for original SVG artwork; assets/vendor/ for local libraries; tests/ for browser checks; screenshots/ for visual evidence; docs/ for results and defense notes.')
para('Running the project: open index.html directly, or run “python3 -m http.server 8000” from the project folder. No package installation, build, credentials, or internet connection is required for the website.')
for number,name,label,explanation in [
 (2,'index','Home','Task: introduce the student and provide clear entry points. The hero uses a two-column Bootstrap row at large widths and stacks on smaller screens. Original SVG artwork reinforces the design theme. Three project cards open detail modals, and the call-to-action links to the journal.'),
 (3,'projects','Projects','Task: present topic-specific content with JavaScript interaction. Three original concept cards can be filtered by category or saved state. The heart buttons persist project IDs in localStorage. Each card opens a Bootstrap modal with its design decision and learning focus.'),
 (4,'about','About','Task: provide personal context and explain the toolkit. The page identifies Aisyn Bekali and group SE-2517. It describes the learning purpose without claiming employment or client experience. A responsive three-column section summarizes the technologies actually used.'),
 (5,'journal','Journal','Task: implement a jQuery effect. Five notes explain structure, responsive layout, interaction feedback, motion and forms. Each heading is a real button connected to its panel with aria-controls. jQuery animates the panel while aria-expanded tracks its state.'),
 (6,'contact','Contact','Task: implement an interactive form with validation. Required fields include name, email, topic, message and acknowledgment. Invalid inputs receive field-specific feedback. Successful validation shows a local confirmation and resets the form. No message is transmitted or stored.')]:
 new(f'Part {number} — {label} page');para(explanation);pic(f'{name}-desktop.png',f'Figure {number-1}. {label} page at a 1440-pixel desktop viewport.',6.8)
new('Part 7 — Responsive layout and Bootstrap Grid')
para('Task: support desktop, tablet and mobile. The custom stylesheet works with Bootstrap’s 12-column grid. Project cards use col-md-6 col-lg-4: one column below 768px, two from 768px, and three from 992px. The hero uses col-lg-6 to split the large-screen layout evenly. Navigation collapses below the md breakpoint.')
para('Automated checks opened all five pages at 1440px, 768px and 390px and confirmed no horizontal overflow. A 2px mobile overflow caused by the interaction between the Bootstrap gutter and custom container padding was found and corrected. Full-resolution screenshots for all 15 page/viewport combinations are included in screenshots/.')
pic('projects-tablet.png','Figure 6. Tablet: the project grid switches to two columns.',3.8)
pic('contact-mobile.png','Figure 7. Mobile: stacked contact content and form, with collapsed navigation.',3.1)
new('Part 8 — JavaScript and interactive components')
para('Task: demonstrate dynamic functionality and a working interactive component. Data attributes identify projects and categories. Filtering updates card visibility, the result count, active button styling and aria-pressed. A Set holds unique saved IDs, and JSON serializes them for localStorage. A guarded read/write prevents storage errors from breaking the interface.')
para('Bootstrap handles modal visibility, Escape and focus trapping. JavaScript inserts the selected concept’s title, description, illustration and explanation using textContent. After closing, focus returns to the button that opened the modal.')
pic('project-modal.png','Figure 8. Open project detail modal with original concept illustration.',4.2)
para('The browser tests verified category counts, the saved empty state, save/reload persistence, removal from Saved, correct modal content and keyboard focus restoration. The interface also provides a back-to-top button for longer pages.')
new('Part 9 — jQuery effects and accessibility')
para('Task: use at least one jQuery effect correctly. Journal buttons use a jQuery click handler. The chosen panel animates with slideDown when opened and slideUp when closed. stop(true, true) finishes queued motion before the next action. The aria-expanded state and plus/minus indicator update with the panel.')
pic('journal-expanded.png','Figure 9. Expanded journal note after the jQuery slide animation.',4.8)
para('Accessibility measures include a skip link, semantic landmarks, visible keyboard focus, form labels and error associations, descriptive image alternatives, live result/status messages, and active navigation indicators. Reduced-motion preference sets jQuery animation duration to zero and disables CSS transitions. These measures were checked in Chromium; a full assistive-technology audit was not performed.')
new('Part 10 — Form validation')
para('Task: validate inputs and communicate outcomes clearly. HTML constraints provide required fields, email type, and length limits. JavaScript trims name/message values so whitespace-only entries fail, calls checkValidity, focuses the first invalid control and maintains aria-invalid. The character counter reflects the message length.')
pic('contact-invalid.png','Figure 10. Empty submission: field-specific validation feedback.',3.5)
pic('contact-success.png','Figure 11. Valid sample input: local confirmation, no email sent or data stored.',3.5)
new('Part 11 — Verification and work process')
para(f'Automated result: {results["passed"]} checks passed; {results["failed"]} failed. The test log is included as docs/test-results.json. This is a count of assertions, including repeated resource checks, rather than a count of independent test scenarios.')
para('Environment: Chromium driven by Python Playwright. Website served by Python’s local HTTP server. JavaScript syntax was also checked using node --check assets/js/main.js.')
for text in ['All five pages: successful HTTP response, one h1, active navigation, loaded images and no overflow at three viewport widths.','Functional checks: mobile menu navigation; category filtering; saved-project persistence and empty state; modal content, Escape close and focus return.','jQuery checks: expand, collapse and reduced-motion expansion.','Form checks: empty submission, whitespace-only fields, invalid email, missing acknowledgment, valid confirmation and reset.','Resource checks: internal navigation links, scripts, stylesheets and images return success; no browser JavaScript or HTTP errors were recorded.']:
 doc.add_paragraph(text,style='List Bullet')
para('Work process summary')
for text in ['Mapped the assignment criteria to five page roles and selected a consistent portfolio identity.','Created semantic page layouts and original vector illustrations, then applied Bootstrap grids and a shared custom stylesheet.','Implemented JavaScript filters, browser-local favorites, detail modals, form validation and jQuery journal panels.','Tested desktop, tablet and mobile layouts, corrected the mobile gutter overflow, and synchronized tests with modal transitions.','Captured the actual browser states, wrote the report and defense guide, and packaged the project with local dependencies and licenses.']:
 doc.add_paragraph(text,style='List Number')
para('Limitations and next steps: only Chromium was exercised, and no backend is included. Future work could add real completed projects, cross-browser testing and a server-side contact service. The saved setup instructions were prepared for future cloud sessions; this does not establish publication or a fresh-session restore.')
new('Part 12 — Defense and submission')
para('The 30% defense criterion requires the student to present and explain the work personally. The files cannot complete this assessment. The Russian-language guide in docs/DEFENSE_RU.md includes a demonstration sequence and likely instructor questions.')
for text in ['Explain the choice of portfolio topic, five-page structure and visual identity.','Show Bootstrap breakpoint classes and demonstrate the layout at desktop, tablet and mobile widths.','Demonstrate filtering, save/reload, modal interaction, jQuery animation and invalid/valid form input.','Explain event listeners, data attributes, Set, localStorage, JSON, checkValidity, textContent and reduced-motion support.','Identify the project’s limits honestly: concept studies, local form demo and no mail service.']:
 doc.add_paragraph(text,style='List Bullet')
para('Submission checklist: upload the Word report and project ZIP before the deadline specified in LMS; check the extracted project locally; review the personal wording; rehearse the defense. A DOC file and an editable DOCX are provided. Full screenshots are included separately in the project folder.')
para('Sources and attribution')
para('Assignment source: “Endterm Assignment (2).pdf”, provided by the user. Bootstrap 5.3.3: getbootstrap.com; jQuery 3.7.1: jquery.com. Both libraries and the included Popper code use the MIT license; full notices are supplied under assets/vendor/. Illustrations and site-specific layout/code were created for this portfolio. System fonts are used.')
para('Preparation note: the implementation and documentation were prepared with AI assistance. The student should review, understand and adapt the work, disclose assistance where required, and present only what they can explain during the individual defense.')
doc.save(OUT/'Aisyn_Bekali_SE-2517_Report.docx')
print(OUT/'Aisyn_Bekali_SE-2517_Report.docx')

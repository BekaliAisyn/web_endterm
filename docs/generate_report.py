"""Create a plain Word report from the existing website screenshots.
Run from the project folder: python3 docs/generate_report.py
Requires python-docx and Pillow.
"""
from pathlib import Path
from datetime import datetime, timezone
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'submission'
OUT.mkdir(exist_ok=True)
doc = Document()
doc.core_properties.author = 'Aisyn Bekali'
doc.core_properties.title = 'Endterm Assignment Report'
doc.core_properties.subject = 'Personal Portfolio — SE-2517'
doc.core_properties.created = datetime(2026, 11, 5, tzinfo=timezone.utc)
doc.core_properties.modified = datetime(2026, 11, 6, tzinfo=timezone.utc)
section = doc.sections[0]
section.page_width = Inches(8.27)
section.page_height = Inches(11.69)
section.top_margin = section.bottom_margin = Inches(.75)
section.left_margin = section.right_margin = Inches(.85)
normal = doc.styles['Normal']
normal.font.name = 'Times New Roman'
normal.font.size = Pt(12)
normal.font.color.rgb = RGBColor(0, 0, 0)
normal.paragraph_format.line_spacing = 1.15
normal.paragraph_format.space_after = Pt(8)

# Use only ordinary paragraphs: no cover design, colored headings, tables or footer.
def para(text, bold=False):
    p = doc.add_paragraph()
    p.add_run(text).bold = bold
    return p

def part(title, task, text, new_page=True):
    if new_page:
        doc.add_page_break()
    para(title, bold=True)
    para('Task: ' + task)
    para(text)

def screenshot(filename, caption, max_height=6.4):
    path = ROOT / 'screenshots' / filename
    width, height = Image.open(path).size
    picture_width = min(6.5, max_height * width / height)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.add_run().add_picture(str(path), width=Inches(picture_width))
    para(caption)

para('Endterm Assignment Report', bold=True)
para('Student: Aisyn Bekali\nGroup: SE-2517\nTopic: Personal Portfolio Website')
para('Introduction', bold=True)
para('This assignment is a personal portfolio website. It introduces the student, presents three design concepts, shares learning notes and includes a contact form. The website has five pages: Home, Projects, About, Journal and Contact.')
para('The website uses HTML, CSS, Bootstrap, JavaScript and jQuery. All pages have the same logo, navigation menu, colors, fonts and footer. Bootstrap and jQuery are stored in the project folder, so the website can work without an internet connection.')
part('Part 1. Home page', 'Create the main page and connect it to the other pages.',
     'The Home page introduces Aisyn Bekali and the purpose of the portfolio. It contains an illustration, buttons leading to Projects and About, three project cards and a link to the Journal page. The navigation menu is available at the top of every page.', new_page=False)
screenshot('index-desktop.png', 'Screenshot 1. Home page.', 5.1)

part('Part 2. Projects page', 'Display projects and add interactive features.',
     'The Projects page contains three original design concepts: Room to Grow, Small Notes and Steppe Atlas. The filter buttons show all projects, web design projects, UI projects or saved projects. Clicking a heart saves a project. Saved project IDs are kept in localStorage, so they remain after the page is refreshed. The cards are labeled as concepts.')
screenshot('projects-desktop.png', 'Screenshot 2. Projects page.')

part('Part 3. About page', 'Add information about the student and the tools used.',
     'The About page shows the student name, Aisyn Bekali, and group SE-2517. It describes the purpose of the portfolio and the learning process. Three cards explain how HTML, CSS, Bootstrap, JavaScript and jQuery are used in the website.')
screenshot('about-desktop.png', 'Screenshot 3. About page.')

part('Part 4. Journal page', 'Create learning notes with a jQuery animation.',
     'The Journal page contains five short notes about building the website. Clicking a note opens its text with the jQuery slideDown effect. Clicking again closes it with slideUp. The plus sign changes to a minus sign when a note is open. The animation is disabled when the browser requests reduced motion.')
screenshot('journal-expanded.png', 'Screenshot 4. Journal page with an open note.')

part('Part 5. Contact page', 'Create a contact form with clear input fields.',
     'The Contact page includes fields for a name, email address, topic and message. It also has a checkbox explaining that this is a demonstration form. A counter shows the number of characters in the message. The form checks the input in the browser; it does not send an email or store the message.')
screenshot('contact-desktop.png', 'Screenshot 5. Contact page.')

part('Part 6. Responsive layout', 'Make the website work on desktop, tablet and mobile screens.',
     'Bootstrap containers, rows and columns organize the layout. The project cards use col-md-6 and col-lg-4: one card per row on small screens, two on tablets and three on larger screens. The Home page uses col-lg-6 for two columns on desktop. On mobile, the content is stacked and the navigation becomes a menu button. Custom CSS controls spacing, fonts, colors and buttons.')
para('All five pages were checked at widths of 1440, 768 and 390 pixels. The content fits the screen without horizontal scrolling.')
comparison = doc.add_paragraph()
comparison.alignment = WD_ALIGN_PARAGRAPH.CENTER
for filename in ['projects-tablet.png', 'contact-mobile.png']:
    comparison.add_run().add_picture(str(ROOT / 'screenshots' / filename), height=Inches(5.8))
    comparison.add_run('  ')
para('Screenshots 6–7. Projects on a tablet (left) and Contact on mobile (right).')

part('Part 7. Project modal', 'Show project details in an interactive window.',
     'Clicking a project image or title opens a Bootstrap modal. JavaScript adds the selected project title, image, description and design explanation. The user can close the window with the close button or the Escape key. After closing, keyboard focus returns to the project button.')
screenshot('project-modal.png', 'Screenshot 8. Project details in a modal window.', 5.4)

part('Part 8. Form validation', 'Check the form and show useful feedback.',
     'JavaScript checks that the name has at least two characters, the email has a valid format, a topic is selected and the message has at least twenty characters. Spaces alone are not accepted as a name or message. The checkbox must also be selected. If a field is invalid, an error appears below it. If the input is valid, a confirmation appears and the form is cleared.')
screenshot('contact-invalid.png', 'Screenshot 9. Error messages after an empty submission.', 3.5)
screenshot('contact-success.png', 'Screenshot 10. Confirmation after valid sample input.', 3.5)

part('Part 9. Testing and work summary', 'Check the website and summarize the development process.',
     'The pages were tested in Chromium. Navigation links, images, filters, saved projects, modal windows, journal animations and form validation were checked. The mobile menu was also tested. The automated checks completed successfully, with no JavaScript errors recorded.')
para('Work process', bold=True)
para('First, the website was divided into five pages. The shared navigation, footer and page structure were created with HTML. Bootstrap was used for the grid, and custom CSS was added for the appearance and responsive layout.')
para('Next, JavaScript was added for project filters, saved projects, modal content and form validation. jQuery was used to animate the journal notes. After that, the pages were tested on different screen sizes. The mobile spacing was adjusted so the content fitted correctly.')
para('Finally, screenshots were taken and the project files were organized. The result is a five-page personal portfolio with responsive layouts and working interactive features.')
para('How to run the website', bold=True)
para('Extract the project ZIP and open index.html in a browser. For local development, run python3 -m http.server 8000 in the project folder and open http://localhost:8000.')

doc.save(OUT / 'Aisyn_Bekali_SE-2517_Report.docx')
print(OUT / 'Aisyn_Bekali_SE-2517_Report.docx')

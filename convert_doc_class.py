from pylatex import Document, Figure
from pylatex.basic import NewPage, Package
from pylatex.headfoot import Command
from pylatex.position import FlushLeft, FlushRight, Center
from pylatex.section import Section, Subsection, \
    Paragraph, Subsubsection, Subparagraph
from pylatex.utils import NoEscape
import os


class ConLatexDocument:
    def __init__(self, doc_sett):
        font_size = doc_sett[
            'font_size'] if 'font_size' in doc_sett.keys() else '12'
        doc_type = doc_sett["type"] if 'type' in doc_sett.keys() else 'article'
        geom = {"top": "2.0", "left": "2.5",
                "bottom": "2.0", "right": "1.0"}
        if 'geom' in doc_sett.keys():
            if isinstance(doc_sett['geom'], dict):
                tmp = {'top', 'left', 'bottom', 'right'}
                if (tmp & set(doc_sett['geom'])) == tmp:
                    geom = doc_sett['geom']

        self.doc = Document('doc_1', documentclass=f'{doc_type}',
                            document_options=['a4paper', f'{font_size}pt'])
        self.doc.packages.append(Package("geometry"))
        self.doc.packages.add(Package('fontenc', options=['T1']))
        self.doc.packages.add(Package('inputenc', options=['utf8']))
        self.doc.packages.add(Package('babel', options=['english', 'russian']))
        self.doc.packages.append(Package("amsmath"))
        self.doc.packages.append(Package("amsthm"))
        self.doc.packages.append(Package("amssymb"))
        self.doc.packages.append(Package("fancyhdr"))
        self.doc.packages.append(Package("setspace"))
        self.doc.packages.append(Package("graphicx"))
        self.doc.packages.append(Package("colortbl"))
        self.doc.packages.append(Package("color"))
        self.doc.packages.append(Package("tikz"))
        self.doc.packages.append(Package("pgf"))
        self.doc.packages.append(Package("subcaption"))
        self.doc.packages.append(Package("listings"))
        self.doc.packages.append(Package("indentfirst"))
        self.doc.packages.append(Package("mathtools"))
        self.doc.packages.append(Package("booktabs"))
        self.doc.packages.append(Package("tablefootnote"))
        self.doc.packages.append(Package("chngcntr"))
        self.doc.packages.add(Package('tocvsec2'))

        self.doc.preamble.append(
            NoEscape(r'\geometry{left=%s' % geom['left'] + 'cm}'))
        self.doc.preamble.append(
            NoEscape(r'\geometry{right=%s' % geom['right'] + 'cm}'))
        self.doc.preamble.append(
            NoEscape(r'\geometry{top=%s' % geom['top'] + 'cm}'))
        self.doc.preamble.append(
            NoEscape(r'\geometry{bottom=%s' % geom['bottom'] + 'cm}'))
        self.doc.preamble.append(NoEscape(r'\setlength{\parindent}{1.25cm}'))

    def center_page_title(self, info):
        self.doc.append(NoEscape(r'\vspace*{\fill}'))
        for i in info['text']:
            self.doc.append(Section(title=i, numbering=False))
        self.doc.append(NoEscape(r'\vfill'))

    def make_title(self, info):
        po = {'R': FlushRight(), 'L': FlushLeft(), 'C': Center()}
        with self.doc.create(po[info['pos']]) as el:
            el.append(Section(info['text'], numbering=True))

    def make_subtitle(self, info):
        po = {'R': FlushRight(), 'L': FlushLeft(), 'C': Center()}
        with self.doc.create(po[info['pos']]) as el:
            el.append(NoEscape(r'\vspace{-2\baselineskip}'))
            el.append(NoEscape(r'\item'))
            el.append(Subsection(info['text'], numbering=True))

    def make_subsubtitle(self, info):
        po = {'R': FlushRight(), 'L': FlushLeft(), 'C': Center()}
        with self.doc.create(po[info['pos']]) as el:
            el.append(NoEscape(r'\vspace{-2\baselineskip}'))
            el.append(NoEscape(r'\item'))
            el.append(Subsubsection(info['text'], numbering=True))

    def add_paragraph(self, info):
        po = {'R': FlushRight(), 'L': FlushLeft(), 'C': Center()}
        with self.doc.create(po[info['pos']]) as el:
            el.append(NoEscape(r'\vspace{-2\baselineskip}'))
            el.append(NoEscape(r'\item'))
            el.append(Paragraph(info['text'], numbering=True))

    def make_table(self):
        self.doc.append(NoEscape(r'{\tableofcontents}'))

    def make_numeration_style(self, info):
        places = {'HL': r'\lhead{\thepage}', 'HC': r'\chead{\thepage}',
                  'HR': r'\rhead{\thepage}', 'LL': r'\lfoot{\thepage}',
                  'LC': r'\cfoot{\thepage}', 'LR': r'\rfoot{\thepage}'}
        if info['num_place'] in places.keys():
            self.doc.preamble.append(NoEscape(r'\pagestyle{fancy}'))
            self.doc.preamble.append(NoEscape(r'\fancyhf{}'))
            self.doc.preamble.append(
                NoEscape(r'%s' % places[info['num_place']]))
            self.doc.preamble.append(
                NoEscape(r'\renewcommand{\headrulewidth}{0pt}'))

    def add_text(self, info):
        po = {'R': FlushRight(), 'L': FlushLeft(), 'C': Center()}
        with self.doc.create(po[info['pos']]) as el:
            el.append(info['text'])

    def set_page_counter(self, info):
        page_number = str(int(info['text']) - 1)
        self.doc.append(NoEscape(r'\setcounter{page}{%s}' % page_number))

    def add_number_of_pages(self, info):
        po = {'R': FlushRight(), 'L': FlushLeft(), 'C': Center()}
        with self.doc.create(po[info['pos']]) as el:
            el.append(NoEscape(r'\vspace{-2\baselineskip}'))
            el.append(NoEscape(r'\item'))
            el.append(NoEscape(r'\pageref{LastPage}'))

    def make_new_page(self):
        self.doc.append(NewPage())

    def skip_numbering(self):
        self.doc.append(NoEscape(r'\thispagestyle{empty}'))

    def gen_doc(self, user_id, user_folder_path):
        for i in self.doc.packages:
            if str(i) == "Package(Arguments('lmodern'), Options())":
                self.doc.packages.remove(i)
                break

        us_tex_path = os.path.join(user_folder_path, "pdf_files")
        self.doc.generate_tex(os.path.join(us_tex_path, f'{user_id}'))
        self.doc.generate_pdf(os.path.join(us_tex_path, f'{user_id}'),
                              clean_tex=False)

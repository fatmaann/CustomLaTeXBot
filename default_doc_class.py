from pylatex import Document, Figure
from pylatex.section import Section, Subsection, Subsubsection
from pylatex.utils import NoEscape
from pylatex.basic import NewPage, Package
from pylatex.headfoot import Command
from pylatex.position import Center, MiniPage, FlushRight
from pylatex.table import Table, Tabular
import os


class DefLatexDocument:
    def __init__(self):
        self.doc = Document('doc_1', documentclass='article',
                            document_options=['a4paper', '12pt'])
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
        self.doc.packages.append(Package('rotating'))
        self.doc.packages.append(Package("indentfirst"))
        self.doc.packages.append(Package("mathtools"))
        self.doc.packages.append(Package("booktabs"))
        self.doc.packages.append(Package("tablefootnote"))
        self.doc.packages.append(Package("chngcntr"))

        hyperref_options = {
            'colorlinks': True, 'citecolor': 'blue', 'linkcolor': 'black',
            'bookmarks': False, 'hypertexnames': True, 'urlcolor': 'blue'
        }
        self.doc.packages.add(Package('hyperref', options=hyperref_options))
        self.doc.preamble.append(
            Command('counterwithin', arguments=['table', 'section']))
        self.doc.preamble.append(NoEscape(r'\geometry{left=2.5cm}'))
        self.doc.preamble.append(NoEscape(r'\geometry{right=1.0cm}'))
        self.doc.preamble.append(NoEscape(r'\geometry{top=2.0cm}'))
        self.doc.preamble.append(NoEscape(r'\geometry{bottom=2.0cm}'))
        self.doc.preamble.append(NoEscape(r'\setlength{\parindent}{1.25cm}'))
        self.doc.preamble.append(
            NoEscape(r'\renewcommand{\baselinestretch}{1.5}'))
        self.pre_info_dict = dict()

    def make_pre_title(self, info):
        self.pre_info_dict['uni_name'] = r'' + info['uni_name']['text'].replace(
            "\n", "\\\\")
        self.pre_info_dict['faculty_name'] = info['faculty_name']['text']
        self.pre_info_dict['edu_prog_name'] = info['edu_prog_name']['text']
        self.pre_info_dict['agreed_name'] = info['agreed_name']['text']
        self.pre_info_dict['agreed_title'] = r'' + info['agreed_title'][
            'text'].replace("\n",
                            "\\\\")
        self.pre_info_dict['approved_name'] = info['approved_name']['text']
        self.pre_info_dict['approved_title'] = r'' + info['approved_title'][
            'text'].replace("\n",
                            "\\\\")
        self.pre_info_dict['performer_name'] = info['performer_name']['text']
        self.pre_info_dict['performer_group'] = info['performer_group']['text']
        self.pre_info_dict['country_code'] = info['country_code']['text']
        self.pre_info_dict['uni_code'] = info['uni_code']['text']
        self.pre_info_dict['doc_year'] = info['doc_year']['text']
        self.pre_info_dict['project_code'] = info['project_code']
        self.pre_info_dict['project_class_code'] = info['project_class_code']
        self.pre_info_dict['format_short_name'] = info['format_short_name']
        self.pre_info_dict['doc_unique_code'] = ''

    def center_page_title(self, info):
        self.pre_info_dict['file_name'] = info['name']
        self.pre_info_dict['project_name'] = r'' + info['text'].replace("\n",
                                                                        "\\\\ ")
        self.define_doc_code()
        self.define_toppage_numbering()
        self.set_page_counter()

        with self.doc.create(Center()) as center:
            center.append(
                Subsection(title=NoEscape(
                    r'\textbf{' + self.pre_info_dict['uni_name'] + '}'),
                    numbering=False))
            center.append(NoEscape(
                r'\textbf{' + self.pre_info_dict['faculty_name'] + r'\\' +
                self.pre_info_dict['edu_prog_name'] + '}'))

        with self.doc.create(Figure(position='ht')) as fig:
            with fig.create(MiniPage(width=r"0.35\textheight")) as minipage_0_1:
                with minipage_0_1.create(Center()) as page_center:
                    page_center.append(NoEscape(
                        r'\textbf{СОГЛАСОВАНО}\\' + self.pre_info_dict[
                            'agreed_title'] + r'\\'))
                    page_center.append(NoEscape(
                        r'\makebox[3cm][c] {\hrulefill}' + self.pre_info_dict[
                            'agreed_name'] + r'\\'))
                    page_center.append(NoEscape(
                        r'«\makebox[1cm][c] {\hrulefill}» \makebox[3cm][c] {\hrulefill}' +
                        self.pre_info_dict['doc_year'] + ' г.'))

            with fig.create(MiniPage(width=r"0.35\textheight")) as minipage_0_1:
                with minipage_0_1.create(Center()) as page_center:
                    page_center.append(NoEscape(
                        r'\textbf{УТВЕРЖДАЮ}\\' + self.pre_info_dict[
                            'approved_title'] + r'\\'))
                    page_center.append(NoEscape(
                        r'\makebox[3cm][c] {\hrulefill}' + self.pre_info_dict[
                            'approved_name'] + r'\\'))
                    page_center.append(NoEscape(
                        r'«\makebox[1cm][c] {\hrulefill}» \makebox[3cm][c] {\hrulefill}' +
                        self.pre_info_dict['doc_year'] + ' г.'))

        self.doc.append(NoEscape(r'\vspace*{\fill}'))

        with self.doc.create(Table(position='htbp')) as table_one:
            with table_one.create(
                    MiniPage(width=r"0.01\textwidth")) as minipage_1_1:
                minipage_1_1.append(NoEscape(r'\hspace*{-2cm}'))
                minipage_1_1.append(NoEscape(r'\rotatebox{90}{'))
                with minipage_1_1.create(Tabular('|c|c|c|c|c|')) as tabular:
                    tabular.add_hline()
                    tabular.add_row(
                        ['Инв. № подл.', 'Подпись и дата', 'Взам. инв. №',
                         'Инв. № дубл.', 'Подпись и дата'])
                    tabular.add_hline()
                    tabular.add_row([NoEscape('{  }') for i in range(5)])
                    tabular.add_hline()
                minipage_1_1.append(NoEscape(r'}'))
                minipage_1_1.append(NoEscape(r'\vspace*{-2cm}'))
            with table_one.create(
                    MiniPage(width=r"0.99\textwidth")) as minipage_1_2:
                minipage_1_2.append(NoEscape(r'\vspace*{-3cm}'))
                with minipage_1_2.create(Center()) as center:
                    center.append(
                        Section(title=NoEscape(
                            self.pre_info_dict['project_name'].upper()),
                            numbering=False))
                    center.append(NoEscape(r'\vspace*{0cm}'))
                    center.append(NoEscape(
                        r'\textbf{' + self.pre_info_dict['file_name'] + '}'))
                    center.append(
                        Section(title='ЛИСТ УТВЕРЖДЕНИЯ', numbering=False))
                    center.append(
                        Section(
                            title=self.pre_info_dict['doc_unique_code'] + '-ЛУ',
                            numbering=False))
                    center.append(
                        NoEscape(r'\textbf{Листов \pageref{LastPage} }'))

                with minipage_1_2.create(FlushRight()) as right:
                    right.append(NoEscape(r'\vspace*{3cm}'))
                    with right.create(
                            MiniPage(width=r"0.3\textheight")) as minipage_0_2:
                        with minipage_0_2.create(Center()) as center_2:
                            center_2.append(NoEscape(
                                r'\textbf{Исполнитель}\\' + self.pre_info_dict[
                                    'performer_group'] + r'\\'))
                            center_2.append(NoEscape(
                                r'\makebox[3cm][c] {\hrulefill}' +
                                self.pre_info_dict['performer_name'] + r'\\'))
                            center_2.append(NoEscape(
                                r'«\makebox[1cm][c] {\hrulefill}» \makebox[3cm][c] {\hrulefill}' +
                                self.pre_info_dict['doc_year'] + ' г.'))
                minipage_1_2.append(NoEscape(r'\vfill'))

        self.add_year_text()
        self.skip_numbering()
        self.make_new_page()
        self.add_approved_text(info['approve'])
        with self.doc.create(Table(position='htbp')) as table_two:
            with table_two.create(
                    MiniPage(width=r"0.01\textwidth")) as minipage_2_1:
                minipage_2_1.append(NoEscape(r'\hspace*{-2cm}'))
                minipage_2_1.append(NoEscape(r'\rotatebox{90}{'))
                with minipage_2_1.create(Tabular('|c|c|c|c|c|')) as tabular:
                    tabular.add_hline()
                    tabular.add_row(
                        ['Инв. № подл.', 'Подпись и дата', 'Взам. инв. №',
                         'Инв. № дубл.', 'Подпись и дата'])
                    tabular.add_hline()
                    tabular.add_row([NoEscape('{  }') for i in range(5)])
                    tabular.add_hline()
                minipage_2_1.append(NoEscape(r'}'))
                minipage_2_1.append(NoEscape(r'\vspace*{-2cm}'))
            with table_two.create(
                    MiniPage(width=r"0.99\textwidth")) as minipage_2_2:
                minipage_2_2.append(NoEscape(r'\vspace*{-14cm}'))
                with minipage_2_2.create(Center()) as center:
                    center.append(
                        Section(title=NoEscape(
                            self.pre_info_dict['project_name'].upper()),
                            numbering=False))
                    center.append(NoEscape(r'\vspace*{1cm}'))
                    center.append(
                        Subsection(title=self.pre_info_dict['file_name'],
                                   numbering=False))
                    center.append(
                        Section(title=self.pre_info_dict['doc_unique_code'],
                                numbering=False))
                    center.append(
                        NoEscape(r'\textbf{Листов \pageref{LastPage} }'))
                minipage_2_2.append(NoEscape(r'\vfill'))
        self.add_year_text()

    def define_doc_code(self):
        self.pre_info_dict[
            'doc_unique_code'] = f'{self.pre_info_dict["country_code"]}.{self.pre_info_dict["uni_code"]}.' \
                                 f'{self.pre_info_dict["project_code"]}.' \
                                 f'{self.pre_info_dict["project_class_code"]}-01 ' \
                                 f'{self.pre_info_dict["format_short_name"]} 01-1'
        self.pre_info_dict['doc_unique_code'] = self.pre_info_dict[
            "doc_unique_code"].upper()

    def make_title(self, info):
        self.doc.append(Section(info['text'].upper()))

    def make_subtitle(self, info):
        self.doc.append(Subsection(info['text'].upper()))

    def make_subsubtitle(self, info):
        self.doc.append(Subsubsection(info['text'].upper()))

    def make_table(self):
        self.doc.append(NoEscape(r'{\tableofcontents}'))

    def set_page_counter(self):
        self.doc.append(NoEscape(r'\setcounter{page}{0}'))

    def add_text(self, info):
        for el in info['text'].split('\n'):
            text = r'\indent ' + el
            self.doc.append(NoEscape(text))
            self.doc.append(NoEscape(r'\newline'))

    def add_year_text(self):
        po = {'C': Center()}
        with self.doc.create(po['C']) as center:
            center.append(
                NoEscape(r'\textbf{' + self.pre_info_dict["doc_year"] + '}'))

    def add_approved_text(self, approve_text):
        self.doc.append(
            Subsection(
                title=f'{approve_text}\n{self.pre_info_dict["doc_unique_code"]}-ЛУ',
                numbering=False))
        self.doc.append(NoEscape(r'\vspace*{\fill}%'))

    def define_toppage_numbering(self):
        self.doc.preamble.append(NoEscape(r'\fancypagestyle{toppage}{'))
        self.doc.preamble.append(NoEscape(r'\fancyhf{}'))
        self.doc.preamble.append(
            NoEscape(r'\renewcommand{\headrulewidth}{0pt}'))
        appr = r'\fancyhead[C]{\thepage\\ \textbf{' + self.pre_info_dict[
            "doc_unique_code"] + '} }}'
        self.doc.preamble.append(NoEscape(appr))
        self.doc.preamble.append(NoEscape(r'\pagestyle{toppage}'))

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

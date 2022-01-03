import os
import datetime
from io import BytesIO

from reportlab.pdfgen import canvas

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Paragraph
from reportlab.platypus import Table, TableStyle

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from logging import *


class PDFReport():
    def __init__(self, subject_file: str, targets: list, scores: tuple,
                 out_file: str = None, out_dir: str = '.') -> None:

        # print(targets)

        self.subject_file = subject_file

        self.targets = [target for target in targets]

        self.target_pairs = self.get_target_pairs(self.targets, pair_len=3)

        self.target_files = [target[0] for target in self.targets]

        self.target_scores = [target[1] for target in self.targets]

        self.num_pages = int(1 + np.ceil(len(self.target_files) / 3))

        self.language = self.get_language(self.subject_file)

        # Create dataframe of target files and target scores
        self.df = pd.DataFrame(
            {
                'Target File': self.target_files,
                'Similarity Score': self.target_scores
            }
        )

        # print(self.df)

        # self.avg_similarity = np.mean(self.target_scores) * 100
        # self.max_similarity = max(self.target_scores) * 100
        self.avg_similarity = scores[0] * 100
        self.max_similarity = scores[1] * 100

        self.index_range = str([0.0, 1.0])

        self.date = datetime.datetime.now().strftime("%d-%b-%Y")
        self.time = datetime.datetime.now().strftime("%r")

        self.out_file = out_file
        self.out_dir = out_dir
        self.done = False

    def get_target_pairs(self, target: list, pair_len: int) -> list:
        pairs, files = [], []

        for i in range(len(target)):
            if (i % pair_len == 0) and (i != 0):
                pairs.append(files)
                files = []

            files.append(target[i])

        if len(files) > 0:
            pairs.append(files)

        return pairs

    def get_language(self, file_name: str) -> str:
        if file_name.endswith('.py'):
            return 'Python'
        elif file_name.endswith('.java'):
            return 'Java'
        elif file_name.endswith('.c'):
            return 'C'
        elif file_name.endswith('.cpp'):
            return 'C++'
        elif file_name.endswith('.cs'):
            return 'C#'
        elif file_name.endswith('.js'):
            return 'JavaScript'
        elif file_name.endswith('.rb'):
            return 'Ruby'
        elif file_name.endswith('.swift'):
            return 'Swift'
        elif file_name.endswith('.sh'):
            return 'Shell'
        elif file_name.endswith('.bat'):
            return 'Batch'
        else:
            return 'Unknown'

    def generate_report(self):
        # Set file_name as source file name if None specified
        file_name = self.subject_file.split(
            '.')[0] + '.pdf' if not self.out_file else self.out_file

        file_name = os.path.join(self.out_dir, file_name)
        warning("Creating PDF report: {}".format(file_name))

        # Create a new PDF canvas with Reportlab
        pdf = canvas.Canvas(file_name, pagesize=A4)

        # Define the page margins
        pdf.setPageRotation(0)
        pdf.setPageTransition(None, None, 0, 0)

        # Set the font style, size and color
        # pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))
        font_size = 12
        pdf.setFont('Helvetica', font_size)
        pdf.setFillColor(colors.black)

        # Set title
        documentTitle = "Report"
        pdf.setTitle(documentTitle)

        # Set author
        pdf.setAuthor("CSC - Code Similarity Check")

        # Save state
        pdf.saveState()

        # Create the header
        self.create_header(pdf, font_size)
        pdf.restoreState()

        # Create the content
        pdf.saveState()
        self.create_content(pdf)
        pdf.restoreState()

        # Create the footer
        pdf.saveState()
        self.create_footer(pdf, 1)
        pdf.restoreState()

        # Add plot
        pdf.saveState()
        self.create_plot(pdf)
        pdf.restoreState()

        # Add table on next page
        pdf.showPage()

        fc = 1
        for i, target_pair in enumerate(self.target_pairs):
            # Start new page
            pdf.saveState()
            self.create_header(pdf, font_size)
            pdf.restoreState()

            pdf.saveState()
            for j, target in enumerate(target_pair):
                self.create_table(
                    pdf,
                    file_no=fc,
                    data=target,
                    x_offset=100,
                    y_offset=520 - (j * 220)
                )
                fc += 1

            pdf.restoreState()

            pdf.saveState()
            self.create_footer(pdf, i + 2)
            pdf.restoreState()

            # Close the PDF file
            pdf.showPage()

        pdf.save()
        self.done = True

    def create_content(self, pdf: canvas):
        # Create the content
        pdf.setFont('Helvetica', 12)
        pdf.drawString(50, 690, "Date: ")
        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawString(50 + 40, 690, "{}".format(self.date))

        pdf.setFont('Helvetica', 12)
        pdf.drawString(425, 690, "Time: ")
        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawString(425 + 45, 690, "{}".format(self.time))

        pdf.setFont('Helvetica', 12)
        pdf.drawString(50, 660, "Subject File: ")
        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawString(50 + 80, 660, "{}".format(self.subject_file))

        pdf.setFont('Helvetica', 12)
        pdf.drawString(425, 660, "Language: ")
        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawString(425 + 72, 660, "{}".format(self.language))

        pdf.setFont('Helvetica', 12)
        pdf.drawString(50, 640, "Target Files: ")
        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawString(50 + 80, 640, "{}".format(len(self.target_files)))

        pdf.setFont('Helvetica', 12)
        pdf.drawString(50, 610, "Avg. Similarity: ")
        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawString(
            50 + 95, 610, "{}%".format(round(self.avg_similarity, 2)))

        pdf.setFont('Helvetica', 12)
        pdf.drawString(50, 590, "Max. Similarity: ")
        pdf.setFont('Helvetica-Bold', 12)
        pdf.drawString(
            50 + 95, 590, "{}%".format(round(self.max_similarity, 2)))

    def create_table(self, pdf: canvas, file_no: int, data: list, x_offset: int, y_offset: int):
        # # Create the table

        nodes_pairs = self.get_target_pairs(target=data[2], pair_len=2)
        data[2] = [' with '.join(pair) for pair in nodes_pairs]

        nodes = ', '.join(data[2][:-1]) + ' and ' + data[2][-1]

        target = data[0]
        index = str(data[1])

        description = """The subject file was compared with
                        <b>{}</b> nodes <i>({})</i> of
                        the target file and was found
                        <b>{}%</b> similar.
                        """.format(len(nodes_pairs), nodes, round(data[1] * 100, 2))

        paragraph = Paragraph(description)

        data = [["Index", "Description"], [index, paragraph]]

        # Create the table
        table = Table(data, colWidths=[
            80, 315], rowHeights=[40, 100], repeatRows=5, ident=0.5)

        table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('BOX', (0, 0), (-1, -1), 0.25, colors.grey),
            ('BACKGROUND', (0, 0), (-1, 0), "#f2f2f2"),
            ('BACKGROUND', (0, 1), (-1, 1), "#f2f2ff"),
        ]))

        # File title
        file_title = Paragraph(
            "Target File {}:\t<b>{}</b>".format(file_no, target))

        file_title.wrapOn(pdf, 400, 40)
        file_title.drawOn(pdf, x_offset, y_offset + 150)

        # Draw the table
        table.wrapOn(pdf, 600, 400)
        table.drawOn(pdf, x_offset, y_offset)

    def create_plot(self, pdf: canvas):
        # Set size
        # size = np.where(self.df['Similarity Score'] >= 0.5, 40, 20)

        # sort the dataframe by similarity score
        self.df = self.df.sort_values(by='Similarity Score', ascending=False)

        group_a = self.df[self.df['Similarity Score'] < 0.5]
        group_b = self.df[self.df['Similarity Score'] >= 0.5]
        group_b = group_b[group_b['Similarity Score'] < 0.75]
        group_c = self.df[self.df['Similarity Score'] >= 0.75]

        y_range_c = np.arange(len(group_c))
        y_range_b = np.arange(len(group_c), len(group_c) + len(group_b))
        y_range_a = np.arange(len(group_c) + len(group_b),
                              len(group_c) + len(group_b) + len(group_a))

        y_range = np.arange(len(self.df['Target File']))

        plt.grid(True, axis='x', linestyle='dotted', color='0.8')

        # # Create the plot
        # fig = plt.figure(figsize=(10, 10))
        # ax = fig.add_subplot(111)

        # Add the data of group a
        plt.hlines(
            y=y_range_a,
            xmin=0.0,
            xmax=group_a['Similarity Score'],
            colors='deepskyblue',
            alpha=0.5,
        )

        plt.scatter(
            group_a['Similarity Score'],
            y_range_a,
            color='deepskyblue',
            s=20,
            alpha=1.0,
            linewidths=0.5,
            zorder=10,
            label='0.0 - 0.5'
        )

        # Add the data of group b
        plt.hlines(
            y=y_range_b,
            xmin=0.0,
            xmax=group_b['Similarity Score'],
            colors='orange',
            alpha=0.5,
        )

        plt.scatter(
            group_b['Similarity Score'],
            y_range_b,
            color='orange',
            s=30,
            alpha=1.0,
            linewidths=0.5,
            zorder=10,
            label='0.5 - 0.75'
        )

        # Add the data of group c
        plt.hlines(
            y=y_range_c,
            xmin=0.0,
            xmax=group_c['Similarity Score'],
            colors='red',
            alpha=0.5,
        )

        plt.scatter(
            group_c['Similarity Score'],
            y_range_c,
            color='red',
            s=40,
            alpha=1.0,
            linewidths=0.5,
            zorder=10,
            label='0.75 - 1.0'
        )

        # Add labels
        plt.legend(loc='upper right')

        plt.yticks(
            y_range,
            self.df['Target File'],
            fontsize=6,
            rotation=45
        )

        plt.xticks(
            np.arange(0, 1.1, 0.1),
            fontsize=6
        )

        plt.title('Similarity Index Plot', loc='center',
                  fontsize=10, fontweight='bold')
        plt.xlabel('Index Value (0.0 - 1.0)', fontsize=8, fontweight='bold')
        plt.ylabel('Target File (File Name)', fontsize=9, fontweight='bold')

        # Set background color of axis
        ax = plt.gca()
        ax.set_facecolor('#f2f2ff')

        # # Set background color of plot
        # fig = plt.gcf()

        # Set height and width of the page
        fig = plt.gcf()
        fig.set_facecolor('#f2f2f2')

        if self.df.shape[0] < 6:
            fig.set_size_inches(5.1, 3.0)

        else:
            fig.set_size_inches(5.1, 6.0)

        plt.close()

        # Add the plot to the PDF
        imgdata = BytesIO()

        fig.savefig(imgdata, format='svg', dpi=300,
                    bbox_inches='tight', pad_inches=0.1)

        imgdata.seek(0)

        svg_img = svg2rlg(imgdata)

        renderPDF.draw(svg_img, pdf, 50, 60)

        # close the file
        imgdata.close()

        # clear the buffer
        plt.clf()

    def create_header(self, pdf: canvas, font_size: int):
        # define title and subtitle
        title = "CODE SIMILARITY CHECKER"
        subTitle = "REPORT"

        path = os.path.join(os.getcwd(), 'img')
        # Create the header

        pdf.drawImage(
            os.path.join(path, 'csc_logo.png'),
            50, 745,
            width=50, height=50
        )

        pdf.setFont('Times-Bold', font_size * 1.3)
        pdf.drawCentredString(297.5, 770, title)
        pdf.setFont('Times-Bold', font_size * 0.9)
        pdf.drawCentredString(297.5, 755, subTitle)

        pdf.drawImage(
            os.path.join(path, 'nu_logo.jpg'),
            495, 745,
            width=50, height=50
        )

    def create_footer(self, pdf: canvas, pg_num: int):
        # Create the footer
        pdf.setFont('Times-Bold', 10)
        pdf.setFillColor(colors.black)
        pdf.drawString(
            50,
            26,
            "Code Similarity Checker {} 2022".format(chr(0xa9))
        )

        pdf.setFont('Times-Roman', 10)
        page_info = "Page {} of {}".format(pg_num, self.num_pages)

        pdf.drawString(
            A4[0] - (50 + pdf.stringWidth(page_info, 'Times-Roman', 10)),
            26,
            page_info
        )

import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def create_report():
    doc = Document()

    # Page Margins: 1 inch top/bottom/right, 1.25 inch left (standard academic thesis binding)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.0)

        # Formal Academic Page Border (Single 1.5pt crisp box border around every page)
        pgBorders_xml = f"""<w:pgBorders {nsdecls('w')} w:offsetFrom="page">
            <w:top w:val="single" w:sz="12" w:space="24" w:color="000000"/>
            <w:left w:val="single" w:sz="12" w:space="24" w:color="000000"/>
            <w:bottom w:val="single" w:sz="12" w:space="24" w:color="000000"/>
            <w:right w:val="single" w:sz="12" w:space="24" w:color="000000"/>
        </w:pgBorders>"""
        section._sectPr.append(parse_xml(pgBorders_xml))

    # Styles Setup
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    img_dir = r"C:\Users\HP\.gemini\antigravity\scratch\activity-2\extracted_images"
    jain_logo = os.path.join(img_dir, "p1_img1_475x86.jpeg")

    # Helper functions
    def add_p(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, bold=False, italic=False, size=12, space_before=0, space_after=6, color=RGBColor(0, 0, 0)):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size)
        run.font.color.rgb = color
        return p

    def add_h1(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h2(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_h3(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(title)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_bullet(text, bold_prefix="", level=0):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.bold = True
            r_pre.font.name = 'Times New Roman'
            r_pre.font.size = Pt(12)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        return p

    def add_image_figure(filename, caption, width=Inches(5.0)):
        path = os.path.join(img_dir, filename)
        if os.path.exists(path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            run = p_img.add_run()
            run.add_picture(path, width=width)
            
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)
            p_cap.paragraph_format.keep_with_next = True
            r_cap = p_cap.add_run(caption)
            r_cap.bold = True
            r_cap.font.name = 'Times New Roman'
            r_cap.font.size = Pt(10.5)
            r_cap.font.color.rgb = RGBColor(51, 65, 85)

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color="D3D3D3"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="single" w:sz="6" w:space="0" w:color="475569"/>
                <w:bottom w:val="single" w:sz="6" w:space="0" w:color="475569"/>
                <w:left w:val="none"/>
                <w:right w:val="none"/>
                <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr.append(borders)

    def create_table(headers, rows_data, col_widths=None):
        table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table)

        # Header
        hdr_cells = table.rows[0].cells
        for i, title in enumerate(headers):
            hdr_cells[i].text = title
            set_cell_background(hdr_cells[i], "0F172A")
            set_cell_margins(hdr_cells[i], 120, 120, 140, 140)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(10)
            p.runs[0].font.bold = True
            p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

        # Rows
        for r_idx, row_values in enumerate(rows_data):
            row_cells = table.rows[r_idx + 1].cells
            bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
            for c_idx, val in enumerate(row_values):
                row_cells[c_idx].text = str(val)
                set_cell_background(row_cells[c_idx], bg_color)
                set_cell_margins(row_cells[c_idx], 80, 80, 120, 120)
                p = row_cells[c_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                p.paragraph_format.line_spacing = 1.05
                p.paragraph_format.space_after = Pt(0)
                if len(p.runs) > 0:
                    p.runs[0].font.name = 'Times New Roman'
                    p.runs[0].font.size = Pt(9.5)
                    p.runs[0].font.color.rgb = RGBColor(15, 23, 42)

        if col_widths:
            for row in table.rows:
                for idx, width in enumerate(col_widths):
                    row.cells[idx].width = Inches(width)

        doc.add_paragraph().paragraph_format.space_after = Pt(6)
        return table

    def add_code_block(code_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.05
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.25)
        set_cell_background(cell, "F1F5F9")
        set_cell_margins(cell, 100, 100, 140, 140)
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="4" w:color="CBD5E1"/><w:bottom w:val="single" w:sz="4" w:color="CBD5E1"/><w:left w:val="single" w:sz="12" w:color="0284C7"/><w:right w:val="single" w:sz="4" w:color="CBD5E1"/></w:tcBorders>')
        tcPr.append(borders)
        
        cp = cell.paragraphs[0]
        cp.paragraph_format.space_after = Pt(0)
        cp.paragraph_format.line_spacing = 1.0
        crun = cp.add_run(code_text.strip())
        crun.font.name = 'Consolas'
        crun.font.size = Pt(8.5)
        crun.font.color.rgb = RGBColor(15, 23, 42)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    print("Framework initialized. Generating document pages...")

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    if os.path.exists(jain_logo):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(10)
        p_logo.paragraph_format.space_after = Pt(14)
        run_logo = p_logo.add_run()
        run_logo.add_picture(jain_logo, width=Inches(3.8))

    add_p("JAIN (Deemed-to-be University)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, space_after=3)
    add_p("Department of Computer Science and Information Technology", align=WD_ALIGN_PARAGRAPH.CENTER, bold=False, size=12, space_after=2)
    add_p("M.Sc. Full Stack Development", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=24)

    add_p("MINI PROJECT REPORT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_after=6)
    add_p("on", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=12, space_after=6)
    add_p("“0/1 Knapsack Problem - Dynamic Programming”", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=16, space_after=28, color=RGBColor(15, 23, 42))

    add_p("Submitted in partial fulfilment of the requirements for the award of the degree of", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=11, space_after=2)
    add_p("Master of Science in Full Stack Development", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=36)

    add_p("Submitted by", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=11, space_after=4)
    add_p("Roshni Priyadarshini Behera", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=2)
    add_p("USN: 25MSFDR009", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11.5, space_after=40)

    add_p("Under the guidance of", align=WD_ALIGN_PARAGRAPH.CENTER, italic=True, size=11, space_after=2)
    add_p("DR. M N NACHAPPA", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=24)

    add_p("Academic Year: 2026-27", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=12, space_after=0)
    doc.add_page_break()

    # =========================================================================
    # PAGE 2: CERTIFICATE
    # =========================================================================
    if os.path.exists(jain_logo):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(6)
        p_logo.paragraph_format.space_after = Pt(8)
        run_logo = p_logo.add_run()
        run_logo.add_picture(jain_logo, width=Inches(3.2))

    add_p("Department of Computer Science & Information Technology", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=13, space_after=2)
    add_p("Programme: Master of Science in Full Stack Development [MSc-FSD]", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=11, space_after=36)

    p_cert = doc.add_paragraph()
    p_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert.paragraph_format.space_after = Pt(28)
    r_cert = p_cert.add_run("Certificate")
    r_cert.font.name = 'Brush Script MT'
    r_cert.font.size = Pt(36)
    r_cert.font.bold = True
    r_cert.font.color.rgb = RGBColor(15, 23, 42)

    cert_text = (
        "This is to certify that Ms. Roshni Priyadarshini Behera, bearing USN: 25MSFDR009, "
        "has satisfactorily completed the course of Activity-2 prescribed by JAIN (Deemed-to-be University) "
        "for the Master of Science in Full Stack Development (M.Sc-FSD) degree course in the academic year 2025 - 2026."
    )
    add_p(cert_text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, size=12, space_after=20)

    add_p("USN: 25MSFDR009", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=12, space_after=4)
    add_p("Date: 05/11/2026", align=WD_ALIGN_PARAGRAPH.LEFT, bold=True, size=12, space_after=90)

    t_sig = doc.add_table(rows=1, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sig.cell(0, 0).width = Inches(3.1)
    t_sig.cell(0, 1).width = Inches(3.1)
    
    p_s1 = t_sig.cell(0, 0).paragraphs[0]
    p_s1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = p_s1.add_run("Signature of Student\n(Roshni Priyadarshini Behera)")
    r1.font.bold = True
    r1.font.size = Pt(11)

    p_s2 = t_sig.cell(0, 1).paragraphs[0]
    p_s2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r2 = p_s2.add_run("Signature of Faculty Incharge\n(DR. M N NACHAPPA)")
    r2.font.bold = True
    r2.font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: DECLARATION
    # =========================================================================
    add_p("DECLARATION", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, space_before=10, space_after=24)
    
    dec_text1 = (
        "I hereby declare that the mini project entitled \"0/1 Knapsack Problem - Dynamic Programming\" "
        "is my original work carried out under the guidance of DR. M N NACHAPPA, in partial fulfilment of the "
        "requirements for the award of the degree of Master of Science in Full Stack Development."
    )
    add_p(dec_text1, space_after=14)

    dec_text2 = (
        "I confirm that all sources, tools, libraries, datasets and other materials used in the project have been "
        "properly acknowledged. This work has not been submitted, in whole or in part, for the award of any other "
        "degree or qualification."
    )
    add_p(dec_text2, space_after=60)

    add_p("Student Name: Roshni Priyadarshini Behera", bold=True, space_after=3)
    add_p("USN: 25MSFDR009", bold=True, space_after=3)
    add_p("Course: M.Sc. Full Stack Development", bold=True, space_after=3)
    add_p("Signature: __________________________", bold=True, space_after=3)
    add_p("Date: 05/11/2026", bold=True, space_after=0)

    p_num3 = doc.add_paragraph()
    p_num3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num3.paragraph_format.space_before = Pt(80)
    p_num3.add_run("iii").font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: ACKNOWLEDGEMENT
    # =========================================================================
    add_p("ACKNOWLEDGEMENT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, space_before=10, space_after=24)

    ack_text1 = (
        "I would like to express my sincere gratitude to my project guide, DR. M N NACHAPPA, "
        "for the guidance, patient feedback and encouragement given to me throughout this mini project. "
        "The suggestions received at each stage helped me to improve both the system and this report."
    )
    add_p(ack_text1, space_after=12)

    ack_text2 = (
        "I thank the Head of the Department and the faculty members of the Department of Computer Science and "
        "Information Technology, JAIN (Deemed-to-be University), for providing the facilities and the academic "
        "environment needed to complete this work."
    )
    add_p(ack_text2, space_after=12)

    ack_text3 = (
        "I also thank the maintainers of the public dataset and of the open source libraries used in this project. "
        "Their work made it possible to build, test and deploy the system without any licensing cost."
    )
    add_p(ack_text3, space_after=12)

    ack_text4 = (
        "Finally, I thank my family and friends for their constant support and encouragement during the preparation of this project."
    )
    add_p(ack_text4, space_after=50)

    add_p("Roshni Priyadarshini Behera", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, space_after=2)
    add_p("USN: 25MSFDR009", align=WD_ALIGN_PARAGRAPH.RIGHT, bold=True, space_after=2)
    add_p("M.Sc. Full Stack Development", align=WD_ALIGN_PARAGRAPH.RIGHT, italic=True, space_after=0)

    p_num4 = doc.add_paragraph()
    p_num4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num4.paragraph_format.space_before = Pt(80)
    p_num4.add_run("iv").font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: ABSTRACT
    # =========================================================================
    add_p("ABSTRACT", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, space_before=10, space_after=24)

    abs_p1 = (
        "Spam messages waste time and can mislead readers, which makes automatic filtering of text messages and email an "
        "important problem in message security. Spam filtering is an application of supervised binary classification of text data, "
        "a task of predictive data analysis. The aim of the project is to analyse a real-world labelled dataset, build a classification "
        "model and evaluate performance on unseen data."
    )
    add_p(abs_p1, space_after=12)

    abs_p2 = (
        "A public dataset of 59,241 labelled messages from SMS, chat and email sources was cleaned by removing conflicting "
        "labels, duplicates and overlap between the original splits, leaving 54,831 messages. A stratified 70/15/15 split produced "
        "training, validation and test sets with no shared text. Text was converted into 50,000 TF-IDF features, and Logistic Regression "
        "with balanced class weights was selected over a Multinomial Naive Bayes baseline using validation results. Evaluation used "
        "accuracy, precision, recall, F1-score and a confusion matrix. The classifier was combined with a 0/1 Knapsack review planner "
        "and deployed as a web application on the Render cloud platform."
    )
    add_p(abs_p2, space_after=12)

    abs_p3 = (
        "On the test set, the model reached an accuracy of 94.89%, with a spam precision, recall and F1-score of 0.93. Limitations "
        "include a single fixed data split, no per-source evaluation, and a genuine one-time password message wrongly marked as spam."
    )
    add_p(abs_p3, space_after=16)

    add_p("Keywords: data analysis, supervised classification, text data, TF-IDF, Logistic Regression, model evaluation, confusion matrix, precision and recall, 0/1 Knapsack, dynamic programming", italic=True, space_after=0)

    p_num5 = doc.add_paragraph()
    p_num5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num5.paragraph_format.space_before = Pt(80)
    p_num5.add_run("v").font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGES 6-7: TABLE OF CONTENTS
    # =========================================================================
    add_p("TABLE OF CONTENTS", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, space_before=10, space_after=20)

    toc_entries = [
        ("Chapter 1: Introduction", "1"),
        ("  1.1 Introduction and background", "1"),
        ("  1.2 Problem statement", "1"),
        ("  1.3 Motivation", "2"),
        ("  1.4 Objectives of the project", "2"),
        ("  1.5 Scope and limitations", "2"),
        ("  1.6 Organization of the report", "3"),
        ("Chapter 2: Literature Review and Existing Systems", "4"),
        ("  2.1 Review of related research papers, systems or applications", "4"),
        ("  2.2 Comparison of existing approaches", "5"),
        ("  2.3 Limitations of existing systems", "5"),
        ("  2.4 Research or implementation gap", "6"),
        ("  2.5 Proposed solution and its advantages", "6"),
        ("Chapter 3: Requirements Analysis", "7"),
        ("  3.1 Functional requirements", "7"),
        ("  3.2 Non-functional requirements", "7"),
        ("  3.3 Hardware requirements", "8"),
        ("  3.4 Software and technology requirements", "8"),
        ("  3.5 User roles and use cases", "9"),
        ("  3.6 Feasibility analysis", "9"),
        ("Chapter 4: System Design and Architecture", "11"),
        ("  4.1 Overall system architecture", "11"),
        ("  4.2 System workflow", "11"),
        ("  4.3 UML diagrams", "12"),
        ("  4.4 Database design and ER diagram", "13"),
        ("  4.5 Module description", "14"),
        ("  4.6 User interface or screen design", "15"),
        ("  4.7 Algorithms or models used", "15"),
        ("Chapter 5: Implementation", "18"),
        ("  5.1 Development environment and tools", "18"),
        ("  5.2 Technology stack", "18"),
        ("  5.3 Module-wise implementation", "18"),
        ("  5.4 Important algorithms and logic", "23"),
        ("  5.5 Database implementation", "23"),
        ("  5.6 Security, validation and error handling", "23"),
        ("  5.7 Selected code snippets", "24"),
        ("Chapter 6: Testing and Validation", "25"),
        ("  6.1 Testing strategy", "25"),
        ("  6.2 Unit testing", "25"),
        ("  6.3 Integration or system testing", "25"),
        ("  6.4 Test cases and expected results", "25"),
        ("  6.5 Actual results and pass or fail status", "26"),
        ("  6.6 Defects identified and corrections made", "27"),
        ("  6.7 Performance or model evaluation", "27"),
        ("Chapter 7: Results and Discussion", "31"),
        ("  7.1 Description of the final working system", "31"),
        ("  7.2 Screenshots of important outputs", "31"),
        ("  7.3 Results obtained", "32"),
        ("  7.4 Comparison with objectives or baseline", "33"),
        ("  7.5 Discussion of results", "33"),
        ("  7.6 Challenges encountered and solutions adopted", "34"),
        ("  7.7 Current limitations", "34"),
        ("Chapter 8: Conclusion and Future Enhancements", "36"),
        ("  8.1 Summary of the project", "36"),
        ("  8.2 Achievement of objectives", "36"),
        ("  8.3 Major learning outcomes", "36"),
        ("  8.4 Limitations and lessons learned", "36"),
        ("  8.5 Future enhancements", "37"),
        ("References", "38"),
        ("Appendix A: Source Code", "39"),
        ("Appendix B: Additional Test Cases", "41"),
        ("Appendix C: User Manual", "42"),
        ("Appendix D: Supporting Material", "43")
    ]

    t_toc = doc.add_table(rows=len(toc_entries), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_toc, color="FFFFFF")
    for idx, (title, page) in enumerate(toc_entries):
        c0 = t_toc.cell(idx, 0)
        c1 = t_toc.cell(idx, 1)
        c0.width = Inches(5.4)
        c1.width = Inches(0.8)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(2)
        p1.paragraph_format.space_after = Pt(2)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        
        is_ch = title.startswith("Chapter") or title in ["References", "Appendix A: Source Code", "Appendix B: Additional Test Cases", "Appendix C: User Manual", "Appendix D: Supporting Material"]
        r0 = p0.add_run(title)
        r0.bold = is_ch
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)
        
        r1 = p1.add_run(page)
        r1.bold = is_ch
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)

    p_num6 = doc.add_paragraph()
    p_num6.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num6.paragraph_format.space_before = Pt(30)
    p_num6.add_run("vi").font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: LIST OF FIGURES
    # =========================================================================
    add_p("LIST OF FIGURES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, space_before=10, space_after=20)
    
    figures_list = [
        ("Figure 3.1: Use case diagram of the system", "9"),
        ("Figure 4.1: Architecture of the system", "11"),
        ("Figure 4.2: Workflow of a scan request", "12"),
        ("Figure 4.3: Sequence diagram of a scan request", "13"),
        ("Figure 4.4: Data preparation pipeline with message counts", "14"),
        ("Figure 4.5: Home screen of the web application", "15"),
        ("Figure 5.1: Class distribution after cleaning", "19"),
        ("Figure 6.1: Validation confusion matrix of the plain Logistic Regression model", "28"),
        ("Figure 6.2: Test confusion matrix of the final balanced model", "29"),
        ("Figure 6.3: Validation comparison of the three models", "29"),
        ("Figure 7.1: Analysis results page of the web application", "31")
    ]

    t_fig = doc.add_table(rows=len(figures_list), cols=2)
    t_fig.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_fig, color="FFFFFF")
    for idx, (title, page) in enumerate(figures_list):
        c0 = t_fig.cell(idx, 0)
        c1 = t_fig.cell(idx, 1)
        c0.width = Inches(5.4)
        c1.width = Inches(0.8)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(4)
        p1.paragraph_format.space_after = Pt(4)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(title)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)
        r1 = p1.add_run(page)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)

    p_num8 = doc.add_paragraph()
    p_num8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num8.paragraph_format.space_before = Pt(80)
    p_num8.add_run("viii").font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 9: LIST OF TABLES
    # =========================================================================
    add_p("LIST OF TABLES", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, space_before=10, space_after=20)

    tables_list = [
        ("Table 2.1: Comparison of spam filtering approaches", "5"),
        ("Table 3.1: Functional requirements", "7"),
        ("Table 3.2: Non-functional requirements", "7"),
        ("Table 3.3: Hardware requirements", "8"),
        ("Table 3.4: Software and technology requirements", "8"),
        ("Table 3.5: Description of the use cases", "9"),
        ("Table 4.1: Data items handled by the system", "13"),
        ("Table 4.2: Modules of the system", "14"),
        ("Table 4.3: Dynamic programming table for the small example", "17"),
        ("Table 5.1: Technology stack", "18"),
        ("Table 5.2: Dataset overview before and after cleaning", "19"),
        ("Table 5.3: Data quality problems found and the action taken", "19"),
        ("Table 6.1: Test cases and expected results", "25"),
        ("Table 6.2: Actual results and status", "26"),
        ("Table 6.3: Defects found and the corrections made", "27"),
        ("Table 6.4: Validation results for the spam class and overall accuracy", "28"),
        ("Table 6.5: Classification report of the final model on the test set", "30"),
        ("Table 7.1: Results of the demonstration scan", "32"),
        ("Table 7.2: The five best combinations within 10 minutes", "32"),
        ("Table 7.3: Objectives and outcomes", "33"),
        ("Table B.1: Additional notebook runs", "41"),
        ("Table D.1: Sources merged in the dataset", "43"),
        ("Table D.2: Model files saved by the notebook", "43"),
        ("Table D.3: Terms used in the report", "43")
    ]

    t_tbl = doc.add_table(rows=len(tables_list), cols=2)
    t_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_tbl, color="FFFFFF")
    for idx, (title, page) in enumerate(tables_list):
        c0 = t_tbl.cell(idx, 0)
        c1 = t_tbl.cell(idx, 1)
        c0.width = Inches(5.4)
        c1.width = Inches(0.8)
        p0 = c0.paragraphs[0]
        p1 = c1.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        p1.paragraph_format.line_spacing = 1.15
        p0.paragraph_format.space_after = Pt(3)
        p1.paragraph_format.space_after = Pt(3)
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r0 = p0.add_run(title)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)
        r1 = p1.add_run(page)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)

    p_num9 = doc.add_paragraph()
    p_num9.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num9.paragraph_format.space_before = Pt(40)
    p_num9.add_run("ix").font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # PAGE 10: LIST OF ABBREVIATIONS
    # =========================================================================
    add_p("LIST OF ABBREVIATIONS", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=15, space_before=10, space_after=20)

    abbr_headers = ["Abbreviation", "Expansion"]
    abbr_data = [
        ["CSV", "Comma-Separated Values"],
        ["DP", "Dynamic Programming"],
        ["FN", "False Negative"],
        ["FP", "False Positive"],
        ["HTML", "HyperText Markup Language"],
        ["IDF", "Inverse Document Frequency"],
        ["IEEE", "Institute of Electrical and Electronics Engineers"],
        ["ML", "Machine Learning"],
        ["NB", "Naive Bayes"],
        ["OTP", "One-Time Password"],
        ["PaaS", "Platform as a Service"],
        ["SMS", "Short Message Service"],
        ["TF", "Term Frequency"],
        ["TF-IDF", "Term Frequency, Inverse Document Frequency"],
        ["TN", "True Negative"],
        ["TP", "True Positive"],
        ["UI", "User Interface"],
        ["UML", "Unified Modeling Language"],
        ["URL", "Uniform Resource Locator"],
        ["USN", "University Seat Number"]
    ]
    create_table(abbr_headers, abbr_data, col_widths=[1.8, 4.4])

    p_num10 = doc.add_paragraph()
    p_num10.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_num10.paragraph_format.space_before = Pt(40)
    p_num10.add_run("x").font.size = Pt(11)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 1: INTRODUCTION
    # =========================================================================
    add_h1("Chapter 1: Introduction")
    
    add_h2("1.1 Introduction and background")
    add_p(
        "Electronic messages are now one of the main ways in which people communicate. Text messages, chat applications and "
        "email carry everything from personal conversation to bank alerts. Alongside genuine messages come unwanted ones: prize "
        "offers, fake warnings about bank accounts, and links that try to collect personal details. These messages are called spam, "
        "and genuine messages are called ham. Spam wastes time, and some of it is dangerous because it is designed to trick the "
        "reader into paying money or sharing private information."
    )
    add_p(
        "Machine learning is widely used to filter spam. A classifier is trained on messages that have already been labelled as spam or ham, "
        "and it then labels new messages. Text must first be converted into numbers. A standard way to do this is TF-IDF, which gives each "
        "word in a message a weight that grows with how often the word appears in that message and shrinks with how many messages in the "
        "collection contain it [5]. Linear models such as Logistic Regression work well on such features and return a probability for each "
        "message, not only a label."
    )
    add_p(
        "This project builds such a filter using a public dataset and then adds a second step. The spam probability of each message is "
        "used to decide which flagged messages deserve attention first when the time available for review is limited. This decision is "
        "modelled as a 0/1 Knapsack problem and solved with dynamic programming. The finished system is deployed on a cloud platform "
        "so that it can be used from a web browser without installing anything."
    )
    add_p(
        "In this report the word “message” is used for the text of an SMS, a chat message or an email, because the dataset used for "
        "training combines all three kinds of text [10]."
    )

    add_h2("1.2 Problem statement")
    add_p(
        "Spam filters usually return a single answer for each message: spam or not spam. A person who has to go through a large batch "
        "of flagged messages, for example when checking a quarantine folder, still has to decide which of them to open first. Every check "
        "takes time, and the time available is limited."
    )
    add_p(
        "The problem addressed in this project has two parts. The first is to classify messages as spam or ham accurately, using a model "
        "trained only on public data. The second is to choose, from the messages predicted as spam, the group with the highest total review "
        "value that can be checked within a given time budget, when the time needed for each message is known. The solution must be usable "
        "through a web page without any local installation."
    )

    add_h2("1.3 Motivation")
    add_bullet("Spam filtering is a well-studied text classification problem with public data, so the quality of a solution can be measured honestly on held-out examples.")
    add_bullet("The review decision has the exact structure of a knapsack problem. Each message has a value and a time cost, the time budget is fixed, and each message is either checked completely or not at all.")
    add_bullet("Combining the two ideas in one working system gave practical experience of the full path from raw data to a deployed service: data preparation, modelling, algorithm design, evaluation and deployment.")
    add_bullet("A hosted web application lets anyone try the system from a browser, which makes the project easy to demonstrate and to test.")

    add_h2("1.4 Objectives of the project")
    add_bullet("To prepare a public labelled message dataset by finding and fixing duplicate messages, conflicting labels, damaged characters and overlap between the training, validation and test data.")
    add_bullet("To convert messages into TF-IDF features and train a Logistic Regression classifier that predicts spam or ham together with a spam probability.")
    add_bullet("To evaluate the classifier with accuracy, precision, recall, F1-score and confusion matrices on separate validation and test sets, and to compare it with a Multinomial Naive Bayes baseline.")
    add_bullet("To convert spam probabilities into review values and to select messages for review within a time budget using a 0/1 Knapsack algorithm solved by dynamic programming.")
    add_bullet("To deploy the system as a web application on a cloud platform so that users can scan their own messages from a browser.")
    add_bullet("To document the design, testing, results and limitations of the system honestly.")

    add_h2("1.5 Scope and limitations")
    add_p(
        "The project covers English-language messages and a two-class decision (spam or ham). The web application accepts three inputs: "
        "the messages, one per line; the time in whole minutes needed to review each message; and the total time budget in whole minutes. "
        "It returns a prediction and spam probability for each message, together with a review plan for the messages predicted as spam."
    )
    add_p("The following limits apply to the work:")
    add_bullet("The classifier was trained and tested on one public dataset that merges three sources. Its behaviour on other kinds of text, other languages or newer spam styles was not measured.")
    add_bullet("The classifier uses the default decision rule of Logistic Regression, which labels a message as spam when its spam probability is above 50%. The probabilities were not calibrated.")
    add_bullet("The review value is the spam probability multiplied by 100 and rounded. It does not measure how harmful a message is. Review times are entered by the user and are not predicted.")
    add_bullet("The interface expects one message per line, so a long email must be entered as a single line of text.")
    add_bullet("User accounts, stored history and monitoring of the hosted service were outside the scope of the project.")

    add_h2("1.6 Organization of the report")
    add_p(
        "The report is organised in eight chapters followed by references and appendices. Chapter 1 introduces the problem, the objectives "
        "and the scope. Chapter 2 reviews related research and existing approaches and explains the gap that this project addresses. "
        "Chapter 3 lists the functional and non-functional requirements, the hardware and software needed, the use cases and the feasibility "
        "of the project. Chapter 4 describes the design of the system: the architecture, the workflow, the UML diagrams, the modules, the user "
        "interface and the algorithms. Chapter 5 explains how each module was implemented, including data preparation, model training, the "
        "review planner and deployment. Chapter 6 presents the testing carried out, the defects found and the evaluation of the classifier. "
        "Chapter 7 presents the results, compares them with the objectives and discusses the limitations. Chapter 8 concludes the report and "
        "lists possible future enhancements. The appendices contain additional source code, extra test evidence, a user manual and supporting material."
    )

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 2: LITERATURE REVIEW AND EXISTING SYSTEMS
    # =========================================================================
    add_h1("Chapter 2: Literature Review and Existing Systems")
    
    add_h2("2.1 Review of related research papers, systems or applications")
    add_p(
        "Automatic spam filtering has been studied for more than two decades. Early commercial and research filters relied on hand-written "
        "rules and keyword lists. Sahami et al. [3] examined methods for building junk email filters automatically from labelled examples "
        "and used Bayesian classifiers for this purpose. They also found that a rule-based approach was of limited use for the task, "
        "which supported the move to learned models."
    )
    add_p(
        "Androutsopoulos et al. [4] compared a Naive Bayesian filter with a memory-based learning filter. They introduced cost-sensitive "
        "evaluation measures, because wrongly blocking a genuine message is usually worse than letting one spam message through. Both methods "
        "filtered spam accurately and both clearly outperformed the keyword-based filter of a widely used mail reader. This work shows two "
        "ideas that are also used in the present project: learning from labelled data and judging a filter by the kinds of mistakes it makes "
        "and not only by one accuracy figure."
    )
    add_p(
        "Spam is not limited to email. Almeida et al. [1] collected the SMS Spam Collection, a public set of 5,574 English text messages "
        "tagged as ham or spam, and reported baseline results for several machine learning methods on it. The collection is available through "
        "the UCI Machine Learning Repository [2]. It is one of the three sources merged into the dataset used in this project [10], "
        "together with a Telegram spam collection and the Enron email spam collection."
    )
    add_p(
        "On the technical side, TF-IDF weighting is a standard way of turning text into numeric vectors [5]. The scikit-learn library [6] "
        "provides ready implementations of the TF-IDF vectorizer, Logistic Regression, Multinomial Naive Bayes and the evaluation metrics "
        "that are used in this work. For the review planning step, the 0/1 Knapsack problem is a classic example of dynamic programming, "
        "and its solution by a table of sub-problems is described in standard algorithm textbooks [7]."
    )
    add_p(
        "For deployment, the NIST definition of cloud computing describes Platform as a Service as a model in which the consumer deploys an "
        "application onto the provider’s infrastructure without managing the underlying servers [8]. Render, the platform used here, offers "
        "web services that host dynamic web applications at a public address and can build and deploy the code from a linked Git repository [9]."
    )

    add_h2("2.2 Comparison of existing approaches")
    add_p("Table 2.1 compares the main approaches discussed above with the approach followed in this project.")
    
    t21_headers = ["Approach", "Main idea", "Strengths", "Weaknesses"]
    t21_data = [
        ["Keyword and rule-based filters", "Block messages that match hand-written words or patterns", "Simple and easy to explain", "Rules need constant manual upkeep and can be avoided by changing wording [3], [4]"],
        ["Naive Bayes classifiers [3], [4]", "Learn word probabilities for each class from labelled data", "Fast to train and works with small amounts of data", "Assumes words are independent given class, not true of real text"],
        ["Linear models on TF-IDF features [1], [5], [6]", "Learn one weight per word or word pair and combine them", "Handles many sparse features. Logistic Regression also gives probability", "Needs enough labelled data. Results depend on dataset and decision threshold"],
        ["Approach of this project", "Linear classifier on TF-IDF features, followed by 0/1 Knapsack review planning", "Gives a label, probability and an optimal review plan for a given time budget", "Review value is only a proxy for importance. Tested on one dataset"]
    ]
    create_table(t21_headers, t21_data, col_widths=[1.5, 1.6, 1.5, 1.65])
    add_p("Table 2.1: Comparison of spam filtering approaches", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("2.3 Limitations of existing systems")
    add_bullet("Each of the studies [1], [3], [4] concentrated on one channel, either email or SMS, so a filter built for one channel is not shown to work on the other.")
    add_bullet("The studies end with a classification result. They do not consider that the person reading the flagged messages has limited time and must choose which ones to check first.")
    add_bullet("Rule-based filters depend on people updating the rules, and they stop working when senders change the wording of their messages.")
    add_bullet("Several early evaluations used small collections. For example, the SMS Spam Collection contains 5,574 messages [2], which is small compared with the 54,831 messages used after cleaning in this project.")

    add_h2("2.4 Research or implementation gap")
    add_p(
        "In the studies reviewed here, the output of the classifier was the end of the process. We did not find a treatment that links "
        "the confidence of the classifier to a decision about how a limited review time should be spent. The gap that this project "
        "addresses is therefore practical: to connect the spam probability produced by a classifier with a 0/1 Knapsack planner, "
        "and to make the result available as a hosted web application that anyone can try."
    )

    add_h2("2.5 Proposed solution and its advantages")
    add_p(
        "The proposed system works in two stages. In the first stage a TF-IDF vectorizer and a class-balanced Logistic Regression "
        "classifier, trained on a cleaned public dataset, predict whether each message is spam and with what probability. In the "
        "second stage the messages predicted as spam are given a review value equal to the rounded spam probability multiplied by 100, "
        "and a dynamic programming solution of the 0/1 Knapsack problem chooses the messages that give the largest total value within the time budget."
    )
    add_bullet("The selection is optimal for the given values and whole-minute times, because dynamic programming checks every sub-problem rather than relying on a rule of thumb.")
    add_bullet("The classifier is simple, quick to train on a laptop and easy to retrain, and every step of its preparation is documented.")
    add_bullet("Evaluation uses separate validation and test sets that share no text, so the reported accuracy is not inflated by repeated messages.")
    add_bullet("Only open source libraries and a public dataset are used, so the work can be reproduced without licence cost.")
    add_bullet("Deployment on a cloud platform means that the system can be used from any browser.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 3: REQUIREMENTS ANALYSIS
    # =========================================================================
    add_h1("Chapter 3: Requirements Analysis")
    
    add_h2("3.1 Functional requirements")
    add_p("The functional requirements describe what the system must do. They were derived from the problem statement and the behaviour of the working application.")
    
    t31_headers = ["ID", "Requirement"]
    t31_data = [
        ["FR1", "Accept one or more messages, entered one per line."],
        ["FR2", "Accept the review time of each message in whole minutes, and one total time budget in whole minutes."],
        ["FR3", "Validate the input: messages must be non-empty text, there must be one review time for every message, review times must be positive integers and the budget must be a non-negative integer."],
        ["FR4", "Predict for every message whether it is spam or ham."],
        ["FR5", "Report the spam probability of every message as a percentage."],
        ["FR6", "Convert the spam probability of each message predicted as spam into an integer review value (probability × 100, rounded). Messages predicted as ham are not eligible for review."],
        ["FR7", "Select the messages that give the maximum total review value within the time budget, using a 0/1 Knapsack algorithm."],
        ["FR8", "Display a table with the message, prediction, spam probability, value, time and decision, together with a summary of the maximum value, the time used and the number of messages selected."]
    ]
    create_table(t31_headers, t31_data, col_widths=[0.8, 5.45])
    add_p("Table 3.1: Functional requirements", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("3.2 Non-functional requirements")
    t32_headers = ["Attribute", "Requirement"]
    t32_data = [
        ["Accuracy", "The classifier should reach a test accuracy above 90% and should treat the spam and ham classes with balanced precision and recall."],
        ["Performance", "A scan of a small batch of messages should return within a few seconds. Response time was not formally measured in this project."],
        ["Usability", "The page should need only three inputs and one button, with the results shown in a single table."],
        ["Portability", "The system should be usable from any modern web browser without installation."],
        ["Maintainability", "The saved model files should be kept separate from the application code so that the model can be retrained and replaced."],
        ["Reproducibility", "Random choices must use a fixed seed so that the data split and the trained model can be recreated."],
        ["Reliability", "Invalid input must be rejected with a clear message instead of producing a wrong plan."]
    ]
    create_table(t32_headers, t32_data, col_widths=[1.5, 4.75])
    add_p("Table 3.2: Non-functional requirements", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("3.3 Hardware requirements")
    t33_headers = ["Item", "Model preparation (notebook)", "End user of the web application"]
    t33_data = [
        ["Processor", "Dual-core or better; Apple silicon was used", "Any device that can run a web browser"],
        ["Memory", "8 GB recommended", "No special requirement"],
        ["Storage", "About 2 GB free for Python environment, dataset cache and model files", "No special requirement"],
        ["Network", "Internet access to download dataset and packages", "Internet access to reach the hosted application"]
    ]
    create_table(t33_headers, t33_data, col_widths=[1.4, 2.4, 2.45])
    add_p("Table 3.3: Hardware requirements", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("3.4 Software and technology requirements")
    t34_headers = ["Component", "Detail", "Purpose"]
    t34_data = [
        ["Python", "Version 3.14 (Anaconda distribution)", "Programming language for all code"],
        ["Jupyter Notebook", "Interactive notebook", "Running and documenting the experiments"],
        ["pandas, NumPy", "pandas 3.0.3, NumPy 2.4.6", "Loading, cleaning and summarising data"],
        ["scikit-learn", "TF-IDF vectorizer, Logistic Regression, Multinomial Naive Bayes, metrics, data splitting", "Feature extraction, models and evaluation [6]"],
        ["Hugging Face datasets", "datasets 5.1.0 with PyArrow 25.0.1", "Downloading the public dataset"],
        ["joblib, matplotlib", "Standard Python packages", "Saving model files; plotting confusion matrices"],
        ["Render", "Cloud platform for web services", "Hosting the web application [9]"],
        ["Web browser", "Any modern browser", "Using the application"]
    ]
    create_table(t34_headers, t34_data, col_widths=[1.5, 2.4, 2.35])
    add_p("Table 3.4: Software and technology requirements", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("3.5 User roles and use cases")
    add_p("The system has one role, the user, who is any person who wants to scan messages and plan their review. Figure 3.1 shows the use cases and Table 3.5 describes them.")
    add_image_figure("p20_img1_1152x843.jpeg", "Figure 3.1: Use case diagram of the system", width=Inches(4.5))

    t35_headers = ["ID", "Use case", "Description"]
    t35_data = [
        ["UC1", "Enter messages", "The user types or pastes the messages, one per line."],
        ["UC2", "Set review times and budget", "The user enters the minutes needed to review each message and the total minutes available."],
        ["UC3", "Run scan", "The user presses the button. The system classifies the messages and computes the review plan."],
        ["UC4", "View predictions and probabilities", "The user reads the spam or ham label and the spam probability of each message."],
        ["UC5", "View review plan and summary", "The user reads which messages are selected, the review time used and the maximum review value."]
    ]
    create_table(t35_headers, t35_data, col_widths=[0.8, 2.2, 3.25])
    add_p("Table 3.5: Description of the use cases", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("3.6 Feasibility analysis")
    add_bullet("Technical feasibility: The dataset is public and all libraries are open source. A linear model on TF-IDF features can be trained on an ordinary laptop, as was done in this project, and the dynamic programming step needs only a small table.")
    add_bullet("Economic feasibility: No software licence had to be bought. The dataset is released under the MIT licence according to its dataset card [10]. Hosting cost depends on the plan chosen on the cloud platform.")
    add_bullet("Operational feasibility: The interface needs three inputs and one button, so users do not need training. The trained model files are loaded by the application and no training happens when a user scans messages.")
    add_bullet("Ethical and privacy considerations: The model was trained only on public data. Because messages that users type may be private, users should avoid entering sensitive personal information into any hosted tool.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 4: SYSTEM DESIGN AND ARCHITECTURE
    # =========================================================================
    add_h1("Chapter 4: System Design and Architecture")
    
    add_h2("4.1 Overall system architecture")
    add_p(
        "The system has an offline stage and an online stage, as shown in Figure 4.1. In the offline stage, carried out in a "
        "Jupyter notebook, the public dataset is cleaned and split, a TF-IDF vectorizer is fitted on the training data and "
        "the classifier is trained and evaluated. The fitted vectorizer and classifier are saved as two joblib files."
    )
    add_p(
        "In the online stage the web application, hosted on Render, loads the saved files. When a user submits a scan, the messages "
        "pass through the vectorizer and the classifier, and the review planner then selects the messages to be reviewed. The results "
        "are returned to the browser as a table and a summary. Render is a Platform as a Service offering [8], [9], so the application "
        "is deployed without managing physical servers."
    )
    add_image_figure("p22_img1_1416x1012.jpeg", "Figure 4.1: Architecture of the system", width=Inches(5.0))

    add_h2("4.2 System workflow")
    add_p(
        "Figure 4.2 shows what happens when a user runs a scan. The input is checked first. Valid messages are converted into TF-IDF "
        "vectors and the classifier predicts the spam probability of each one. A message predicted as spam receives a review value "
        "equal to its probability multiplied by 100 and rounded. A message predicted as ham receives the value zero and is left out of "
        "the plan. The Knapsack step then finds the best set of messages for the time budget, and a backtracking step lists which messages form that set."
    )
    add_image_figure("p23_img1_618x1049.jpeg", "Figure 4.2: Workflow of a scan request", width=Inches(3.2))

    add_h2("4.3 UML diagrams")
    add_p("The use case diagram of the system is given in Figure 3.1. Figure 4.3 is a sequence diagram of one scan. A class diagram is not included because the system is built from functions and trained model objects and not from a hierarchy of application classes.")
    add_image_figure("p24_img1_1285x960.jpeg", "Figure 4.3: Sequence diagram of a scan request", width=Inches(4.8))

    add_h2("4.4 Database design and ER diagram")
    add_p("The system does not use a database, so there is no ER diagram. The data handled by the system is listed in Table 4.1. The dataset files and the saved model files are ordinary files, and the data of a scan exists only for the duration of the request.")
    
    t41_headers = ["Data item", "Contents", "Where it lives"]
    t41_data = [
        ["Dataset record", "A label (ham or spam) and the message text", "Dataset files downloaded from Hugging Face"],
        ["Cleaned dataset", "Original text, processed text and label for 54,831 messages", "Notebook memory"],
        ["Vectorizer file", "The TF-IDF vocabulary and weights learned from the training data", "tfidf_vectorizer.joblib"],
        ["Classifier file", "The trained Logistic Regression model", "spam_classifier.joblib"],
        ["Scan input", "Messages, review times and the budget", "Requests sent from the browser"],
        ["Scan result", "One row per message and a summary", "Response shown in the browser"]
    ]
    create_table(t41_headers, t41_data, col_widths=[1.5, 2.8, 1.95])
    add_p("Table 4.1: Data items handled by the system", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("4.5 Module description")
    add_p("The system is divided into six modules, summarised in Table 4.2. Figure 4.4 shows the data preparation module in more detail, with the number of messages that remained after each step.")
    
    t42_headers = ["Module", "Input", "Output", "Purpose"]
    t42_data = [
        ["Data preparation", "Raw dataset splits", "Clean train, validation and test sets", "Remove duplicates, conflicts and encoding problems; split without overlap"],
        ["Feature extraction", "Message text", "TF-IDF vectors with 50,000 features", "Turn text into numbers"],
        ["Classification", "TF-IDF vectors", "Label and spam probability", "Decide spam or ham"],
        ["Review planner", "Values, times, budget", "Selected messages and maximum value", "Solve the 0/1 Knapsack problem"],
        ["Web interface", "User input", "Results table and summary", "Collect input and show results"],
        ["Deployment", "Code and model files", "Hosted web application", "Make the system available online"]
    ]
    create_table(t42_headers, t42_data, col_widths=[1.4, 1.4, 1.6, 1.85])
    add_p("Table 4.2: Modules of the system", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)
    add_image_figure("p25_img1_778x700.jpeg", "Figure 4.4: Data preparation pipeline with message counts", width=Inches(3.8))

    add_h2("4.6 User interface or screen design")
    add_p(
        "Figure 4.5 shows the home screen of the web application, which names itself SpamGuard. The page uses a dark theme with a "
        "short headline, two short descriptions and a phone-style card in the centre. The left description states that TF-IDF features "
        "and a Logistic Regression classifier estimate whether each message looks like spam. The right description states that only messages "
        "predicted as spam are eligible for review and that the planner selects the highest total review value within the time budget."
    )
    add_p(
        "The card is titled “New Scan”. It contains a text box for the messages, one per line, a field for the review time of each message "
        "in minutes, a field for the budget, and a “Run scan” button. The review time field explains that the values are comma-separated, "
        "with one value per message, in the range 1 to 60. The top bar offers three links: Analyzer, Review plan and System status. "
        "The results screen is shown in Chapter 7."
    )
    add_image_figure("p26_img1_1139x533.jpeg", "Figure 4.5: Home screen of the web application", width=Inches(4.8))

    add_h2("4.7 Algorithms or models used")
    add_h3("4.7.1 TF-IDF feature extraction")
    add_p("TF-IDF represents each message as a vector with one entry for each word or word pair in the vocabulary. The weight of a term t in a message d is the product of its term frequency and its inverse document frequency:")
    add_p("tf-idf(t, d) = tf(t, d) × idf(t)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    add_p("With the default settings of the scikit-learn vectorizer [6], idf(t) = ln((1 + n) / (1 + df(t))) + 1, where n is the number of training messages and df(t) is the number of training messages that contain t. Each message vector is then scaled to unit length. Words that occur in many messages get a low weight, and words that are rare but present get a higher weight. In this project the vocabulary was limited to the 50,000 most frequent single words and word pairs, text was converted to lower case and no stop words were removed.")

    add_h3("4.7.2 Logistic Regression")
    add_p("Logistic Regression computes a weighted sum of the features of a message and passes it through the logistic function to obtain the probability that the message is spam:")
    add_p("P(spam | x) = 1 / (1 + e^-(w · x + b))", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True)
    add_p("The weights w and the bias b are learned by minimising the regularised log loss on the training data. The default L2 regularisation of scikit-learn was used. A message is labelled spam when this probability is above 0.5. Because spam is the smaller class (37.46% of the cleaned data), the final model uses the “balanced” class weight option, which weights each class by n_samples / (n_classes × n_class). For the training set, whose counts are 24,002 ham and 14,379 spam messages, this gives weights of about 0.80 for ham and 1.33 for spam.")

    add_h3("4.7.3 Multinomial Naive Bayes (baseline)")
    add_p("Multinomial Naive Bayes was trained on the same features as a baseline. It chooses the class c that maximises P(c) multiplied by the product of P(t | c) over the terms of the message, under the assumption that terms are independent given the class [3], [4]. It is fast and simple, which makes it a useful reference point for the Logistic Regression model.")

    add_h3("4.7.4 0/1 Knapsack by dynamic programming")
    add_p("The review plan is a 0/1 Knapsack problem. There are n messages predicted as spam candidates. Message i has a value v(i) and a review time w(i), and the total time budget is W minutes. Each message can be chosen once or not at all. The aim is to maximise the sum of the chosen values so that the sum of the chosen times does not exceed W. Let dp[i][j] be the best total value that can be obtained from the first i messages with j minutes available. Then:")
    add_p("dp[0][j] = 0 for every j", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("dp[i][j] = dp[i-1][j]   if w(i) > j", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("dp[i][j] = max( dp[i-1][j], v(i) + dp[i-1][j - w(i)] )   if w(i) ≤ j", align=WD_ALIGN_PARAGRAPH.CENTER)
    add_p("The answer is dp[n][W]. To find which messages were chosen, the table is read backwards from dp[n][W]. If dp[i][j] differs from dp[i-1][j], message i was chosen, and j is reduced by w(i). The table has (n + 1) × (W + 1) cells and each cell takes constant time, so the running time and the memory use are both O(nW) [7]. This is called pseudo-polynomial because it grows with the numeric value of the budget W, which is acceptable here because W is a small number of minutes.")
    add_p("Table 4.3 shows the table for a small example used in the notebook: three messages with values 60, 100 and 120, review times 5, 10 and 6 minutes, and a budget of 10 minutes. The last cell gives the answer 120. Reading backwards, row 3 differs from row 2 at 10 minutes, so message 3 is chosen and 6 minutes are used up. At 4 minutes the values in rows 2 and 1 are both 0, so no other message is chosen.")
    
    t43_headers = ["Items", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    t43_data = [
        ["None", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"],
        ["First 1", "0", "0", "0", "0", "0", "60", "60", "60", "60", "60", "60"],
        ["First 2", "0", "0", "0", "0", "0", "60", "60", "60", "60", "60", "100"],
        ["First 3", "0", "0", "0", "0", "0", "60", "120", "120", "120", "120", "120"]
    ]
    create_table(t43_headers, t43_data)
    add_p("Table 4.3: Dynamic programming table for the small example (columns are minutes available)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 5: IMPLEMENTATION
    # =========================================================================
    add_h1("Chapter 5: Implementation")
    
    add_h2("5.1 Development environment and tools")
    add_p("All data preparation, modelling and evaluation were carried out in a Jupyter notebook running Python 3.14 from the Anaconda distribution on a computer with an Apple silicon processor. The dataset was downloaded with the Hugging Face datasets library, the models were built with scikit-learn, and the trained objects were saved with joblib. The web application built from the saved models was deployed on the Render cloud platform and is used through a browser.")

    add_h2("5.2 Technology stack")
    t51_headers = ["Layer", "Technology", "Role"]
    t51_data = [
        ["Data", "Hugging Face dataset mshenoda/spam-messages", "Labelled messages for training and testing"],
        ["Preparation", "pandas, Python html module", "Cleaning, duplicate removal, HTML entity decoding"],
        ["Features", "scikit-learn TfidfVectorizer", "Word and word-pair TF-IDF features"],
        ["Models", "scikit-learn LogisticRegression and MultinomialNB", "Classifier and baseline"],
        ["Evaluation", "scikit-learn metrics, matplotlib", "Accuracy, precision, recall, F1-score, confusion matrices"],
        ["Persistence", "joblib", "Saving and loading the vectorizer and classifier"],
        ["Review planning", "Python function for 0/1 Knapsack", "Optimal selection of messages"],
        ["Hosting", "Render web service", "Public web application"]
    ]
    create_table(t51_headers, t51_data, col_widths=[1.5, 2.5, 2.25])
    add_p("Table 5.1: Technology stack", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("5.3 Module-wise implementation")
    add_h3("5.3.1 Data collection and inspection")
    add_p("The dataset was loaded from Hugging Face with two lines of code:")
    add_code_block("from datasets import load_dataset\nds = load_dataset(\"mshenoda/spam-messages\")")
    add_p("According to its dataset card, the data merges three public sources: the SMS Spam Collection, a Telegram spam and ham collection and the Enron email spam collection [10]. It comes with three splits, which hold 47,392, 5,923 and 5,926 messages. Each record has a text column and a label column, and no missing values were found. The label counts are given in Table 5.2.")
    
    t52_headers = ["Stage", "Train", "Validation", "Test", "Total"]
    t52_data = [
        ["Original splits", "47,392", "5,923", "5,926", "59,241"],
        ["Original ham", "n/a", "n/a", "n/a", "35,631"],
        ["Original spam", "n/a", "n/a", "n/a", "23,610"],
        ["After cleaning and re-splitting", "38,381", "8,225", "8,225", "54,831"],
        ["Cleaned ham", "24,002", "5,143", "5,144", "34,289"],
        ["Cleaned spam", "14,379", "3,082", "3,081", "20,542"]
    ]
    create_table(t52_headers, t52_data, col_widths=[2.2, 1.0, 1.0, 1.0, 1.05])
    add_p("Table 5.2: Dataset overview before and after cleaning", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)
    add_p("The source of each message is not stored in the data columns, so the performance of the model on each source separately was not measured. The cleaned data has 34,289 ham messages (62.54%) and 20,542 spam messages (37.46%), as shown in Figure 5.1.")
    add_image_figure("p30_img1_691x472.jpeg", "Figure 5.1: Class distribution after cleaning", width=Inches(3.8))

    add_h3("5.3.2 Data cleaning")
    add_p("The inspection found several data quality problems, summarised in Table 5.3. The counts for damaged characters, HTML entities and spacing were taken on the 54,961 messages that remained after exact duplicates were removed.")
    
    t53_headers = ["Problem", "Number found", "Action"]
    t53_data = [
        ["A text with conflicting labels (the word “hi” labelled both spam and ham)", "1 text, 3 rows", "All rows of the text were removed"],
        ["Exact duplicate rows after combining the splits", "4,277", "Duplicates removed, one copy kept"],
        ["Overlap between the original splits", "Train and validation 643, train and test 624, validation and test 99", "Removed by deduplication and a new split"],
        ["Damaged characters (Unicode replacement character)", "480 messages, 867 characters", "Replaced by a space in the processed text"],
        ["HTML entities such as &lt; and &amp;", "269 messages", "Decoded to normal characters"],
        ["Leading or trailing spaces; repeated spaces", "8,428; 1,144", "Trimmed and collapsed"],
        ["Duplicates that appeared only after cleaning the text", "130", "Removed, one copy kept"]
    ]
    create_table(t53_headers, t53_data, col_widths=[2.3, 1.9, 2.05])
    add_p("Table 5.3: Data quality problems found and the action taken", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_p("The original text was kept in one column and the cleaned text was written to a second column, so no information was lost. The two steps that repair damaged characters and decode HTML entities were written as follows:")
    add_code_block("""# Preserve the original text 
df_clean["text_original"] = df_clean["text"]

# Create a separate column for NLP preprocessing 
df_clean["text_processed"] = df_clean["text"].copy()

# Replace the Unicode replacement character with a space 
df_clean["text_processed"] = df_clean["text_processed"].str.replace("\uFFFD", " ", regex=False)

import html
# Decode HTML entities in the processed text 
df_clean["text_processed"] = df_clean["text_processed"].apply(html.unescape)""")

    add_h3("5.3.3 Splitting the data")
    add_p("The cleaned messages were split into 70% training, 15% validation and 15% test data. The split was stratified on the label, so that every part has the same share of spam, and a fixed random state of 42 was used. A check after the split showed no message text in common between any two parts.")
    add_code_block("""from sklearn.model_selection import train_test_split

# First, separate 15% for the test set 
df_train_val, df_test = train_test_split(
    df_clean, test_size=0.15, random_state=42, stratify=df_clean["label"]
)

# Next, take 15% of the original total for validation (15 / 85 = ~0.17647)
df_train, df_val = train_test_split( 
    df_train_val, test_size=0.17647, random_state=42, stratify=df_train_val["label"]
)""")

    add_h3("5.3.4 Feature extraction and model training")
    add_p("The TF-IDF vectorizer was fitted on the training messages only, and then applied to the validation and test messages, so that no information from them leaked into the vocabulary. The vectors for all three sets have 50,000 columns.")
    add_code_block("""from sklearn.feature_extraction.text import TfidfVectorizer

# Create the TF-IDF vectorizer 
tfidf = TfidfVectorizer(
    lowercase=True, stop_words=None, ngram_range=(1, 2), max_features=50000
)
# Learn vocabulary and transform training messages 
X_train_tfidf = tfidf.fit_transform(X_train)""")

    add_p("Three models were trained and compared on the validation set: Logistic Regression, Logistic Regression with balanced class weights and Multinomial Naive Bayes. The balanced model was selected, and it was the only model evaluated on the test set.")
    add_code_block("""from sklearn.linear_model import LogisticRegression

# Create a class-balanced Logistic Regression model 
balanced_model = LogisticRegression(
    max_iter=1000, random_state=42, class_weight="balanced"
)
# Train on the training data 
balanced_model.fit(X_train_tfidf, y_train)

import joblib
from pathlib import Path

Path("models").mkdir(exist_ok=True)
joblib.dump(tfidf, "models/tfidf_vectorizer.joblib")
joblib.dump(balanced_model, "models/spam_classifier.joblib")""")

    add_h3("5.3.5 Review planner")
    add_p("The review planner is a Python function that implements the dynamic programming table and the backtracking step described in Section 4.7.4. It takes the values, the review times and the budget, and returns the maximum value and the positions of the chosen messages.")
    add_code_block("""def knapsack_01(values, weights, capacity): 
    n = len(values)
    # dp[i][w] = maximum value using first i items with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1): 
        value = values[i - 1] 
        weight = weights[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weight <= w:
                include_value = value + dp[i - 1][w - weight] 
                dp[i][w] = max(dp[i][w], include_value)
                
    # Recover selected items via backtracking
    selected_items = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]: 
            selected_items.append(i - 1) 
            w -= weights[i - 1]
    selected_items.reverse()
    return dp[n][capacity], selected_items""")

    add_h3("5.3.6 Web application and deployment")
    add_p("The saved vectorizer and classifier and the review planner were packaged as a web application, and the application was deployed on Render as a web service [9]. The application shows the home screen in Figure 4.5 and the results screen in Figure 7.1. A user opens the page in a browser, enters the messages, review times and budget, and receives the results without installing any software.")

    add_h2("5.4 Important algorithms and logic")
    add_p("The logic that connects the two stages is the conversion of probabilities into values. For a message i with spam probability p(i), the review value is v(i) = round(100 × p(i)) if the message is predicted as spam, and v(i) = 0 otherwise. A value of zero means the message can never improve the total, so ham messages are never selected. Messages with a high probability and a short review time are the most attractive, and a very long review time can rule out a message even when its probability is high. Section 7.3 gives an example in which the message with the highest probability was not selected for this reason.")

    add_h2("5.5 Database implementation")
    add_p("No database was implemented, as explained in Section 4.4. The only stored artefacts are the downloaded dataset files and the two joblib files in the models folder.")

    add_h2("5.6 Security, validation and error handling")
    add_p("The planner function checks its input before doing any work and raises an error with a clear message when a check fails. The checks are listed below.")
    add_bullet("At least one message must be given.")
    add_bullet("There must be exactly one review time for each message.")
    add_bullet("Every message must be a non-empty text.")
    add_bullet("Every review time must be a positive whole number, and truth values are rejected.")
    add_bullet("The time budget must be a non-negative whole number.")
    add_bullet("The classifier must contain a class named spam.")
    add_p("The input form also tells the user that each review time is a value between 1 and 60 minutes. Joblib files can run code when they are loaded, so the model files should be loaded only from a trusted source, which in this project is the author's own training run. Users should not type confidential messages into the hosted tool.")

    add_h2("5.7 Selected code snippets")
    add_p("The main snippets are shown in the sections above: data loading in Section 5.3.1, cleaning in Section 5.3.2, splitting in Section 5.3.3, vectorizing and training in Section 5.3.4, model saving in Section 5.3.4 and the Knapsack function in Section 5.3.5. Each snippet is copied from the project notebook, with comments trimmed where a shorter listing was enough. The wrapper function that combines prediction and planning is given in full in Appendix A.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 6: TESTING AND VALIDATION
    # =========================================================================
    add_h1("Chapter 6: Testing and Validation")
    
    add_h2("6.1 Testing strategy")
    add_p("Testing was done at three levels: checks on the data and on single components, checks that the components work together, and checks of the complete web application. The evidence for the results in this chapter is the output of the project notebook and the screenshots of the deployed application. No automated test framework was used, so these are manual and notebook-based checks. In addition, the output of the web application for one scan was verified independently by trying every possible combination of messages.")

    add_h2("6.2 Unit testing")
    add_p("Unit-level checks covered data loading, missing values, overlap between the data splits, the shape of the TF-IDF output, reloading of the saved model files and the Knapsack function on a known example. They are listed as T1 to T6 in Table 6.1.")

    add_h2("6.3 Integration or system testing")
    add_p("Integration checks ran the saved vectorizer and classifier on new messages and ran the complete planner in the notebook (T7 and T8). System checks used the deployed web application with ten messages and confirmed that the plan respects the time budget, excludes ham messages and is optimal (T9 to T13). T14 records a judgement test on a genuine one-time password message.")

    add_h2("6.4 Test cases and expected results")
    t61_headers = ["ID", "Level", "Test and input", "Expected result"]
    t61_data = [
        ["T1", "Unit", "Load the dataset from Hugging Face", "Three splits with a text and a label column; 47,392, 5,923 and 5,926 rows"],
        ["T2", "Unit", "Check for missing or empty text", "No missing or empty text"],
        ["T3", "Unit", "Compare text between the final training, validation and test sets", "No text in common"],
        ["T4", "Unit", "Apply the TF-IDF vectorizer to the three sets", "Each set has 50,000 columns"],
        ["T5", "Unit", "Reload the saved vectorizer and classifier", "Both load; classes are ham and spam"],
        ["T6", "Unit", "Knapsack on values 60, 100, 120, times 5, 10, 6, budget 10", "Maximum value 120 with the third message"],
        ["T7", "Integration", "Classify five new messages (prizes, bank, lunch, notes)", "Prize, cash and bank messages are spam; lunch and notes messages are ham"],
        ["T8", "Integration", "Run the planner in the notebook on five messages, times 4, 2, 5, 3, 1, budget 6", "A results table and a summary within the 6 minute budget"],
        ["T9", "System", "Web application: ten messages, times 4, 2, 5, 1, 3, 2, 4, 1, 5, 2, budget 10", "Results table and summary are shown"],
        ["T10", "System", "Check the decision for messages predicted as ham", "Ham messages have value 0 and are excluded"],
        ["T11", "System", "Compare the time used with the budget", "Time used does not exceed 10 minutes"],
        ["T12", "System", "Try all 2^10 combinations of the ten messages", "No feasible combination has a value above the plan"],
        ["T13", "System", "Compare each label with its probability", "Spam if and only if probability is above 50%"],
        ["T14", "System", "A genuine one-time password message", "Labelled ham"]
    ]
    create_table(t61_headers, t61_data, col_widths=[0.6, 1.1, 2.3, 2.25])
    add_p("Table 6.1: Test cases and expected results", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("6.5 Actual results and pass or fail status")
    t62_headers = ["ID", "Actual result", "Status"]
    t62_data = [
        ["T1", "Three splits with 47,392, 5,923 and 5,926 rows; columns label and text", "Pass"],
        ["T2", "No missing values and no empty text", "Pass"],
        ["T3", "Overlap between train and validation, train and test, validation and test was 0, 0 and 0", "Pass"],
        ["T4", "Shapes (38,381, 50,000), (8,225, 50,000) and (8,225, 50,000)", "Pass"],
        ["T5", "Both files loaded; classes were ham and spam", "Pass"],
        ["T6", "Maximum value 120; the third message selected; 6 minutes used", "Pass"],
        ["T7", "Spam probabilities 97.06%, 94.93% and 92.53% for the three spam messages; 5.78% and 6.66% for the two ham messages", "Pass"],
        ["T8", "Maximum value 106, 6 of 6 minutes used, 3 messages selected. Two of the selected messages were ham (see D1)", "Pass, with defect D1"],
        ["T9", "Six spam and four ham messages; maximum value 269; 10 of 10 minutes used; 3 messages selected", "Pass"],
        ["T10", "All four ham messages show value 0 and the decision EXCLUDED (HAM)", "Pass"],
        ["T11", "10 minutes used out of 10", "Pass"],
        ["T12", "The best feasible value found by trying all combinations was 269, reached by one selection only", "Pass"],
        ["T13", "All ten rows are consistent: spam rows range from 75.11% to 98.02%, ham rows from 4.76% to 23.15%", "Pass"],
        ["T14", "The message “Your OTP for login is 482916. Do not share it with anyone.” was labelled spam with probability 75.11%", "Fail"]
    ]
    create_table(t62_headers, t62_data, col_widths=[0.6, 4.8, 0.85])
    add_p("Table 6.2: Actual results and status", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)
    add_p("T12 was carried out while preparing this report by a short script that tried all 1,024 combinations of the ten messages with the values and times shown in the screenshot.")

    add_h2("6.6 Defects identified and corrections made")
    t63_headers = ["ID", "Defect", "Correction or status"]
    t63_data = [
        ["D1", "In the notebook planner (T8), values were also given to ham messages. With a tight budget, two ham messages with values 6 and 7 were selected because their review times were short, and two high-value spam messages were left out.", "In the web application, messages predicted as ham get value 0 and are excluded (T10)."],
        ["D2", "The original splits shared texts: 643 between train and validation, 624 between train and test, and 99 between validation and test. This could inflate the test score.", "Duplicates were removed and the data was split again; overlap is now zero (T3)."],
        ["D3", "One text was labelled both spam and ham.", "All rows of this text were removed."],
        ["D4", "Messages contained damaged characters and HTML entities.", "Both were repaired in a separate processed text column."],
        ["D5", "Spam is the smaller class (37.46%), and the first Logistic Regression model missed more spam than it flagged wrongly (validation recall 0.9095, precision 0.9659).", "Balanced class weights raised the validation recall to 0.9384, with precision 0.9390."],
        ["D6", "A genuine one-time password message was labelled spam (T14).", "Not corrected. Recorded as a limitation in Section 7.7."]
    ]
    create_table(t63_headers, t63_data, col_widths=[0.6, 2.8, 2.85])
    add_p("Table 6.3: Defects found and the corrections made", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("6.7 Performance or model evaluation")
    add_p("The classifier was evaluated with accuracy, precision, recall, F1-score and the confusion matrix. Precision is the share of messages predicted as spam that really are spam, recall is the share of real spam that was found, and F1 is the harmonic mean of the two. In a confusion matrix, TP and TN are the correctly predicted spam and ham messages, and FP and FN are the wrongly predicted ones.")
    add_p("Table 6.4 compares the three models on the validation set. Logistic Regression and the balanced Logistic Regression have the same accuracy. The plain model has higher precision but lower recall for spam, so more spam passes unnoticed. The balanced model gives the best F1-score for spam. Its advantage over the plain model is small (0.9387 against 0.9368), and Naive Bayes is slightly behind both. Figure 6.3 shows the same values as a chart.")

    t64_headers = ["Model", "Accuracy", "Spam precision", "Spam recall", "Spam F1"]
    t64_data = [
        ["Logistic Regression", "0.9540", "0.9659", "0.9095", "0.9368"],
        ["Logistic Regression, balanced", "0.9540", "0.9390", "0.9384", "0.9387"],
        ["Multinomial Naive Bayes", "0.9483", "0.9372", "0.9241", "0.9306"]
    ]
    create_table(t64_headers, t64_data, col_widths=[2.4, 0.95, 1.0, 0.95, 0.95])
    add_p("Table 6.4: Validation results for the spam class and overall accuracy", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_image_figure("p39_img1_529x432.png", "Figure 6.1: Validation confusion matrix of the plain Logistic Regression model", width=Inches(3.8))
    add_image_figure("p40_img1_529x432.png", "Figure 6.2: Test confusion matrix of the final balanced model", width=Inches(3.8))
    add_image_figure("p40_img2_966x738.jpeg", "Figure 6.3: Validation comparison of the three models", width=Inches(4.5))

    add_p("The balanced model was then evaluated once on the test set (Table 6.5 and Figure 6.2). Its accuracy is 0.9489, which is about half a percentage point below the validation accuracy. This small drop is normal when a model chosen on the validation set is tested on new data. Out of 5,144 ham messages, 211 (4.10%) were wrongly marked as spam, and out of 3,081 spam messages, 209 (6.78%) were missed.")

    t65_headers = ["Class", "Precision", "Recall", "F1-score", "Support"]
    t65_data = [
        ["Ham", "0.96", "0.96", "0.96", "5,144"],
        ["Spam", "0.93", "0.93", "0.93", "3,081"],
        ["Accuracy", "", "", "0.9489", "8,225"]
    ]
    create_table(t65_headers, t65_data, col_widths=[1.5, 1.2, 1.2, 1.2, 1.15])
    add_p("Table 6.5: Classification report of the final model on the test set", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 7: RESULTS AND DISCUSSION
    # =========================================================================
    add_h1("Chapter 7: Results and Discussion")
    
    add_h2("7.1 Description of the final working system")
    add_p("The final system is a web application that combines the trained classifier with the review planner. A user enters messages, review times and a budget on the home screen (Figure 4.5) and presses Run scan. The application returns an analysis page with three summary cards (maximum review value, review time used and messages selected) and a table with one row for each message.")

    add_h2("7.2 Screenshots of important outputs")
    add_p("Figure 7.1 shows the analysis page for the demonstration scan. The input consisted of ten messages, the review times 4, 2, 5, 1, 3, 2, 4, 1, 5 and 2 minutes, and a budget of 10 minutes. The page reports a maximum review value of 269, a review time used of 10 out of 10 minutes and 3 messages selected.")
    add_image_figure("p42_img1_1432x898.jpeg", "Figure 7.1: Analysis results page of the web application", width=Inches(5.0))

    add_h2("7.3 Results obtained")
    add_p("Table 7.1 repeats the table of Figure 7.1. Six messages were predicted as spam and four as ham. The ham messages were given the value 0 and excluded. Among the spam messages, the iPhone offer, the one-time password message and the free car offer were selected, with times of 4, 2 and 4 minutes and values of 98, 75 and 96. The total is 10 minutes and a value of 269.")

    t71_headers = ["No.", "Message", "Label", "Spam %", "Value", "Min", "Decision"]
    t71_data = [
        ["1", "Congratulations! You won a free iPhone. Claim your prize now!", "SPAM", "98.02", "98", "4", "SELECTED"],
        ["2", "Hey, are we still meeting for lunch today?", "HAM", "5.66", "0", "2", "EXCLUDED (HAM)"],
        ["3", "URGENT! Your bank account is blocked. Click here to verify your details.", "SPAM", "97.86", "98", "5", "NOT SELECTED"],
        ["4", "Hi Mom, I’ll be home by 7 PM.", "HAM", "13.65", "0", "1", "EXCLUDED (HAM)"],
        ["5", "WINNER! You have been selected for a $1000 gift card. Call now!", "SPAM", "92.07", "92", "3", "NOT SELECTED"],
        ["6", "Your OTP for login is 482916. Do not share it with anyone.", "SPAM", "75.11", "75", "2", "SELECTED"],
        ["7", "FREE entry to win a brand new car! Text WIN to 98765 now!", "SPAM", "95.97", "96", "4", "SELECTED"],
        ["8", "Can you send me the notes from yesterday’s class?", "HAM", "4.76", "0", "1", "EXCLUDED (HAM)"],
        ["9", "Congratulations! You have won a lottery. Pay a processing fee to claim your reward.", "SPAM", "92.90", "93", "5", "NOT SELECTED"],
        ["10", "Your electricity bill is due tomorrow. Please make the payment.", "HAM", "23.15", "0", "2", "EXCLUDED (HAM)"]
    ]
    create_table(t71_headers, t71_data, col_widths=[0.4, 2.6, 0.7, 0.7, 0.5, 0.45, 0.9])
    add_p("Table 7.1: Results of the demonstration scan", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_p("The bank account message has the same value as the iPhone message (98) but needs 5 minutes instead of 4, so it was not selected. This shows how the planner works: it maximises the total value within the budget and does not simply take the messages with the highest probability. Table 7.2 lists the five best combinations that fit into 10 minutes. The chosen combination is the only one with a value of 269.")

    t72_headers = ["Rank", "Messages", "Minutes", "Value"]
    t72_data = [
        ["1", "iPhone offer, OTP, Free car", "10", "269"],
        ["2", "iPhone offer, Gift card, OTP", "9", "265"],
        ["3", "Bank account, Gift card, OTP", "10", "265"],
        ["4", "iPhone offer, Mom, Gift card, OTP", "10", "265"],
        ["5", "iPhone offer, Gift card, OTP, Class notes", "10", "265"]
    ]
    create_table(t72_headers, t72_data, col_widths=[0.7, 3.8, 0.8, 0.95])
    add_p("Table 7.2: The five best combinations within 10 minutes (all combinations were tried)", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_p("On the held-out test set, the final classifier reached an accuracy of 94.89%, with a precision, recall and F1-score of 0.93 for spam and 0.96 for ham (Section 6.7).")

    add_h2("7.4 Comparison with objectives or baseline")
    t73_headers = ["Objective", "Outcome"]
    t73_data = [
        ["1. Prepare the dataset", "Conflicting labels, duplicates, damaged characters and split overlap were found and fixed (Table 5.3). Overlap between the final splits is zero."],
        ["2. TF-IDF and Logistic Regression", "Completed with 50,000 word and word-pair features and balanced class weights."],
        ["3. Evaluation and baseline", "Evaluated on validation and test sets. Test accuracy 0.9489. Compared with Naive Bayes, which had a spam F1 of 0.9306 against 0.9387 for the final model on the validation set."],
        ["4. Review planning with 0/1 Knapsack", "Implemented with dynamic programming. The demonstration plan reached the best possible value of 269."],
        ["5. Cloud deployment", "The system runs as a web application on Render and was used to produce the screenshots in this report."],
        ["6. Honest documentation", "Defects and limits, including the failed test T14, are recorded in Sections 6.6 and 7.7."]
    ]
    create_table(t73_headers, t73_data, col_widths=[2.1, 4.15])
    add_p("Table 7.3: Objectives and outcomes", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("7.5 Discussion of results")
    add_p("The classifier correctly handles about 19 messages out of 20, and its errors are roughly balanced between the two classes: 211 genuine messages were marked as spam and 209 spam messages were missed. For a spam filter, a false alarm can be more costly than a missed spam message, so the decision threshold could be tuned in future work. This was not done here, and the default threshold of 50% was used.")
    add_p("The Knapsack planner behaves as designed. In the demonstration it preferred the one-time password message (value 75, 2 minutes) to the bank account message (value 98, 5 minutes), because with the 10 minute budget the first combination gives a higher total (Table 7.2). This also shows a weakness of the approach. The one-time password message is genuine, but the classifier gave it a spam probability of 75.11%, so it used up 2 minutes of the review budget. The planner is only as good as the probabilities it receives.")
    add_p("The value of a message is defined as its spam probability. This is a simple choice that follows the output of the classifier. It does not say how much harm a message could do, so a different value rule, for example one that weights messages containing links more strongly, could give a more useful plan.")

    add_h2("7.6 Challenges encountered and solutions adopted")
    add_bullet("Overlap between data splits: The original splits shared hundreds of identical texts. This was solved by removing duplicates and splitting again, followed by a check that no text is shared.")
    add_bullet("Text quality: Damaged characters, HTML entities and extra spaces were repaired in a separate column, so the original text stays available.")
    add_bullet("Class imbalance: Spam is the smaller class. Balanced class weights improved the spam recall on the validation set from 0.9095 to 0.9384.")
    add_bullet("Planner choosing ham messages: In the notebook, values were also given to ham messages, which could fill the budget with harmless messages. In the web application, ham messages receive the value zero and are excluded.")
    add_bullet("Choice of the final model: Three models were compared on the validation set only, and the test set was used once for the final model, so that the reported test score is not tuned.")

    add_h2("7.7 Current limitations")
    add_bullet("The model was trained on one dataset that merges SMS, Telegram and email text. The source of each message is not recorded, so performance on each type of text was not measured.")
    add_bullet("A genuine one-time password message was labelled spam (T14). The cause was not investigated, so no explanation is claimed here.")
    add_bullet("The decision threshold is fixed at 50% and the probabilities are not calibrated.")
    add_bullet("Review value is the spam probability and does not measure the possible harm of a message. Review times are typed by the user.")
    add_bullet("Only English messages were considered, and the performance on other languages and on newer kinds of spam is unknown.")
    add_bullet("The interface takes one message per line, so a long email must be pasted as one line.")
    add_bullet("Evaluation uses one fixed split. No cross-validation or confidence intervals were computed.")
    add_bullet("Response time and the number of users the hosted service can handle were not measured.")
    add_bullet("The Knapsack planner needs whole-minute review times, and its running time grows with the product of the number of messages and the budget.")

    doc.add_page_break()

    # =========================================================================
    # CHAPTER 8: CONCLUSION AND FUTURE ENHANCEMENTS
    # =========================================================================
    add_h1("Chapter 8: Conclusion and Future Enhancements")
    
    add_h2("8.1 Summary of the project")
    add_p("This project built a spam filter and a review planner and deployed them as a web application. A public dataset of 59,241 messages was cleaned to 54,831 messages and divided into training, validation and test sets with no shared text. TF-IDF features and a class-balanced Logistic Regression classifier reached a test accuracy of 94.89%. A 0/1 Knapsack algorithm based on dynamic programming turned the spam probabilities into a review plan that gives the highest total value within the time budget.")

    add_h2("8.2 Achievement of objectives")
    add_p("All six objectives listed in Section 1.4 were met, as summarised in Table 7.3. The data was prepared and checked for leakage, the classifier was trained and evaluated on separate sets, the planner was implemented and verified on a demonstration, the system was deployed and used through a browser, and the defects and limits were recorded, including one test case (T14) that failed.")

    add_h2("8.3 Major learning outcomes")
    add_bullet("The quality of the data matters as much as the choice of the model. Finding and removing shared texts between the splits was necessary to make the test score meaningful.")
    add_bullet("Models should be compared on a validation set, and the test set should be kept for one final evaluation.")
    add_bullet("A single accuracy figure hides the kinds of mistakes made. Precision, recall and the confusion matrix gave a clearer picture, especially because spam is the smaller class.")
    add_bullet("A classic algorithm such as the 0/1 Knapsack can be combined with a machine learning model to turn predictions into a practical decision.")
    add_bullet("Deploying a model on a cloud platform requires the saved model files and the application code to be kept consistent with each other.")

    add_h2("8.4 Limitations and lessons learned")
    add_p("The main limitations are listed in Section 7.7. The most important lesson is that a result that looks good on a demonstration, such as the optimal plan of value 269, still depends on the quality of the underlying probabilities. The misclassified one-time password message showed that the planner cannot correct the mistakes of the classifier.")

    add_h2("8.5 Future enhancements")
    add_bullet("Record the source of each message and measure the performance separately for SMS, chat and email text.")
    add_bullet("Tune the decision threshold on the validation set to reduce false alarms, and calibrate the probabilities.")
    add_bullet("Add examples of genuine automated messages, such as one-time passwords and bills, to the training data and test whether the false alarms on them reduce.")
    add_bullet("Use a richer review value that also reflects the possible harm of a message, for example the presence of links or requests for money.")
    add_bullet("Use cross-validation and report confidence intervals for the metrics.")
    add_bullet("Accept multi-line emails and file uploads in the web interface.")
    add_bullet("Add automated tests for the data preparation, the planner and the web application, and monitor the hosted service.")
    add_bullet("Support more languages and retrain regularly on new examples.")

    doc.add_page_break()

    # =========================================================================
    # REFERENCES
    # =========================================================================
    add_h1("References")
    
    refs = [
        "[1] T. A. Almeida, J. M. Gómez Hidalgo, and A. Yamakami, “Contributions to the study of SMS spam filtering: New collection and results,” in Proc. 2011 ACM Symp. Document Engineering (DocEng ’11), Mountain View, CA, USA, 2011.",
        "[2] T. Almeida and J. Hidalgo, “SMS Spam Collection,” UCI Machine Learning Repository, 2011, doi: 10.24432/C5CC84. [Online]. Available: https://archive.ics.uci.edu/dataset/228/sms+spam+collection",
        "[3] M. Sahami, S. Dumais, D. Heckerman, and E. Horvitz, “A Bayesian approach to filtering junk e-mail,” in Proc. AAAI-98 Workshop on Learning for Text Categorization, 1998, pp. 55-62.",
        "[4] I. Androutsopoulos, G. Paliouras, V. Karkaletsis, G. Sakkis, C. D. Spyropoulos, and P. Stamatopoulos, “Learning to filter spam e-mail: A comparison of a Naive Bayesian and a memory-based approach,” in Proc. Workshop on Machine Learning and Textual Information Access, 4th European Conf. Principles and Practice of Knowledge Discovery in Databases (PKDD), 2000. [Online]. Available: arXiv:cs/0009009",
        "[5] C. D. Manning, P. Raghavan, and H. Schütze, Introduction to Information Retrieval. Cambridge, U.K.: Cambridge Univ. Press, 2008.",
        "[6] F. Pedregosa et al., “Scikit-learn: Machine learning in Python,” J. Mach. Learn. Res., vol. 12, pp. 2825-2830, 2011.",
        "[7] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, Introduction to Algorithms, 4th ed. Cambridge, MA, USA: MIT Press, 2022.",
        "[8] P. Mell and T. Grance, “The NIST definition of cloud computing,” National Institute of Standards and Technology, Gaithersburg, MD, USA, Spec. Publ. 800-145, Sep. 2011.",
        "[9] Render, “Web services,” Render Documentation. [Online]. Available: https://render.com/docs/web-services (accessed Oct. 26, 2026).",
        "[10] mshenoda, “spam-messages,” Hugging Face dataset card. [Online]. Available: https://huggingface.co/datasets/mshenoda/spam-messages (accessed Oct. 26, 2026)."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.line_spacing = 1.15
        p_ref.paragraph_format.space_after = Pt(6)
        p_ref.paragraph_format.left_indent = Inches(0.4)
        p_ref.paragraph_format.first_line_indent = Inches(-0.4)
        run_ref = p_ref.add_run(r)
        run_ref.font.name = 'Times New Roman'
        run_ref.font.size = Pt(10.5)

    doc.add_page_break()

    # =========================================================================
    # APPENDICES
    # =========================================================================
    add_h1("Appendix A: Source Code")
    add_p("The complete source of the model preparation is the project notebook. The wrapper function below combines prediction and review planning. It uses the Knapsack function listed in Section 5.3.5.")
    
    app_code = """import pandas as pd

def optimize_message_reviews(
    messages,
    vectorizer,
    classifier,
    review_times,
    time_budget
):
    \"\"\"
    Predict spam/ham and select messages using 0/1 Knapsack.
    Review value is spam probability * 100, rounded to an integer.
    Review times and the budget must be positive/non-negative integer minutes, respectively.
    \"\"\"
    if not messages:
        raise ValueError("Please provide at least one message.")
    if len(messages) != len(review_times):
        raise ValueError("Each message must have a corresponding review time.")
    if any(not isinstance(m, str) or not m.strip() for m in messages):
        raise ValueError("Messages must be non-empty strings.")
    if any(not isinstance(t, int) or isinstance(t, bool) or t <= 0 for t in review_times):
        raise ValueError("Review times must be positive integers.")
    if not isinstance(time_budget, int) or isinstance(time_budget, bool) or time_budget < 0:
        raise ValueError("Time budget must be a non-negative integer.")

    # 1. Transform messages using the saved TF-IDF vectorizer.
    features = vectorizer.transform(messages)

    # 2. Predict HAM or SPAM.
    predictions = classifier.predict(features)

    # 3. Obtain each message's spam probability.
    probabilities = classifier.predict_proba(features)
    classes = list(classifier.classes_)
    spam_index = next((i for i, label in enumerate(classes) if str(label).lower() == "spam"), None)

    if spam_index is None:
        raise ValueError("The classifier has no 'spam' class.")
    spam_probabilities = probabilities[:, spam_index]

    # 4. Convert probabilities into integer review values.
    values = [round(float(p) * 100) for p in spam_probabilities]

    # 5. Run the existing 0/1 Knapsack algorithm.
    max_value, selected_indices = knapsack_01(values, review_times, time_budget)
    selected_set = set(selected_indices)

    # 6. Build a readable results table.
    results = pd.DataFrame({
        "Message": messages,
        "Prediction": predictions,
        "Spam Probability (%)": [round(float(p) * 100, 2) for p in spam_probabilities],
        "Review Value": values,
        "Review Time (min)": review_times,
        "Selected for Review": [i in selected_set for i in range(len(messages))]
    })

    summary = {
        "maximum_total_value": max_value,
        "total_review_time": sum(review_times[i] for i in selected_indices),
        "time_budget": time_budget,
        "messages_selected": len(selected_indices),
        "selected_indices": selected_indices
    }
    return results, summary"""
    add_code_block(app_code)

    doc.add_page_break()

    add_h1("Appendix B: Additional Test Cases")
    add_p("The notebook contains further runs that support the results in Chapter 6.")
    
    tb1_headers = ["Run", "Input", "Result"]
    tb1_data = [
        ["B1", "Three new messages classified with the saved model: an iPhone prize message, a lunch message and a cash prize message", "SPAM, HAM, SPAM"],
        ["B2", "Five messages with a probability-based value for every message, review time 2 minutes each, budget 6 minutes", "Maximum value 285; 3 messages selected (the three spam messages); 6 minutes used"],
        ["B3", "The same five messages with times 4, 2, 5, 3, 1 and budget 6", "Maximum value 106; selected messages 2, 4 and 5 (a lunch message, the bank message and a notes message); 6 minutes used"],
        ["B4", "The wrapper function on the same input as B3", "Same selection and summary as B3: maximum value 106, selected positions 1, 3 and 4 (counting from 0)"]
    ]
    create_table(tb1_headers, tb1_data, col_widths=[0.8, 3.2, 2.25])
    add_p("Table B.1: Additional notebook runs", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    doc.add_page_break()

    add_h1("Appendix C: User Manual")
    add_h2("C.1 Using the web application")
    add_p("The web application needs no installation. Open the page in a web browser and follow these steps.")
    add_bullet("In the message box, type or paste the messages to be scanned, one message on each line.")
    add_bullet("In the review time field, enter the number of minutes needed to review each message, as whole numbers separated by commas, in the same order as the messages. Use values from 1 to 60.")
    add_bullet("In the budget field, enter the total number of minutes available for review.")
    add_bullet("Press Run scan.")
    add_bullet("Read the three summary cards: maximum review value, review time used and messages selected.")
    add_bullet("Read the table. The label shows whether the message is predicted as spam or ham, the spam probability is shown as a percentage, and the decision is SELECTED, NOT SELECTED or EXCLUDED (HAM).")
    add_p("The number of review times must equal the number of messages. Messages predicted as ham are always excluded, so the time budget is spent only on messages predicted as spam.")

    add_h2("C.2 Running the notebook")
    add_p("To repeat the model preparation, install Python 3 and the packages used by the notebook:")
    add_code_block("pip install datasets pandas scikit-learn matplotlib joblib jupyter")
    add_p("Then start Jupyter Notebook, open the project notebook and run the cells from top to bottom. The notebook downloads the dataset, cleans and splits it, trains the models, evaluates them and writes the two model files into a folder named models.")

    doc.add_page_break()

    add_h1("Appendix D: Supporting Material")
    add_h2("D.1 Dataset sources")
    add_p("According to the dataset card [10], the dataset used in this project merges the three public sources listed in Table D.1.")
    
    td1_headers = ["Source", "Kind of text"]
    td1_data = [
        ["SMS Spam Collection [1], [2]", "English text messages labelled ham or spam"],
        ["Telegram spam and ham collection", "Chat messages"],
        ["Enron email spam collection", "Email text"]
    ]
    create_table(td1_headers, td1_data, col_widths=[3.0, 3.25])
    add_p("Table D.1: Sources merged in the dataset", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("D.2 Files produced by the notebook")
    td2_headers = ["File", "Contents"]
    td2_data = [
        ["models/tfidf_vectorizer.joblib", "TF-IDF vectorizer fitted on the training messages"],
        ["models/spam_classifier.joblib", "Balanced Logistic Regression classifier"]
    ]
    create_table(td2_headers, td2_data, col_widths=[3.0, 3.25])
    add_p("Table D.2: Model files saved by the notebook", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    add_h2("D.3 Glossary")
    td3_headers = ["Term", "Meaning"]
    td3_data = [
        ["Ham", "A legitimate message"],
        ["Spam", "An unwanted message, often an unsolicited offer or a trick"],
        ["Precision", "Share of messages predicted as spam that really are spam"],
        ["Recall", "Share of real spam messages that were found"],
        ["F1-score", "Harmonic mean of precision and recall"],
        ["Review value", "The spam probability multiplied by 100 and rounded; used by the planner"],
        ["Budget", "Total minutes available for reviewing messages"]
    ]
    create_table(td3_headers, td3_data, col_widths=[2.0, 4.25])
    add_p("Table D.3: Terms used in the report", align=WD_ALIGN_PARAGRAPH.CENTER, bold=True, size=10.5)

    output_path = r"C:\Users\HP\.gemini\antigravity\scratch\activity-2\Roshni_Priyadarshini_Behera_25MSFDR009_Mini_Project_Report.docx"
    border_output_path = r"C:\Users\HP\.gemini\antigravity\scratch\activity-2\Roshni_Priyadarshini_Behera_25MSFDR009_Mini_Project_Report_With_Borders.docx"
    alt_output_path = r"C:\Users\HP\.gemini\antigravity\scratch\activity-2\Roshni_Priyadarshini_Behera_25MSFDR009_Mini_Project_Report_Updated.docx"
    
    try:
        doc.save(output_path)
        print(f"SUCCESS: Report saved successfully to:\n{output_path}")
    except PermissionError:
        print(f"NOTICE: {output_path} is currently open in Word.")

    try:
        doc.save(border_output_path)
        print(f"SUCCESS: Border report saved to:\n{border_output_path}")
    except PermissionError:
        pass

    try:
        doc.save(alt_output_path)
        print(f"SUCCESS: Updated report saved to:\n{alt_output_path}")
    except PermissionError:
        print(f"NOTICE: {alt_output_path} is currently open in Word.")

if __name__ == "__main__":
    create_report()


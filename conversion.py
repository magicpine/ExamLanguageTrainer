# Used to convert files to Text
import os


def is_pdf(filename):
    pdf_formats = ['pdf']
    return filename.rsplit('.', 1)[1].lower() in pdf_formats


def is_ppt(filename):
    ppt_formats = ['ppt', 'pptx']
    return filename.rsplit('.', 1)[1].lower() in ppt_formats


def convert_pdf_to_text(filename, UPLOAD_FOLDER):
    sys = 'pdftotext ' + UPLOAD_FOLDER+filename
    os.system(sys)


def convert_ppt_to_text(filename, UPLOAD_FOLDER):
    sys = 'soffice --headless --convert-to pdf '+UPLOAD_FOLDER+filename
    os.system(sys)
    new_filename = filename.split('.')[0] + '.pdf'
    sys = 'pdftotext ' + new_filename
    os.system(sys)
    os.system('rm -f ' + new_filename)


def convert_doc_to_text(filename, UPLOAD_FOLDER):
    sys = 'soffice --headless --convert-to txt:Text '+UPLOAD_FOLDER+filename
    os.system(sys)

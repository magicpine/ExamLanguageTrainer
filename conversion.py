# Used to convert files to Text
import os


def is_pdf(filename):
    ''' Checks to see if the file is a pdf
        Returns true if it is '''
    pdf_formats = ['pdf']
    return filename.rsplit('.', 1)[1].lower() in pdf_formats


def is_ppt(filename):
    ''' Checks to see if the file is a powerpoint
        returns true if it is '''
    ppt_formats = ['ppt', 'pptx']
    return filename.rsplit('.', 1)[1].lower() in ppt_formats


def convert_pdf_to_text(filename, UPLOAD_FOLDER):
    ''' Converts any pdf into a text file '''
    sys = 'pdftotext ' + UPLOAD_FOLDER+filename
    os.system(sys)


def convert_ppt_to_text(filename, UPLOAD_FOLDER):
    ''' Converts any powerpoint into a text file '''
    # First convert into a pdf
    sys = 'soffice --headless --convert-to pdf '+UPLOAD_FOLDER+filename
    os.system(sys)
    new_filename = filename.split('.')[0] + '.pdf'
    # Take the PDF and convert that into a text file
    sys = 'pdftotext ' + new_filename
    os.system(sys)
    os.system('rm -f ' + new_filename)


def convert_doc_to_text(filename, UPLOAD_FOLDER):
    ''' Convert any document file into a text file '''
    sys = 'soffice --headless --convert-to txt:Text '+UPLOAD_FOLDER+filename
    os.system(sys)

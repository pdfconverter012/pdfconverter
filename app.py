from flask import Flask, request, send_file, render_template
import PyPDF2
import os

app = Flask(__name__)

def combine_pdfs(front_pdf_path, back_pdf_path, output_pdf_path):
    front_pdf = PyPDF2.PdfReader(open(front_pdf_path, "rb"))
    back_pdf = PyPDF2.PdfReader(open(back_pdf_path, "rb"))
    output_pdf = PyPDF2.PdfWriter()

    num_front_pages = len(front_pdf.pages)
    num_back_pages = len(back_pdf.pages)

    if num_front_pages != num_back_pages:
        raise ValueError("Die Anzahl der Seiten in den beiden PDFs muss übereinstimmen.")

    for i in range(num_front_pages):
        output_pdf.add_page(front_pdf.pages[i])
        output_pdf.add_page(back_pdf.pages[num_back_pages - 1 - i])

    with open(output_pdf_path, "wb") as output_file:
        output_pdf.write(output_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'front' not in request.files or 'back' not in request.files:
        return 'Es müssen zwei Dateien hochgeladen werden', 400

    front_file = request.files['front']
    back_file = request.files['back']

    front_path = os.path.join('uploads', 'front.pdf')
    back_path = os.path.join('uploads', 'back.pdf')
    output_path = os.path.join('uploads', 'combined.pdf')

    front_file.save(front_path)
    back_file.save(back_path)

    try:
        combine_pdfs(front_path, back_path, output_path)
    except ValueError as e:
        return str(e), 400

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)


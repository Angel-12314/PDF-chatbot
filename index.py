from flask import Flask, request, render_template
import PyPDF2

app = Flask(__name__)

# Function to extract text from the uploaded PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
    if file.filename == '':
        return "No selected file"
    
    if file and file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(file)
        return render_template('query.html', text=text)
    
    return "Invalid file format. Please upload a PDF."

@app.route('/query', methods=['POST'])
def answer_query():
    text = request.form['text']
    query = request.form['query']
    
    if query.lower() in text.lower():
        start_idx = text.lower().find(query.lower())
        snippet = text[start_idx:start_idx+300]  # Show some context from the query
        return f"Query found! Here's the context: <br><br>{snippet}"
    else:
        return "Sorry, your query was not found in the document."

if __name__ == '__main__':
    app.run(debug=True)
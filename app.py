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

    def get_snippet(text, query, snippet_length=300):
        start_idx = text.lower().find(query.lower())
        
        # Find the nearest space before and after the snippet to avoid splitting words
        snippet_start = max(0, text.rfind(' ', 0, start_idx))
        snippet_end = text.find(' ', start_idx + snippet_length)

        # If there's no space after, take the end of the text
        if snippet_end == -1:
            snippet_end = len(text)

        # Extract the snippet with full words
        snippet = text[snippet_start:snippet_end]
        
        return snippet  # Ensure return happens here in all cases
    
    # Check if the query exists in the text
    if query.lower() in text.lower():
        snippet = get_snippet(text, query, snippet_length=300)  # Call the function to get the snippet
        #return f"Query found! Here's the context: <br><br>{snippet}"
        return render_template('result.html', snippet=snippet, query=query)
    else:
        #return "Sorry, your query was not found in the document."
        return render_template('result.html', error_message = 'Sorry, your query was not found in the document.')
            
                #return snippet

        #snippet = text[start_idx:start_idx+301]  # Show some context from the query
  
    

if __name__ == '__main__':
    app.run(debug=True)

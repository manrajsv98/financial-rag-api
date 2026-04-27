from pypdf import PdfReader

def load_pdf(file_path: str):
    reader = PdfReader(file_path)
    # reader.pages now have access to page object but need to do

        # reader.pages
        #     ↓
        # [
        # PageObject(page 1),
        # PageObject(page 2),
        # PageObject(page 3)
        # ]

    # page.extract_text() to extract text from the page. 


    documents = []

    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()

        if text:  # skip empty pages
            documents.append({
                "text": text,
                "metadata": {
                    "source": file_path,
                    "page": page_number + 1
                }
            })
    return documents 
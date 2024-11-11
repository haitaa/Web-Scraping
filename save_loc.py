import os

def save_to_csv(content, filename="output.csv"):
    documents_path = os.path.expanduser("/Users/mustafahaita/Documents/AI Webscraper/documents")
    
    # Hedef dizin mevcut değilse oluşturun
    if not os.path.exists(documents_path):
        os.makedirs(documents_path)

    # Dosyanın tam yolunu oluşturun
    file_path = os.path.join(documents_path, filename)

    with open(file_path, "w", newline="", encoding="utf-8") as file:
        file.write(content)
import PyPDF2

# Список PDF файлов для объединения
pdf_files = ["1.pdf", "2.pdf", "3.pdf", "4.pdf"]

# Создаем объект объединенного PDF
merged_pdf = PyPDF2.PdfFileMerger()

# Объединяем каждый PDF файл в объект merged_pdf
for file in pdf_files:
    with open(file, "rb") as pdf:
        merged_pdf.append(pdf)

# Сохраняем объединенный PDF в новый файл
with open("4-готовый.pdf", "wb") as output:
    merged_pdf.write(output)

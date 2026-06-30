from input_handler import extract_text_from_pdf
from similarity import calculate_similarity

text1 = extract_text_from_pdf("uploads/file1.pdf")
text2 = extract_text_from_pdf("uploads/file2.pdf")

percentage = calculate_similarity(text1, text2)

print(f"Plagiarism Percentage: {percentage}%")
from flask import Flask, render_template, request
import os

from input_handler import extract_text_from_pdf
from ai_similarity import hybrid_similarity

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/compare", methods=["POST"])
def compare():

    files = request.files.getlist("pdf_files")

    paths = []

    for file in files:
        if file.filename == "":
            continue

        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)
        paths.append(path)

    if len(paths) < 2:
        return "Upload at least 2 PDFs"

    # Extract text
    texts = []
    for path in paths:
        texts.append(extract_text_from_pdf(path))

    results = []

    n = len(texts)

    high = 0
    medium = 0
    low = 0

    for i in range(n):
        for j in range(i + 1, n):

            score, matches = hybrid_similarity(texts[i], texts[j])

            if score > 70:
                high += 1
            elif score > 40:
                medium += 1
            else:
                low += 1

            results.append({
                "file1": os.path.basename(paths[i]),
                "file2": os.path.basename(paths[j]),
                "similarity": round(score, 2),
                "matches": matches
            })

    return render_template(
        "result.html",
        results=results,
        high=high,
        medium=medium,
        low=low
    )


if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
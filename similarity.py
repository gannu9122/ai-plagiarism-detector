import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Overall PDF Similarity
def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform([text1, text2])

    similarity = cosine_similarity(vectors)

    percentage = similarity[0][1] * 100

    return round(percentage, 2)


# Split text into sentences
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


# Find similar sentences
def compare_sentences(text1, text2, threshold=70):
    sent1 = split_sentences(text1)
    sent2 = split_sentences(text2)

    if not sent1 or not sent2:
        return []

    # TF-IDF for all sentences together
    all_sentences = sent1 + sent2

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(all_sentences)

    # Similarity Matrix
    sim_matrix = cosine_similarity(tfidf)

    matches = []

    offset = len(sent1)

    # Compare every sentence of File1 with File2
    for i in range(len(sent1)):

        best_score = 0
        best_sentence = ""

        for j in range(len(sent2)):

            score = sim_matrix[i][offset + j] * 100

            if score > best_score:
                best_score = score
                best_sentence = sent2[j]

        if best_score >= threshold:
            matches.append({
                "sentence1": sent1[i],
                "sentence2": best_sentence,
                "score": round(best_score, 2)
            })

    return matches
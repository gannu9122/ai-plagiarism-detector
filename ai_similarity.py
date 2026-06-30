from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

model = SentenceTransformer('all-MiniLM-L6-v2')


def split_sentences(text):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]


def hybrid_similarity(text1, text2):

    sent1 = split_sentences(text1)
    sent2 = split_sentences(text2)

    # TF-IDF global similarity
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([text1, text2])
    tfidf_score = cosine_similarity(tfidf)[0][1]

    # Semantic similarity
    emb1 = model.encode(sent1)
    emb2 = model.encode(sent2)

    matches = []

    for i, e1 in enumerate(emb1):

        best_score = 0
        best_sentence = ""

        for j, e2 in enumerate(emb2):

            score = cosine_similarity([e1], [e2])[0][0]

            if score > best_score:
                best_score = score
                best_sentence = sent2[j]

        if best_score >= 0.75:
            matches.append({
                "sentence1": sent1[i],
                "sentence2": best_sentence,
                "score": round(best_score * 100, 2)
            })

    # Final weighted score
    final_score = (tfidf_score * 0.4 + sum([m["score"]/100 for m in matches]) / max(len(matches), 1) * 0.6) * 100

    return round(final_score, 2), matches
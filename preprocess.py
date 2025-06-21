import pandas as pd
import re
import nltk
import joblib
import logging
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("preprocess.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logging.info("🚀 Starting preprocessing...")

nltk.download('punkt')
nltk.download('stopwords')

# Load and sample dataset
try:
    df = pd.read_csv("spotify_millsongdata.csv").sample(10000)
    logging.info("✅ Dataset loaded and sampled: %d rows", len(df))
except Exception as e:
    logging.error("❌ Failed to load dataset: %s", str(e))
    raise e

# Drop link column and preprocess
df = df.drop(columns=['link'], errors='ignore').reset_index(drop=True)

# Text cleaning
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = re.sub(r"[^a-zA-Z\s]", "", str(text))
    text = text.lower()
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)

logging.info("🧹 Cleaning text...")
df['cleaned_text'] = df['text'].apply(preprocess_text)
logging.info("✅ Text cleaned.")

# Vectorization
logging.info("🔠 Vectorizing using TF-IDF...")
tfidf = TfidfVectorizer(max_features=5000)
tfidf_matrix = tfidf.fit_transform(df['cleaned_text'])
logging.info("✅ TF-IDF matrix shape: %s", tfidf_matrix.shape)

# Cosine similarity matrix (for full dataset similarity, if needed)
logging.info("📐 Calculating cosine similarity matrix for dataset...")
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
logging.info("✅ Cosine similarity matrix generated.")

# Save everything
joblib.dump(df, 'df_cleaned.pkl')
joblib.dump(tfidf_matrix, 'tfidf_matrix.pkl')
joblib.dump(cosine_sim, 'cosine_sim.pkl')
joblib.dump(tfidf, 'vectorizer.pkl')  # Save vectorizer for later input transforms
logging.info("💾 Data saved to disk.")

# New: input validation function
def is_valid_input(text):
    if not isinstance(text, str):
        return False
    cleaned = re.sub(r"[^a-zA-Z\s]", "", text).strip()
    return len(cleaned) > 0

# New: function to find and print top similar songs for any input text
def find_similar_songs(user_input, top_n=5):
    if not is_valid_input(user_input):
        print("Invalid input")
        return
    
    processed_input = preprocess_text(user_input)
    input_vec = tfidf.transform([processed_input])
    sim_scores = cosine_similarity(input_vec, tfidf_matrix).flatten()
    top_indices = sim_scores.argsort()[-top_n:][::-1]
    
    print(f"\nTop {top_n} similar songs:")
    for idx in top_indices:
        song_text = df.loc[idx, 'text']
        score = sim_scores[idx]
        print(f"Score: {score:.3f}  -  Song lyrics: {song_text}")

logging.info("✅ Preprocessing complete.")

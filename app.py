import spacy
import streamlit as st
import string

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Load the text file
try:
    with open('book for checkpoint.txt', 'r', encoding='utf-8') as f:
        data = f.read().replace('\n', ' ')
except FileNotFoundError:
    st.error("Error: 'book for checkpoint.txt' not found.")
    data = ""

# Tokenize the text into sentences
doc = nlp(data)
sentences = [sent.text for sent in doc.sents]

# Define a function to preprocess each sentence
def preprocess(text):
    doc = nlp(text)
    words = [
        token.lemma_.lower() for token in doc
        if not token.is_stop and token.is_alpha
    ]
    return words

# Preprocess each sentence in the text
corpus = [preprocess(sentence) for sentence in sentences]

# Define a function to find the most relevant sentence given a query
def get_most_relevant_sentence(query):
    query_tokens = set(preprocess(query))
    max_similarity = 0
    most_relevant_sentence = ""

    for sentence, original_sentence in zip(corpus, sentences):
        if not sentence:
            continue

        sentence_tokens = set(sentence)
        similarity = len(query_tokens & sentence_tokens) / max(1, len(query_tokens | sentence_tokens))

        if similarity > max_similarity:
            max_similarity = similarity
            most_relevant_sentence = original_sentence  # Keep the original sentence format

    return most_relevant_sentence if most_relevant_sentence else "I couldn't find a relevant answer."

# Define the chatbot function
def chatbot(question):
    return get_most_relevant_sentence(question)

# Streamlit App
st.title("Simple NLP Chatbot (spaCy)")

user_input = st.text_input("Ask a question:")
if st.button("Get Answer"):
    response = chatbot(user_input)
    st.write("Chatbot:", response)

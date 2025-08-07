import gradio as gr
from cryptography.fernet import Fernet
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import nltk
import uuid
import os
import datetime
import re

nltk.download('punkt')

# Hindi stopwords (basic list, zarurat anusar badha sakte ho)
hindi_stopwords = [
    'और', 'का', 'के', 'की', 'है', 'को', 'से', 'पर', 'बल्कि', 'भी', 'था', 'थे',
    'था', 'ना', 'इस', 'मैं', 'हो', 'तो', 'कि', 'जो', 'वे', 'हम', 'ये', 'कि', 'थे'
]

# Language-specific sentence tokenizer
def hindi_sentence_tokenize(text):
    # Hindi sentences mostly '।', '?', '!' se khatam hote hain
    sentences = re.split(r'[।!?]+', text)
    # Extra whitespace hatao
    sentences = [s.strip() for s in sentences if s.strip()]
    return sentences

def multi_lang_tokenize(text, lang='english'):
    if lang == 'english':
        return nltk.tokenize.sent_tokenize(text)
    elif lang == 'hindi':
        return hindi_sentence_tokenize(text)
    else:
        return nltk.tokenize.sent_tokenize(text)

def tfidf_summarize_keywords(text, n=3, k=5, lang='english'):
    sentences = multi_lang_tokenize(text, lang)
    if not sentences:
        return "", ""

    # Setup stopwords based on language
    if lang == 'english':
        stop_words = 'english'
    elif lang == 'hindi':
        stop_words = hindi_stopwords
    else:
        stop_words = None

    vectorizer = TfidfVectorizer(stop_words=stop_words)
    tfidf_matrix = vectorizer.fit_transform(sentences)
    sentence_scores = tfidf_matrix.sum(axis=1).A1
    top_n_idx = np.argsort(sentence_scores)[-n:][::-1]
    summary = [sentences[i] for i in sorted(top_n_idx)]

    feature_array = np.array(vectorizer.get_feature_names_out())
    tfidf_sum = tfidf_matrix.sum(axis=0).A1
    keywords = feature_array[np.argsort(tfidf_sum)[-k:][::-1]]

    return ' '.join(summary), ', '.join(keywords)

# Encryption key generation and cipher object creation
key = Fernet.generate_key()  # User ko store kar lena chaiye ye key
cipher = Fernet(key)

def summarize_and_encrypt(text, n, k, lang):
    if not text.strip():
        return "", "", None, key.decode(), "Input text cannot be empty."

    summary, keywords = tfidf_summarize_keywords(text, n, k, lang)
    if not summary:
        return "", "", None, key.decode(), "Could not generate summary - input may be too short or invalid."

    encrypted = cipher.encrypt(summary.encode())

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"enc_summary_{lang}_{timestamp}_{uuid.uuid4().hex[:6]}.bin"
    with open(filename, "wb") as f:
        f.write(encrypted)
    abs_path = os.path.abspath(filename)

    return summary, keywords, abs_path, key.decode(), "Summary generated and encrypted successfully!"

def decrypt_uploaded(file_obj, user_key):
    if file_obj is None or not user_key.strip():
        return "Please upload an encrypted file and provide a secret key."
    try:
        cipher2 = Fernet(user_key.encode())
        with open(file_obj.name, "rb") as f:
            enc = f.read()
        dec = cipher2.decrypt(enc).decode()
        return dec
    except Exception as e:
        return f"Error: Decryption failed. {str(e)}"

with gr.Blocks() as demo:
    gr.Markdown("## 🔐 Privacy-First Multi-language Summary App (Encryption integrated)")

    with gr.Tab("Summarize & Encrypt"):
        inp = gr.Textbox(lines=8, placeholder="Yahan apna text paste karo...", label="Input Text")
        lang_inp = gr.Dropdown(choices=['english', 'hindi'], value='english', label="Select Language")
        n_inp = gr.Slider(minimum=1, maximum=10, value=3, step=1, label="Summary Sentence Count")
        k_inp = gr.Slider(minimum=1, maximum=10, value=5, step=1, label="Keywords Count")
        btn = gr.Button("Summarize & Encrypt")

        out_summary = gr.Textbox(label="Summary", interactive=False)
        out_keywords = gr.Textbox(label="Keywords", interactive=False)
        out_file = gr.File(label="Download Encrypted Summary")
        key_out = gr.Textbox(label="Your Secret Key (SAVE THIS!)", interactive=False)
        status = gr.Textbox(label="Status Message", interactive=False)

        btn.click(
            summarize_and_encrypt,
            inputs=[inp, n_inp, k_inp, lang_inp],
            outputs=[out_summary, out_keywords, out_file, key_out, status]
        )

    with gr.Tab("Decrypt Uploaded Summary"):
        upload = gr.File(label="Upload Encrypted Summary File (.bin)")
        key_in = gr.Textbox(label="Paste your Secret Key")
        decrypt_btn = gr.Button("Decrypt")
        decrypt_out = gr.Textbox(label="Decrypted (original) Summary", interactive=False)
        decrypt_status = gr.Textbox(label="Status", interactive=False)
        decrypt_btn.click(
            decrypt_uploaded,
            inputs=[upload, key_in],
            outputs=[decrypt_out]
        )

    gr.Markdown("Made with ❤️ by You! Apni summaries ko private aur secure rakhein.")

demo.launch(share=True)

import nltk
from nltk.util import ngrams
from nltk.tokenize import sent_tokenize
import re
from collections import Counter
import pandas as pd
import plotly.express as px
import time
import os
import ssl

def format_size(size_bytes):
    """Format size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} GB"

def ensure_nltk_data():
    """Ensure all required NLTK data is downloaded."""
    # First, try to create an unverified SSL context for downloads
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    # Clear any existing corrupted downloads
    nltk_data_dir = os.path.expanduser('~/nltk_data')
    if os.path.exists(nltk_data_dir):
        for subdir in ['tokenizers', 'taggers', 'corpora']:
            path = os.path.join(nltk_data_dir, subdir)
            if os.path.exists(path):
                try:
                    import shutil
                    shutil.rmtree(path)
                    print(f"Cleaned up {path}")
                except Exception as e:
                    print(f"Could not clean up {path}: {e}")

    # List of required NLTK packages
    packages = [
        ('punkt', 'Punkt Tokenizer'),
        ('averaged_perceptron_tagger', 'Perceptron Tagger'),
        ('stopwords', 'Stopwords'),
        ('wordnet', 'WordNet'),
        ('omw-1.4', 'Open Multilingual WordNet')
    ]

    print("\nDownloading NLTK data packages:")
    for package, description in packages:
        print(f"\nProcessing {description}...")
        try:
            nltk.download(package, quiet=True, raise_on_error=True)
            print(f"✓ Successfully downloaded {description}")
        except Exception as e:
            print(f"× Failed to download {description}: {e}")
            # Try alternative download method
            try:
                import urllib.request
                url = f"https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/{package}.zip"
                save_path = os.path.join(nltk_data_dir, f"{package}.zip")
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                urllib.request.urlretrieve(url, save_path)
                print(f"✓ Successfully downloaded {description} using alternative method")
            except Exception as e2:
                print(f"× Failed alternative download for {description}: {e2}")

    print("\nNLTK data download process completed.")
    print(f"Data directory: {nltk_data_dir}")

# Initialize NLTK data when module is imported
try:
    ensure_nltk_data()
except Exception as e:
    print(f"Warning: Error during NLTK data initialization: {e}")
    print("The application will continue with limited functionality.")

# Common stopwords from main app
STOPWORDS = {
    'the', 'is', 'in', 'a', 'an', 'and', 'of', 'to', 'it', 'on', 'for', 'with', 'that', 'this',
    'as', 'are', 'was', 'were', 'by', 'be', 'am', 'at', 'or', 'from', 'but', 'not', 'have', 'has',
    'had', 'do', 'does', 'did', 'so', 'if', 'out', 'up', 'down', 'about', 'into', 'over', 'then',
    'its', "it's"
}

def tokenize(text):
    """Split text into tokens and clean punctuation."""
    return [word.strip(".,()[]{}<>\"':;!?\n") for word in text.split()]

def filter_stopwords(tokens):
    """Remove stopwords from token list."""
    return [word.lower() for word in tokens if word.lower() not in STOPWORDS]

def analyze_sentence_structure(text):
    """Analyze the structure of sentences in the text."""
    try:
        sentences = sent_tokenize(text)
    except Exception as e:
        print(f"Warning: Error in sentence tokenization: {e}")
        # Fallback to simple sentence splitting
        sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    patterns = []
    for sentence in sentences:
        try:
            length = len(sentence.split())
            has_comma = ',' in sentence
            ends_with = sentence[-1] if sentence else ''
            patterns.append({
                'length': length,
                'has_comma': has_comma,
                'ending': ends_with
            })
        except Exception as e:
            print(f"Warning: Error analyzing sentence: {e}")
            continue
    return patterns

def get_ngrams(text, n=3):
    """Generate n-grams from text."""
    tokens = tokenize(text)
    n_grams = list(ngrams(tokens, n))
    return [' '.join(gram) for gram in n_grams]

def detect_paraphrasing(text1, text2):
    """Detect potential paraphrasing between two texts."""
    sent_struct_1 = analyze_sentence_structure(text1)
    sent_struct_2 = analyze_sentence_structure(text2)
    
    struct_similarity = len(set(str(sent_struct_1)) & set(str(sent_struct_2))) / \
                       max(len(str(sent_struct_1)), len(str(sent_struct_2)))
    
    words1 = set(filter_stopwords(tokenize(text1)))
    words2 = set(filter_stopwords(tokenize(text2)))
    
    word_overlap = len(words1.intersection(words2)) / max(len(words1), len(words2))
    
    return (struct_similarity + word_overlap) / 2

def find_citations(text):
    """Find citation patterns in text."""
    patterns = [
        r'\(\w+,\s*\d{4}\)',  # (Author, YYYY)
        r'\[\d+\]',           # [1]
        r'(?<!\w)et al\.',    # et al.
        r'\d+\.\s*\w+',       # 1. Reference
    ]
    
    citations = []
    for pattern in patterns:
        matches = re.finditer(pattern, text)
        citations.extend([m.group() for m in matches])
    
    return citations

def generate_text_statistics(text):
    """Generate comprehensive statistics for a text."""
    try:
        words = tokenize(text)
    except Exception as e:
        print(f"Warning: Error in word tokenization: {e}")
        words = text.split()
    
    try:
        sentences = sent_tokenize(text)
    except Exception as e:
        print(f"Warning: Error in sentence tokenization: {e}")
        sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    try:
        stats = {
            'Word Count': len(words),
            'Sentence Count': len(sentences),
            'Average Words per Sentence': round(len(words) / len(sentences), 2) if sentences else 0,
            'Unique Words': len(set(words)),
            'Character Count': len(text),
        }
        
        word_freq = Counter(filter_stopwords(words))
        most_common = dict(word_freq.most_common(10))
        
    except Exception as e:
        print(f"Warning: Error generating statistics: {e}")
        stats = {
            'Word Count': 0,
            'Sentence Count': 0,
            'Average Words per Sentence': 0,
            'Unique Words': 0,
            'Character Count': 0,
        }
        most_common = {}
    
    return stats, most_common

def visualize_comparison(text1, text2, filename1, filename2):
    """Generate visualization comparing two texts."""
    try:
        stats1, freq1 = generate_text_statistics(text1)
        stats2, freq2 = generate_text_statistics(text2)
        
        # Statistics comparisonx
        stats_df = pd.DataFrame({
            filename1: stats1,
            filename2: stats2
        }).reset_index()
        stats_df.columns = ['Metric', 'File 1', 'File 2']
        
        fig_stats = px.bar(stats_df, 
                          x='Metric', 
                          y=['File 1', 'File 2'],
                          barmode='group',
                          title='Document Statistics Comparison')
        
        # Word frequency comparison
        freq_df = pd.DataFrame({
            f'Top Words in {filename1}': freq1,
            f'Top Words in {filename2}': freq2
        }).fillna(0)
        
        fig_freq = px.bar(freq_df,
                         barmode='group',
                         title='Most Common Words Comparison')
        
        return fig_stats, fig_freq
    except Exception as e:
        print(f"Warning: Error in visualization: {e}")
        # Return empty figures as fallback
        empty_fig = px.bar(pd.DataFrame({'x': [0], 'y': [0]}))
        return empty_fig, empty_fig 
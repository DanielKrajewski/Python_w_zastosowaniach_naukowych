import argparse
from collections import Counter
from ascii_graph import Pyasciigraph
from rich.console import Console
import tqdm
import re

import collections
from _collections_abc import Iterable 
collections.Iterable = Iterable

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        exit(1)

def clean_and_split_text(text, min_word_length):
    words = re.findall(r"\b\w+\b", text.lower())
    return [word for word in words if len(word) >= min_word_length]

def create_histogram(words, top_n):
    word_counts = Counter(words)
    most_common = word_counts.most_common(top_n)

    histogram_data = []
    for word, count in tqdm.tqdm(most_common, desc="Processing words"):
        histogram_data.append((word, count))

    return histogram_data

def display_histogram(histogram_data):
    graph = Pyasciigraph()
    for line in graph.graph('Word Frequency Histogram', histogram_data):
        print(line)


parser = argparse.ArgumentParser(description="Generate a word frequency histogram from a text file.")
parser.add_argument("file", help="Path to the text file.")
parser.add_argument("--top","-t", type=int, default=10, help="Number of top words to display in the histogram (default: 10).")
parser.add_argument("--min-length","-ml", type=int, default=0, help="Minimum word length to include in the histogram (default: 0).")
args = parser.parse_args()

console = Console()
console.print("[bold green]Reading file...[/bold green]")
text = read_file(args.file)

console.print("[bold green]Processing text...[/bold green]")
words = clean_and_split_text(text, args.min_length)

console.print("[bold green]Creating histogram...[/bold green]")
histogram_data=create_histogram(words,args.top)

console.print("[bold green]Displaying histogram...[/bold green]")
display_histogram(histogram_data)

#poetry run python lab01.py wiedzmin.txt -t 10 -ml 5
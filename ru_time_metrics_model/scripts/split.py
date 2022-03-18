"""Convert textcat annotation from JSONL to spaCy v3 .spacy format."""
import srsly
import typer
import warnings
from pathlib import Path

import spacy
from spacy.tokens import DocBin


def split(input_path: Path):
    cwd = Path.cwd() 
    out_path = cwd / 'corpus' / 'train.spacy'
    print(out_path)

if __name__ == "__main__":
    typer.run(split)

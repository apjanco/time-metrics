import srsly
import typer
import csv
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
import spacy

def make_cats(date:str):
    entry_date = datetime.strptime(date, "%Y-%m-%d")
    february1917 = datetime.strptime("1917-03-08", "%Y-%m-%d")
    december1991 = datetime.strptime("1991-12-26", "%Y-%m-%d")

    # Is pre-February 1917
    if entry_date < february1917:
        return {"EMPIRE": 1.0, "SOVIET": 0.0, "POST": 0.0}
    if february1917 < entry_date < december1991:    
        return {"EMPIRE": 0.0, "SOVIET": 1.0, "POST": 0.0}
    if entry_date > december1991:
        return {"EMPIRE": 0.0, "SOVIET": 0.0, "POST": 1.0}
    else:
        return None, None

def read_timeline(input_path:str, model: str):
    total = len(list(srsly.read_jsonl(input_path)))
    typer.echo(typer.style(f"⭐ Running read timeline of {total} entries", fg=typer.colors.BRIGHT_MAGENTA, bold=True))
    nlp =spacy.load(model)

    with open('./corpus/timeline_output.csv', mode='w') as csv_file:
        fieldnames = ['id', 'date', 'author', 'diary', 'empire', 'soviet', 'post',]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
    
        timeline = srsly.read_jsonl(input_path)
        
        for line in tqdm(timeline, total=total):
            row = {}
            doc = nlp(line["text"])
            cats = doc.cats
            row['id'] = line["id"]
            row['date'] = line["date"]
            row['author'] = line["author"]
            row['diary'] = line["diary"]
            row['empire'] = cats["EMPIRE"]
            row['soviet'] = cats["SOVIET"]
            row['post'] = cats["POST"]
            writer.writerow(row)        
            
    typer.echo(typer.style(f"⭐ Done", fg=typer.colors.BRIGHT_CYAN, bold=True))



if __name__ == "__main__":
    typer.run(read_timeline)



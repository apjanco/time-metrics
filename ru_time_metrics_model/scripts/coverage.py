import srsly
import typer
import collections
from pathlib import Path
from datetime import datetime, timedelta
from typing import List 
from tqdm import tqdm

def timeline_coverage(dates:List, start, end):
   
    total_days = (end - start).days
    
    c = collections.Counter(dates)
    entries_weighted = 0
    for date in set(dates):
        entries_weighted += c[date]

    return entries_weighted / total_days

def simple_average(dates:List, start, end):
    total_days = (end - start).days
    date_range = [end - timedelta(days=x) for x in range(total_days)]
    #convert to comparable strings
    date_range = [d.strftime("%Y-%m-%d") for d in date_range]
    c = collections.Counter(dates)
    sum = 0
    for date in date_range:
        sum += c[date]
    return sum / total_days
    

    return entries_weighted / total_days

def lifetime_coverage(entries, birth, death):
    total_days_lived = (death - birth).days
    
    entry_dates = [e.get('fields',None).get('date_start',None) for e in entries]
    c = collections.Counter(entry_dates)
    entries_weighted = 0
    for date in set(entry_dates):
        entries_weighted += c[date]

    if total_days_lived > 0:
        return entries_weighted / total_days_lived


def coverage(start:str='1800-01-01', end:str='2018-01-01'):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    total_days = (end - start).days
    #total_date_range = [end - timedelta(days=x) for x in range(total_days)]
    
    # get counds for each date
    dates = []
    data = srsly.read_json("assets/entries.json")
    for entry in data:
        date = entry.get('fields',None).get('date_start', None)
        if date: 
            dates.append(date)
    
    time_coverage = timeline_coverage(dates, start, end)
    print('[*] timeline coverage: ',time_coverage)
    average = simple_average(dates, start, end)
    print('[*] simple average: ', average)

    people = srsly.read_json("assets/people.json")
    people_out = """"""
    for person in tqdm(people): 
        author = person.get('pk', None)
        birth = person.get('fields',None).get('birth_date',None)
        death = person.get('fields',None).get('death_date',None)
        if birth and death:
            birth = datetime.strptime(birth, "%Y-%m-%d")
            death = datetime.strptime(death, "%Y-%m-%d")

            entries = [e for e in data if e.get('fields',None).get('author',None) == author]
            life_coverage = lifetime_coverage(entries,birth, death)
            people_out += f'{author}, {life_coverage}\n'
    Path('people_coverage.csv').write_text(people_out)


if __name__ == "__main__":
    typer.run(coverage)

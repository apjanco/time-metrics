import srsly
import typer
import random
from pathlib import Path
from datetime import datetime
from tqdm import tqdm
from sklearn.model_selection import train_test_split


def make_cats(date:str):
    entry_date = datetime.strptime(date, "%Y-%m-%d")
    february1917 = datetime.strptime("1917-03-08", "%Y-%m-%d")
    december1991 = datetime.strptime("1991-12-26", "%Y-%m-%d")

    # Is pre-February 1917
    if entry_date < february1917:
        return 'empire',{"EMPIRE": 1.0, "SOVIET": 0.0, "POST": 0.0}
    if february1917 < entry_date < december1991:    
        return 'soviet',{"EMPIRE": 0.0, "SOVIET": 1.0, "POST": 0.0}
    if entry_date > december1991:
        return 'post', {"EMPIRE": 0.0, "SOVIET": 0.0, "POST": 1.0}
    else:
        return None, None

def load_json(input_path: Path, test_size: float, random_state: int, examples: int):
    
    empire = []
    soviet = []
    post = []

    typer.echo(typer.style("⭐ Processing diary entries", fg=typer.colors.GREEN, bold=True))
    for line in tqdm(srsly.read_json(input_path)):
        date = line.get('fields',None).get('date_start',None)
        if date is not None:
            row = {}
            row['id'] = line.get('pk',None)
            row['date'] = date
            row['text'] = line.get('fields',None).get('text',None)
            # removed to create a public dataset
            #row['author'] = line.get('fields',None).get('author',None)
            #row['diary'] = line.get('fields',None).get('diary',None)
            label, row['cats'] = make_cats(date)
            if label == 'empire':
                empire.append(row)
            elif label == 'soviet':
                soviet.append(row)
            elif label == 'post':
                post.append(row)

    typer.echo(typer.style(f"⭐ Created {len(empire)} Empire, {len(soviet)} Soviet, {len(post)} post-Soviet docs", fg=typer.colors.GREEN, bold=True))        

        
    empire = random.sample(empire, k=examples)
    empire_train, empire_val = train_test_split(
        empire, test_size=test_size, random_state=random_state
    )

    soviet = random.sample(soviet, k=examples)
    soviet_train, soviet_val = train_test_split(
        soviet, test_size=test_size, random_state=random_state
    )

    post = random.sample(post, k=examples)
    post_train, post_val = train_test_split(
         post, test_size=test_size, random_state=random_state
    )

    train_set = empire_train + soviet_train + post_train
    val_set = empire_val + soviet_val + post_val
    typer.echo(typer.style(f"⭐ Created {len(train_set)} training docs and {len(val_set)} validation docs", fg=typer.colors.GREEN, bold=True))        
    

    srsly.write_jsonl("time-metrics/ru_time_metrics_model/assets/train.jsonl", train_set)
    srsly.write_jsonl('time-metrics/ru_time_metrics_model/assets/dev.jsonl', val_set)


    typer.echo(typer.style(f"⭐ Done", fg=typer.colors.GREEN, bold=True))



if __name__ == "__main__":
    typer.run(load_json)


# Convert the datadump from django to jsonl
# original format
# {'model': 'prozhito_app.entry',
# 'pk': 694,
# 'fields': {'text': 'Читал Шаляпина — воспоминания. Оказывается, историк Ключевский был, по словам Шаляпина, хороший актер.  \nВызвал корреспондента ТАСС в связи со статьей о налогах с торгпредства. Пришел Лингарт с докладом о делах, потом Богомолова и Крачевский. В 101/2 пошел в баню. Подвергся массажу. Поехал в министерство к Крофте (у него третьего дня умерла мать). Говорили о налогах с торгпредства и о статье. По дороге из министерства, купил цветы для жены и для проводов Кошеков. Пообедали. Дети, Лена и Оля, были очень веселы. По приезде в полпредство мне доложили, что прибыла комиссия владельца дома, которой я назначил аудиенцию. Говорили около часа о перестройке дома. Потом явилась Майерова; об устройстве своей книги в ГИЗ. Скромная симпатичная женщина. Сидела недолго. Я пошел в детскую посмотреть, как укладываются дочери. Они шалят, смеются. Полежал у них, рассказал про свое детство. Уснули. Я пошел в своей кабинет. Читал газеты, написал несколько писем. Перед сном пишу эти страницы и завидую Майеровой, которая может заниматься только литературой.  \nПрощай еще один мой безлитературный день!',
#  'lemmatized': 'читать шаляпин — воспоминание. оказываться, историк ключевский быть, по слово шаляпин, хороший актер.  \nвызывать корреспондент тасс в связь со статья о налог с торгпредство. приходить лингарт с доклад о дело, потом богомолова и крачевский. в 101/2 пойти в баня. подвергаться массаж. поехать в министерство к крофт (у он третий день умирать мать). говорить о налог с торгпредство и о статья. по дорога из министерство, купить цветок для жена и для проводы кошек. пообедать. ребенок, лена и оля, быть очень веселый. по приезд в полпредство я докладывать, что прибывать комиссия владелец дома, который я назначать аудиенция. говорить около час о перестройка дом. потом являться майеров; об устройство свой книга в гиз. скромный симпатичный женщина. сидеть недолго. я пойти в детский посмотреть, как укладываться дочь. они шалить, смеяться. полежать у они, рассказывать про свой детство. уснуть. я пойти в свой кабинет. читать газета, написать несколько письмо. перед сон писать этот страница и завидовать майеровой, который мочь заниматься только литература.  \nпрощать еще один мой безлитературный день!\n',
#  'date_start': '1932-10-06',
#  'date_end': None,
#  'author': 4,
#  'diary': 3,
#  'sentiment': 'neutral',
#  'RuBERT': True,
#  'people': [],
#  'keywords': [],
#  'places': []}}

# TO 
# new format
#{"cats": {"OTHER": 1.0, "baking": 1.0, "bread": 0.0, "chicken": 0.0, "eggs": 0.0, "equipment": 0.0, "food-safety": 0.0, "meat": 0.0, "sauce": 0.0, "storage-method": 0.0, "substitutions": 0.0}, "meta": {"id": "1"}, "text": "How can I get chewy chocolate chip cookies?\n<p>My chocolate chips cookies are always too crisp. How can I get chewy cookies, like those of Starbucks?</p>\n<hr/>\n<p>Thank you to everyone who has answered. So far the tip that had the biggest impact was to chill and rest the dough, however I also increased the brown sugar ratio and increased a bit the butter. Also adding maple syrup helped. </p>\n"}

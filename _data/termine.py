import yaml, re, sys, math
from datetime import datetime, timedelta

termine = None
now = datetime.now()
# Latest date to add reoccuring events
max_date = datetime(2023, 12, 31, 23, 59)

# Training
difft = 3 - now.weekday()
next_training = (now + timedelta(days = 7 + difft if difft < 0 else difft))
weekdelta = timedelta(days = 7)

def training(i):
    zeit = next_training + i * weekdelta
    return { 'name': 'Training', 'zeit': zeit.replace(hour = 18, minute = 30) }

# Schützenzwerge
already = False
def zwerge(i):
    global already
    if i==0 and now.day > 7:
        already = True
    
    month = now.month + i + (1 if already else 0)
    zeit = datetime(now.year + math.floor((month - 1) / 12), (month - 1) % 12 + 1, 1, 10, 0)
    diffz = 5 - zeit.weekday()
    zeit = zeit + timedelta(days = (6 if diffz == -1 else diffz))
    
    if i==0 and zeit < now:
        already = True
        return zwerge(0)

    return { 'name': 'Schützenzwerge', 'zeit': zeit.replace(hour = 10, minute = 0), 'zeitbis': '11:30'}

def add_reoccuring(termine):
    for gen in [ training, zwerge ]:
        i = 0
        while True:
            next_termin = gen(i)
            if next_termin and next_termin['zeit'] <= max_date:
                next_termin['wiederholt'] = True
                if next_termin not in termine:
                    termine.append(next_termin)
                i = i + 1
            else:
                break

def parse_time(time):
    if re.match(r'\d{1,2}\.\d{1,2}\.\d+$', time):
        time = time + " 00:00"
    if re.match(r'\d{1,2}\.\d{1,2}\.\d+ \d{1,2}:\d{1,2}', time):
        return datetime.strptime(time, '%d.%m.%Y %H:%M')
    else:
        raise ValueError("Malformatted date: " + time) 

print('Loading YAML...')
with open('termine.yml', 'r+', encoding='utf-8') as file:
    termine = yaml.safe_load(file)
    if termine == None:
        sys.exit('No termine found')

    for termin in termine:
        termin['zeit'] = parse_time(termin['zeit'])
    
    print('Adding reoccuring...')
    add_reoccuring(termine)

    print('Normalizing datetimes...')
    for termin in termine:
        termin['zeit'] = termin['zeit'].strftime('%d.%m.%Y' if termin['zeit'].minute == 0 and termin['zeit'].hour == 0 else '%d.%m.%Y %H:%M')

    print('Sorting...')
    termine.sort(key = lambda termin: parse_time(termin['zeit']))
    
    print('Saving...')
    file.seek(0)
    file.truncate()
    yaml.dump(termine, file, allow_unicode=True)

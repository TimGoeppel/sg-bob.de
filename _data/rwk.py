import requests, yaml, json, os, sys

def fetch(path, query = {}):
    if not query:
        return {}
    for v in query.values():
        if not v:
            return {}

    try:
        req = requests.get('https://www.rwk-shooting.de/drucken/webservices/' + path + '.php', params = query)
        if req.status_code == 204 or not req.text: # Empty response
            return {}
        elif req.ok:
            return req.json()
    except Exception as e:
        print('Exception during execution of "fetch" (status code ' + str(req.status_code) + '): (' + str(path) + ', ' + str(query) + ')')
        print(e)
    return {}

def to_int(string):
    try:
        return int(string)
    except (ValueError, TypeError):
        return None

def to_float(string):
    try:
        return float(string)
    except (ValueError, TypeError):
        return None

def join_str(str1, str2):
    if str1:
        if str2:
            return str1 + ' ' + str2
        else:
            return str1
    elif str2:
        return str2
    return ''

def get_gaue():
    return fetch('get_gau')

def get_vereine(gau):
    vereine = fetch('get_verein', {
        'gau_nr': gau.get('gau_nr')
    }).get('vereine', [])
    if gau.get('gau_nr'):
        for verein in vereine:
            verein['gau_nr'] = gau.get('gau_nr')
    return vereine

def get_disziplinen(verein, only_current_year = True):
    disziplinen = []
    year = -1
    for disziplin in fetch('get_rundenwettkampf_einteilung', {
        'vereinsnummer': verein.get('vereinsnummer')
    }).get('rundenwettkampf', []):
        sportjahr = to_int(disziplin.get('sportjahr'))
        disziplin_new = {
            'id': disziplin.get('id'),
            'gau_nr': disziplin.get('gau_nr'),
            'sportjahr': sportjahr,
            'rwk_id': disziplin.get('rwk_id'),
            'eingeteilte_gruppen_id': disziplin.get('eingeteilte_gruppen_id'),
            'disziplin': disziplin.get('disziplin'),
            'disziplin_kurz': disziplin.get('disziplin_kurz'),
            'disziplin_id': disziplin.get('disziplin_id')
        }
        if only_current_year:
            if sportjahr > year:
                year = sportjahr
                disziplinen = [disziplin_new] # Reset and add this element
            elif sportjahr == year:
                disziplinen.append(disziplin_new)
        else:
            disziplinen.append(disziplin_new)
    return disziplinen

def get_mannschaften(verein, disziplin):
    mannschaften = []
    for mannschaft in fetch('get_mannschaftsinfo_year', {
        'vereinsnummer': verein.get('vereinsnummer'),
        'sportjahr': disziplin.get('sportjahr'),
        'disziplin_kurz': disziplin.get('disziplin_kurz')
    }).get('mannschaften', []):
        mannschaften.append({
            'vereinsnummer': verein.get('vereinsnummer'),
            'disziplin': disziplin.copy(),
            'platzierung': mannschaft.get('platzierung'),
            'klasse': mannschaft.get('klasse'),
            'klassen_name': mannschaft.get('klassen_name'),
            'klassen_id': mannschaft.get('klassen_id'),
            'gruppe': mannschaft.get('gruppe'),
            'gruppen_nr': to_int(mannschaft.get('gruppen_nr')),
            'gruppen_id': mannschaft.get('gruppen_id'),
            'mannschafts_nr': to_int(mannschaft.get('heim_verein_ma_nr'))
        })
    return mannschaften

def get_mannschaftsinfo(mannschaft, erzeuge_tabelle = True, erzeuge_durchgaenge = True):
    params = {
            'vereinsnummer': mannschaft.get('vereinsnummer'),
            'mannschaftsnummer': mannschaft.get('mannschafts_nr'),
            'gruppen_id': mannschaft.get('gruppen_id'),
            'klassen_id': mannschaft.get('klassen_id'),
            'disziplin_id': mannschaft.get('disziplin', {}).get('disziplin_id'),
            'rwk_id': mannschaft.get('disziplin', {}).get('rwk_id')
    }
    info = next(iter(fetch('get_mannschaftsinfo', params).get('mannschaftsinfo', [])), {})
    tabelle_new = []
    if erzeuge_tabelle:
        tabelle = info.get('tabelle', [])
        for i in range(len(tabelle)):
            m = tabelle[i]
            name = m.get('mannschaft')
            if ' ' in name:
                (name, _, _) = name.rpartition(' ')
            tabelle_new.append({
                'vereinsnummer': m.get('vereinsnummer'),
                'disziplin': mannschaft.get('disziplin', {}).copy(),
                'platzierung': i + 1,
                'klasse': mannschaft.get('klasse'),
                'klassen_name': mannschaft.get('klassen_name'),
                'klassen_id': mannschaft.get('klassen_id'),
                'gruppe': mannschaft.get('gruppe'),
                'gruppen_nr': mannschaft.get('gruppen_nr'),
                'gruppen_id': mannschaft.get('gruppen_id'),
                'mannschafts_nr': to_int(m.get('m_nr')),
                'name': name,
                'punkte_gewonnen': to_int(m.get('punkteGewonnen')),
                'punkte_verloren': m.get('punkteVerloren'),
                'ringe': to_int(m.get('ringe')),
                'anzahl_geschossen': to_int(m.get('anzahlGeschossen'))
            })
    durchgaenge_new = []
    if erzeuge_durchgaenge:
        durchgaenge = info.get('durchgang', [])
        termine = fetch('get_termine', params).get('termine', [])
        i = 0
        for termin in termine:
            durchgang_new = {
                    'heim_id': termin['heim'],
                    'runde': termin['v_r'],
                    'wettkampftag': to_int(termin.get('wettkampftag')),
                    'zeit': join_str(termin.get('datum'), termin.get('zeit')),
                    'ort': termin.get('name_heim_verein'),
                    'heim_name': termin.get('name_heim_verein'),
                    'gast_name': termin.get('name_gast_verein'),
                    'heim_mannschafts_nr': to_int(termin.get('heim_verein_ma_nr')),
                    'gast_mannschafts_nr': to_int(termin.get('gast_verein_ma_nr')),
            }
            durchgang_new['name'] = ' '.join([durchgang_new['heim_name'], str(durchgang_new['heim_mannschafts_nr']), '–', durchgang_new['gast_name'], str(durchgang_new['gast_mannschafts_nr']), '(' + str(durchgang_new['wettkampftag']) + '.', durchgang_new['runde'] + ')'])
            if i < len(durchgaenge):
                durchgang = durchgaenge[i]
                if durchgang.get('wettkampftag') == (termin.get('wettkampftag') + ' ' + termin.get('v_r')) and (termin.get('name_heim_verein') + ' ' + termin.get('heim_verein_ma_nr')) == durchgang.get('heim_name') and (termin.get('name_gast_verein') + ' ' + termin.get('gast_verein_ma_nr')) == durchgang.get('gast_name'):
                    durchgang_new['heim_ringe'] = to_int(durchgang.get('heim_punkte'))
                    durchgang_new['gast_ringe'] = to_int(durchgang.get('gast_punkte'))
                    win_lose = durchgang.get('win_lose')
                    if win_lose:
                        durchgang_new['sieg'] = 1 if win_lose == 'win' else (0 if win_lose == 'undecided' else -1)
                    if 'platzierung' in durchgang:
                        durchgang_new['platzierung'] = durchgang.get('platzierung')
                    durchgang_new['punkte'] = durchgang.get('punkte')
                    durchgang_new['punkte_akkumulativ'] = durchgang.get('act_win')
                    durchgang_new['avg'] = to_float(durchgang.get('avg'))
                    i += 1
                        
            durchgaenge_new.append(durchgang_new)
    mannschafts_info = {
        'platzierung': info.get('platzierung'),
        'avg': to_float(info.get('avg')),
        'max': to_float(info.get('max')),
        'min': to_float(info.get('min')),
        'tabelle': tabelle_new,
        'durchgaenge': durchgaenge_new
    }
    return mannschafts_info

def get_chartjs(vereins_name, mannschaft, mannschafts_info):
    try:
        if vereins_name == None or mannschaft == None or 'klasse' not in mannschaft or 'mannschafts_nr' not in mannschaft or mannschafts_info == None or 'avg' not in mannschafts_info or 'durchgaenge' not in mannschafts_info or mannschafts_info['durchgaenge'] == None:
            return None
        maximum = 400
        if mannschaft['klasse'] in ['Jug', 'Jugendklasse']:
            maximum *= 3
        else:
            maximum *= 4
        avg = mannschafts_info['avg']
        s_min = max(2 * avg - maximum, 0)
        labels = []
        data_verein = []
        data_gegner = []
        for durchgang in mannschafts_info['durchgaenge']:
            if 'wettkampftag' in durchgang and 'heim_name' in durchgang and 'heim_ringe' in durchgang and 'gast_ringe' in durchgang:
                labels.append(str(durchgang['wettkampftag']) + '. ' + durchgang['runde'])
                heim = durchgang['heim_name'] == vereins_name
                data_verein.append(durchgang['heim_ringe' if heim else 'gast_ringe'])
                data_gegner.append(durchgang['gast_ringe' if heim else 'heim_ringe'])

        data = {
            'labels': labels,
            'datasets': [
                {
                    'label': vereins_name + ' ' + str(mannschaft['mannschafts_nr']),
                    'data': data_verein,
                    'pointRadius': 6
                },
                {
                    'label': 'Gegner',
                    'data': data_gegner,
                    'pointRadius': 6
                }
            ]
        }
        return {
            'data': data,
            'suggested_min': s_min,
            'max': maximum
        }
    except Exception as e:
        return None

def get_schuetzen(verein, disziplin, erzeuge_durchgaenge = False):
    schuetzen = fetch('get_shooter', {
        'vereinsnummer': verein.get('vereinsnummer'),
        'rwk_id': disziplin.get('rwk_id')
    }).get('shooters', [])
    for schuetze in schuetzen:
        detail = next(iter(fetch('get_detail_shooter', {
            'vereinsnummer': verein.get('vereinsnummer'),
            'shooter_id': schuetze.get('id'),
            'rwk_id': disziplin.get('rwk_id')
        }).get('shooter', [])), {})
        # Details hinzufügen
        if detail:
            if 'mannschafts_nr' in detail:
                mannschafts_nr = detail.get('mannschafts_nr')
                if mannschafts_nr and '.' in mannschafts_nr:
                    (nr, _, _) = detail.get('mannschafts_nr').partition('.')
                    schuetze['mannschafts_nr'] = to_int(nr)
            schuetze['gruppe'] = detail.get('gruppen_name')
            schuetze['max'] = to_int(detail.get('max'))
            schuetze['min'] = to_int(detail.get('min'))
            schuetze['avg'] = to_float(detail.get('avg'))
            schuetze['avg_stamm'] = to_float(detail.get('avgStamm'))
            schuetze['avg_ersatz'] = to_float(detail.get('avgErsatz'))
            schuetze['anzahl_stamm'] = to_int(detail.get('anzahlStamm'))
            schuetze['anzahl_ersatz'] = to_int(detail.get('anzahlErsatz'))
            if erzeuge_durchgaenge:
                schuetze['durchgaenge'] = detail.get('durchgang')
    return schuetzen

def get_schuetzen_mannschaft(schuetzen, mannschaft):
    return [schuetze for schuetze in schuetzen if (isinstance(schuetze, dict) and schuetze.get('mannschafts_nr') == mannschaft.get('mannschafts_nr') and schuetze.get('gruppe') == mannschaft.get('gruppe'))]

# If 'years' is empty, use the current year, and if 'years' is equal to 'None', show all years.
def get_overview(gau_nr, vereinsnummer, vereins_name, years, include_ersatz = False):
    data = {
            'gau_nr': gau_nr,
            'vereinsnummer': vereinsnummer
    }
    if years == None:
        data['disziplinen'] = get_disziplinen(data, only_current_year = False)
    else:
        if len(years) == 0:
            data['disziplinen'] = get_disziplinen(data, only_current_year = True)
        else:
            data['disziplinen'] = [disziplin for disziplin in get_disziplinen(data, only_current_year = False) if disziplin.get('sportjahr', None) in years]
    if data['disziplinen']:
        parent_dir = os.path.dirname(os.path.dirname(__file__))
        for index_d in range(0, len(data['disziplinen'])):
            disziplin = data['disziplinen'][index_d]
            schuetzen = get_schuetzen(data, disziplin)
            disziplin['mannschaften'] = get_mannschaften(data, disziplin)
            for index_m in range(0, len(disziplin['mannschaften'])):
                mannschaft = disziplin['mannschaften'][index_m]
                mannschaft['info'] = get_mannschaftsinfo(mannschaft, erzeuge_tabelle = True, erzeuge_durchgaenge = True)
                prefix = '_'.join([disziplin['disziplin_kurz'], str(disziplin['sportjahr']), str(mannschaft['mannschafts_nr']), mannschaft['klassen_name']]).replace(' ', '_').lower()
                calendar_path = prefix
                mannschaft['info']['kalender'] = calendar_path
                for durchgang in mannschaft['info'].get('durchgaenge', []):
                    durchgang['uuid'] = prefix + '_' + (str(durchgang['wettkampftag']) + '_' + durchgang['runde']).replace(' ', '_').lower()
                try:
                    print(os.path.dirname(__file__))
                    print(parent_dir)
                    ical_file = open(parent_dir + '/assets/calendar/' + calendar_path + '.ics', 'w')
                    ical_file.write('---\nlayout: null\n---\n{% assign termine = site.data.rwk_data.disziplinen[' + str(index_d) + '].mannschaften[' + str(index_m) + '].info.durchgaenge %}{% include calendar.ics termine=termine name="SG Burgoberbach ' + str(mannschaft['mannschafts_nr']) + ' (' + mannschaft['klassen_name'] + ')" description="Wettkampftermine der ' + str(mannschaft['mannschafts_nr']) + '. Mannschaft des SG Burgoberbach" %}')
                    ical_file.close()
                except Exception as e:
                    print('Could not write "' + prefix + '.ics" to file')
                    print(e)
                mannschaft['schuetzen'] = get_schuetzen_mannschaft(schuetzen, mannschaft)
                del mannschaft['disziplin']
                chartjs = get_chartjs(vereins_name, mannschaft, mannschaft['info'])
                if chartjs != None:
                    mannschaft['chartjs'] = chartjs
                for tabellen_mannschaft in mannschaft['info'].get('tabelle', []):
                    del tabellen_mannschaft['disziplin']
            if include_ersatz:
                ersatz_mannschaft = {
                    'vereinsnummer': vereinsnummer,
                    'gruppe': 'Ersatz',
                    'disziplin': disziplin
                }
                ersatz_mannschaft['schuetzen'] = get_schuetzen_mannschaft(schuetzen, ersatz_mannschaft)
                del ersatz_mannschaft['disziplin']
                if len(ersatz_mannschaft.get('schuetzen', [])) != 0:
                    disziplin['mannschaften'].append(ersatz_mannschaft)
                
        return data
    return None

args = sys.argv[1:]
if 'all' in args:
    args = None
elif len(args) != 0:
    args = [to_int(arg) for arg in args if to_int(arg)]
path = os.path.dirname(__file__)
file = open(path + '/' + 'rwk_data.yml', 'w')
file2 = open(path + '/' + 'rwk_data.json', 'w')
data = get_overview('102000', '102013', 'SG Burgoberbach', args, include_ersatz = True)
if data:
    yaml.dump(data, file, allow_unicode=True)
    file.close()
    json.dump(data, file2, ensure_ascii=False)
    file2.close()

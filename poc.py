from datetime import date

import requests

today = date.today().strftime("%Y-%m-%d")

tegel_moderna = {}
tegel_moderna['api'] = f"https://www.doctolib.de/availabilities.json?start_date={today}&visit_motive_ids=2537716&agenda_ids=465584-465619-465575-465527-465534-466146-465526-465592-465598-465601-465651-465543-465615-465653-466144-466139-466141-466153-466157-465550-465553-465594-465701-465630-465532-465609-466127-466128-466129-466130-466131-466132-466133-466134-466135-466136-466137-466138-466140-466143-466145-466147-466148-466149-466150-466151-466152-466154-466155-466156-466158-466159-466160-466161-465678-465555-465558-465580-465582&insurance_sector=public&practice_ids=158436&destroy_temporary=true&limit=4"
tegel_moderna['practice'] = 158436

response = requests.get(tegel_moderna['api']).json()

if response['total'] > 0:
    print(response)
    print(appointment_link.format(practice=tegel_moderna['practice']))
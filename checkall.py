import requests

from datetime import date
import webbrowser

from agendas import group_agendas
from constants import *


appointment_link = "https://www.doctolib.de/institut/berlin/ciz-berlin-berlin?pid=practice-{practice}"
availability_url = "https://www.doctolib.de/availabilities.json?start_date={today}&visit_motive_ids={motive}&agenda_ids={agenda}&insurance_sector=public&practice_ids={practice}&destroy_temporary=true&limit=4"
agendas_url = "https://www.doctolib.de/booking/ciz-berlin-berlin.json"

def generate_availability_url(practice_id, motive_id, agendas_string):
    today = date.today().strftime("%Y-%m-%d")
    url = availability_url.format(
        today=today,
        motive=motive_id,
        agenda=agendas_string,
        practice=practice_id
    )
    return url

def check():
    agendas_json = requests.get(agendas_url).json()
    agendas_by_practice = group_agendas(agendas_json['data']['agendas'])

    for practice_id, agendas_by_motives in agendas_by_practice.items():

        for motive_id, agendas in agendas_by_motives.items():
            agendas_string = "-".join(agendas)

            availability_url = generate_availability_url(practice_id, motive_id, agendas_string)
            #print(availability_url)
            availability = requests.get(availability_url).json()

            if availability['total']:
                print(availability['total'])
                url = appointment_link.format(practice_id)

                webbrowser.open_new(url)

if __name__ == "__main__":
    check()
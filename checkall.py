import requests

import webbrowser
import json
import os
from datetime import date
from collections import defaultdict


appointment_link = "https://www.doctolib.de/institut/berlin/ciz-berlin-berlin?pid=practice-{practice}"
availability_url = "https://www.doctolib.de/availabilities.json?start_date={today}&visit_motive_ids={motive}&agenda_ids={agenda}&insurance_sector=public&practice_ids={practice}&destroy_temporary=true&limit=4"
agendas_url = "https://www.doctolib.de/booking/ciz-berlin-berlin.json"

slack_webhook_url = os.environ['SLACK_WEBHOOK']

request_headers = {
    'User-Agent': 'Impferator',
}

def slack_notification(amount, url):
    msg = "{amount} vaccination appointments are available here: {url}"

    msg_formatted = {'text': msg.format(amount=amount, url=url)}
    response = requests.post(
        slack_webhook_url, data=json.dumps(msg_formatted),
        headers={'Content-Type': 'application/json'}
    )
    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
    )

def generate_availability_url(practice_id, motive_id, agendas_string):
    today = date.today().strftime("%Y-%m-%d")
    url = availability_url.format(
        today=today,
        motive=motive_id,
        agenda=agendas_string,
        practice=practice_id
    )
    return url

def group_agendas(agendas):
    agenda_ids = defaultdict(lambda: defaultdict(list))

    for agenda in agendas:
        if agenda['booking_disabled'] or agenda['booking_temporary_disabled']:
            continue

        if not agenda['visit_motive_ids']:
            continue

        practice_id = agenda['practice_id']
        motive_id = agenda['visit_motive_ids'][0]

        agenda_ids[practice_id][motive_id].append(str(agenda['id']))

    return agenda_ids


def check():
    agendas_json = requests.get(agendas_url).json()
    agendas_by_practice = group_agendas(agendas_json['data']['agendas'])

    for practice_id, agendas_by_motives in agendas_by_practice.items():

        for motive_id, agendas in agendas_by_motives.items():
            agendas_string = "-".join(agendas)

            availability_url = generate_availability_url(practice_id, motive_id, agendas_string)
            #print(availability_url)
            availability = requests.get(availability_url, headers=request_headers).json()

            if availability['total'] and availability['total'] < 100:
                #print(availability['total'])
                url = appointment_link.format(practice=practice_id)

                slack_notification(availability['total'], url)
                #webbrowser.open_new(url)

if __name__ == "__main__":
    check()

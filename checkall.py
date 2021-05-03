import requests

today = date.today().strftime("%Y-%m-%d")

appointment_link = "https://www.doctolib.de/institut/berlin/ciz-berlin-berlin?pid=practice-{practice}"
availability_url = "https://www.doctolib.de/availabilities.json?start_date={today}&visit_motive_ids={motive}&agenda_ids={agenda}&insurance_sector=public&practice_ids={practice}&destroy_temporary=true&limit=4"


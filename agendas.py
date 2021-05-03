import requests
from collections import defaultdict


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

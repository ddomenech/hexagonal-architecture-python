from datetime import datetime

import json


def datetime_to_rfc822_string(dt: datetime) -> str:
    if isinstance(dt, datetime):
        return datetime.strftime(dt,"%Y-%m-%dT%H:%M:%S.%f%z")
    return json.dumps(dt)

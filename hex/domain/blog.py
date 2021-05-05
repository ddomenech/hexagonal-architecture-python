from dataclasses import dataclass
from datetime import datetime

from dataclasses_json import dataclass_json, LetterCase

from hex.domain.post import Post


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class Blog:
    id: int
    author_name: str
    title: str
    body: str
    created_at: datetime
    updated_at: datetime
    post_id: int

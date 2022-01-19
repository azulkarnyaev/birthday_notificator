from dataclasses import dataclass
from typing import Callable, List

from birthday_notificator.personal_info import Relation, Language, Contact

DbItems = list[dict[str, any]]


@dataclass
class BirthdayData:
    day_of_month: int
    month: int
    relation: Relation
    target_chat_id: str
    language: Language
    name: str
    contact_details: Contact


def read_birthdays(db_reader: Callable[[], DbItems]) -> List[BirthdayData]:
    db_items = db_reader()
    return [_parse_birthday_item(item) for item in db_items]


def _parse_birthday_item(item):
    birth_date = _parse_birth_date(item['birthday'])
    if len(birth_date) != 2:
        raise Exception("Wrong birthday key")
    return BirthdayData(
        day_of_month=birth_date[0],
        month=birth_date[1],
        relation=Relation[item['relation']],
        target_chat_id=item['chat_id'],
        language=Language[item['lang']],
        name=item['name'],
        contact_details=_parse_contact_details(item)
    )


def _parse_birth_date(compound_birthday: str) -> list[int]:
    date_components = compound_birthday.split('#')
    return [int(c) for c in date_components]


def _parse_contact_details(item):
    return Contact(telegram_id=item['contact'].get('telegram_id', None),
                   whatsapp=item['contact'].get('whatsapp', None))

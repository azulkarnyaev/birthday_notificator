import pytest

from birthday_notificator.birthday_reader import BirthdayData, read_birthdays, DbItems
from birthday_notificator.personal_info import Language, Contact, Relation


def test_read_birthdays():
    expected_birthday_data = BirthdayData(
        day_of_month=1,
        month=7,
        relation=Relation.FAMILY,
        target_chat_id='12345678',
        language=Language.RU,
        name='Name',
        contact_details=Contact(
            whatsapp=None,
            telegram_id='tg_id'
        )
    )

    def db_reader() -> DbItems:
        return [{'relation': 'FAMILY', 'congrats_id': '12aebb12-1aaa-450d-9a55-c0ae66a7c108', 'name': 'Name',
                 'contact': {'telegram_id': 'tg_id'}, 'chat_id': '12345678', 'birthday': '01#07', 'lang': 'RU'}]
    assert read_birthdays(db_reader) == [expected_birthday_data]


def test_parse_birthday_day():
    def db_reader() -> DbItems:
        return [{'relation': 'FAMILY', 'congrats_id': '12aebb12-1aaa-450d-9a55-c0ae66a7c108', 'name': 'Name',
                 'contact': {'telegram_id': 'tg_id'}, 'chat_id': '12345678', 'birthday': '02#07', 'lang': 'RU'}]

    assert read_birthdays(db_reader)[0].day_of_month == 2


def test_parse_birthday_month():
    def db_reader() -> DbItems:
        return [{'relation': 'FAMILY', 'congrats_id': '12aebb12-1aaa-450d-9a55-c0ae66a7c108', 'name': 'Name',
                 'contact': {'telegram_id': 'tg_id'}, 'chat_id': '12345678', 'birthday': '02#08', 'lang': 'RU'}]

    assert read_birthdays(db_reader)[0].month == 8


def test_should_fail_if_date_has_3_components():
    def db_reader() -> DbItems:
        return [{'relation': 'FAMILY', 'congrats_id': '12aebb12-1aaa-450d-9a55-c0ae66a7c108', 'name': 'Name',
                 'contact': {'telegram_id': 'tg_id'}, 'chat_id': '12345678', 'birthday': '01#07#1993', 'lang': 'RU'}]

    with pytest.raises(Exception):
        read_birthdays(db_reader)

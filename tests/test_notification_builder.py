from typing import List

from birthday_notificator.birthday_reader import BirthdayData
from birthday_notificator.notification_builder import build_congratulation
from birthday_notificator.personal_info import Relation, Language, Contact


def test_build_telegram_congratulation():
    birthday_data = create_birthday_data(
        Contact(
            whatsapp=None,
            telegram_id='azat_zul'
        )
    )

    def congratulations_reader(relation, language) -> List[str]:
        return ["С днем рождения!"]

    def selector(conrats):
        return conrats[0]

    assert build_congratulation(birthday_data,
                                selector,
                                congratulations_reader) == """Today is Name's birthday\\!
[Congratulate in Telegram](tg://msg?text=%D0%A1%20%D0%B4%D0%BD%D0%B5%D0%BC%20%D1%80%D0%BE%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F%21&to=azat_zul)"""


def test_build_whatsapp_link():
    birthday_data = create_birthday_data(
        Contact(
            whatsapp='12345678',
            telegram_id=None
        )
    )

    def congratulations_reader(relation, language) -> List[str]:
        return ["С днем рождения!"]

    def selector(conrats):
        return conrats[0]

    assert build_congratulation(birthday_data,
                                selector,
                                congratulations_reader) == """Today is Name's birthday\\!
[Congratulate in Whatsapp](https://wa.me/12345678?text=%D0%A1%20%D0%B4%D0%BD%D0%B5%D0%BC%20%D1%80%D0%BE%D0%B6%D0%B4%D0%B5%D0%BD%D0%B8%D1%8F%21)"""


def test_build_telegram_and_whatsapp_links():
    birthday_data = create_birthday_data(
        Contact(
            whatsapp='12345678',
            telegram_id='tg_id'
        )
    )

    def selector(conrats):
        return conrats[0]

    def congratulations_reader(relation, language) -> List[str]:
        return ["Happy birthday!"]

    assert build_congratulation(birthday_data,
                                selector,
                                congratulations_reader) == """Today is Name's birthday\\!
[Congratulate in Telegram](tg://msg?text=Happy%20birthday%21&to=tg_id)
[Congratulate in Whatsapp](https://wa.me/12345678?text=Happy%20birthday%21)"""


def test_build_empty_notification():
    birthday_data = create_birthday_data(
        Contact(
            whatsapp=None,
            telegram_id=None
        )
    )

    def congratulations_reader(relation, language) -> List[str]:
        return ["Happy birthday!"]

    def selector(conrats):
        return conrats[0]

    assert build_congratulation(birthday_data,
                                selector,
                                congratulations_reader) == """Today is Name's birthday\\!
_No contact details found_"""


def test_empty_notifications():
    birthday_data = create_birthday_data(
        Contact(
            whatsapp="1234567",
            telegram_id="id"
        )
    )

    def selector(conrats):
        return None

    def congratulations_reader(relation, language) -> List[str]:
        return []

    assert build_congratulation(birthday_data,
                                selector,
                                congratulations_reader) == """Today is Name's birthday\\!
There is no congratulation text for relation FAMILY and language RU"""


def create_birthday_data(contact_details: Contact) -> BirthdayData:
    return BirthdayData(
        day_of_month=1,
        month=7,
        relation=Relation.FAMILY,
        target_chat_id='12345123',
        language=Language.RU,
        name='Name',
        contact_details=contact_details
    )

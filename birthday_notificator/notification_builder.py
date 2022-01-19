from typing import Callable, List, Optional, Sequence
from urllib.parse import quote

from birthday_notificator.birthday_reader import BirthdayData
from birthday_notificator.personal_info import Relation, Language

DbReader = Callable[[Relation, Language], List[str]]
RandomSelector = Callable[[Sequence[str]], Optional[str]]


def build_congratulation(birthday_data: BirthdayData,
                         random_selector: RandomSelector,
                         congratulation_db_reader: DbReader) -> str:
    congratulations = congratulation_db_reader(birthday_data.relation, birthday_data.language)
    notification = random_selector(congratulations)

    congratulation_prefix = f"Today is {birthday_data.name}'s birthday\\!"

    if notification is None:
        return f"{congratulation_prefix}\nThere is no congratulation text for relation {birthday_data.relation.name} " \
               f"and language {birthday_data.language.name}"
    normalised_text = quote(notification)
    contact_details = birthday_data.contact_details
    text = []
    if contact_details.telegram_id:
        text.append(_build_telegram_link(normalised_text, contact_details.telegram_id))
    if contact_details.whatsapp:
        text.append(_build_whatsapp_link(normalised_text, contact_details.whatsapp))
    links = '\n'.join(text)
    if links == '':
        links = "_No contact details found_"
    return f"{congratulation_prefix}\n{links}"


def _pick_random_notification(congratulations: List[str]) -> Optional[str]:
    if len(congratulations) == 0:
        return None
    return congratulations[0]


def _build_telegram_link(message: str, telegram_id: str) -> str:
    return f"[Congratulate in Telegram](tg://msg?text={message}&to={telegram_id})"


def _build_whatsapp_link(message: str, phone: str) -> str:
    return f"[Congratulate in Whatsapp](https://wa.me/{phone}?text={message})"

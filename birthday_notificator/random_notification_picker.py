import random
from typing import List, Optional, Sequence


def pick_random_notification(notifications: Sequence[str]) -> Optional[str]:
    if len(notifications) == 0:
        return None
    return random.choice(notifications)

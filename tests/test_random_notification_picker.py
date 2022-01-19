from birthday_notificator.random_notification_picker import pick_random_notification


def test_empty_response_if_no_notification():
    assert pick_random_notification([]) is None


def test_return_random_element():
    first_choice = pick_random_notification(["first", "second", "third"])
    max_retries = 100
    i = 0
    while i < max_retries and first_choice != pick_random_notification(["first", "second", "third"]):
        i = i + 1
    assert i < max_retries


def test_should_not_return_none():
    assert pick_random_notification(["first", "second", "third"]) is not None


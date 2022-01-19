import pytest

from birthday_notificator.date_extractor import extract_date_key


def test_extract_date_key():
    event_sample = {'version': '0',
                    'id': 'a1062439-34fa-e157-d774-5d7966136b14',
                    'detail-type': 'Scheduled Event',
                    'source': 'aws.events',
                    'account': '1234567891011',
                    'time': '2021-12-29T09:00:00Z',
                    'region': 'eu-west-2',
                    'resources': ['arn:aws:events:eu-west-2:1234567891011:rule/rule_name'],
                    'detail': {}
                    }
    assert extract_date_key(event_sample) == "29#12"


def test_trim_zero_leading_values():
    event_sample = {'account': '1234567891011',
                    'time': '2021-09-01T09:00:00Z',
                    'region': 'eu-west-2'
                    }
    assert extract_date_key(event_sample) == "1#9"


def test_trim_zero_leading_values_day():
    event_sample = {'account': '1234567891011',
                    'time': '2021-12-02T09:00:00Z',
                    'region': 'eu-west-2'
                    }
    assert extract_date_key(event_sample) == "2#12"


def test_should_raise_error_if_event_does_not_have_time_parameter():
    event_sample = {'key1': 1, 'key2': 2}
    with pytest.raises(Exception):
        extract_date_key(event_sample)

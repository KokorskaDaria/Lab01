from copy import deepcopy

import pytest

from core import MeterReading, calculate_consumption, make_processor


def sample_readings() -> list[MeterReading]:
    return [
        {'id': 1, 'name': 'Test', 'previous': 100, 'current': 150, 'tariff_group': 'standard', 'has_benefit': True}
    ]


def tariff(consumption: int, group: str) -> float:
    return consumption * {'standard': 4.0, 'night': 2.0}[group]


def benefit(amount: float, enabled: bool) -> float:
    return amount * (0.75 if enabled else 1.0)


def test_referential_transparency() -> None:
    readings = sample_readings()
    processor = make_processor(tariff, benefit)
    assert processor(readings) == processor(readings)


def test_no_mutation() -> None:
    readings = sample_readings()
    original = deepcopy(readings)
    make_processor(tariff, benefit)(readings)
    assert readings == original


def test_callable_policies() -> None:
    result = make_processor(tariff, benefit)(sample_readings())
    assert result['count'] == 1
    assert result['bills'][0]['consumption'] == 50
    assert result['bills'][0]['base_amount'] == 200.0
    assert result['bills'][0]['amount_due'] == 150.0
    assert result['total_due'] == 150.0


def test_custom_callable_policies() -> None:
    result = make_processor(lambda consumption, group: consumption * 10, lambda amount, enabled: amount - 20)(sample_readings())
    assert result['total_due'] == 480.0


def test_invalid_readings() -> None:
    reading = sample_readings()[0]
    reading['current'] = 90
    with pytest.raises(ValueError):
        calculate_consumption(reading)

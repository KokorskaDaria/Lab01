from typing import Callable, TypedDict
class MeterReading(TypedDict):
    id: int
    name: str
    previous: int
    current: int
    tariff_group: str
    has_benefit: bool
class Bill(MeterReading):
    consumption: int
    base_amount: float
    amount_due: float
class Result(TypedDict):
    count: int
    total_due: float
    bills: list[Bill]
TariffFn = Callable[[int, str], float]
BenefitFn = Callable[[float, bool], float]
def calculate_consumption(reading: MeterReading) -> int:
    if reading['previous'] < 0 or reading['current'] < reading['previous']:
        raise ValueError('Invalid meter readings')
    return reading['current'] - reading['previous']
def calculate_base_amount(consumption: int, group: str, tariff: TariffFn) -> float:
    return round(tariff(consumption, group), 2)
def calculate_amount_due(base_amount: float, has_benefit: bool, benefit: BenefitFn) -> float:
    return round(benefit(base_amount, has_benefit), 2)
def create_bill(reading: MeterReading, tariff: TariffFn, benefit: BenefitFn) -> Bill:
    consumption = calculate_consumption(reading)
    base_amount = calculate_base_amount(consumption, reading['tariff_group'], tariff)
    amount_due = calculate_amount_due(base_amount, reading['has_benefit'], benefit)
    return {**reading, 'consumption': consumption, 'base_amount': base_amount, 'amount_due': amount_due}
def make_processor(tariff: TariffFn, benefit: BenefitFn) -> Callable[[list[MeterReading]], Result]:
    def process(readings: list[MeterReading]) -> Result:
        bills = [create_bill(reading, tariff, benefit) for reading in readings]
        return {'count': len(bills), 'total_due': round(sum(bill['amount_due'] for bill in bills), 2), 'bills': bills}
    return process

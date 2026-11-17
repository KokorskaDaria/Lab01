from core import MeterReading, Result, make_processor


def tariff(consumption: int, group: str) -> float:
    rates = {'standard': 4.0, 'night': 2.0}  # Умовні тарифи, грн/кВт·год
    if group not in rates:
        raise ValueError(f'Unknown tariff group: {group}')
    return consumption * rates[group]


def benefit(amount: float, has_benefit: bool) -> float:
    return amount * (0.75 if has_benefit else 1.0)  # Умовна пільга 25%


def render_report(result: Result) -> None:
    for bill in result['bills']:
        print(f"Квитанція №{bill['id']} — {bill['name']}")
        print(f"Показники: {bill['previous']} → {bill['current']}")
        print(f"Споживання: {bill['consumption']} кВт·год")
        print(f"Тарифна група: {bill['tariff_group']}")
        print(f"До пільги: {bill['base_amount']:.2f} грн")
        print(f"До оплати: {bill['amount_due']:.2f} грн\n")
    print(f"Кількість квитанцій: {result['count']}")
    print(f"Загальна сума: {result['total_due']:.2f} грн")


def main() -> None:
    readings: list[MeterReading] = [
        {'id': 1, 'name': 'Олена', 'previous': 1200, 'current': 1350, 'tariff_group': 'standard', 'has_benefit': False},
        {'id': 2, 'name': 'Іван', 'previous': 500, 'current': 620, 'tariff_group': 'night', 'has_benefit': True},
        {'id': 3, 'name': 'Марія', 'previous': 2200, 'current': 2280, 'tariff_group': 'standard', 'has_benefit': True},
    ]
    processor = make_processor(tariff, benefit)
    render_report(processor(readings))


if __name__ == '__main__':
    main()

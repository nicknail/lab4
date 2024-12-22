import json
import os
import random

from logging import basicConfig, info, INFO
from typing import Type

from lab4.gists.account import *
from lab4.gists.card import *
from lab4.gists.person import *


def process_child(person: dict) -> Type[Child]:
    cards = [KidsCard(c["number"], c["balance"], c["limit"]) for c in person["cards"]]
    return Child(
        person["first_name"],
        person["last_name"],
        cards,
        person["age"],
    )


def process_adult(person: dict) -> Type[Adult]:
    cards = [Card(c["number"], c["balance"]) for c in person["cards"]]
    children = [process_child(c) for c in person["children"]]
    return Adult(person["first_name"], person["last_name"], cards, children)


def process_data(filepath: str) -> Type[Adult]:
    with open(filepath) as file:
        people = json.load(file)

    for person in people:
        yield process_adult(person)


def get_suitable_targets(people: list) -> Type[Adult]:
    for person in people:
        if not person.get_children():
            continue
        if not person.get_cards():
            continue
        if not all(c.get_cards() for c in person.get_children()):
            continue
        yield person


def demo(people: list):
    sep = "\n---\n"

    info("# Демонстрация")
    info("### Строковое представление")

    info(
        "> Возьмем произвольного субъекта с детьми и картами"
        " и применим к нему метод строкового представления\n"
    )

    target = random.choice(list(get_suitable_targets(people)))
    info(target)

    info(sep)
    info("> Узнаем информацию о картах субъекта")

    for card in (cards := target.get_cards()):
        info(card)

    for child in (children := target.get_children()):
        info(sep)
        info("> Применим методы к следующему ребенку: %s\n", child.get_name())

        info(child)
        for card in (cards := child.get_cards()):
            info(card)

    info("### Покупка товаров")
    info(
        "> Возьмем за субъекта первого (по списку) ребенка "
        "и попробуем купить акции Сбера"
    )
    info("> Будем использовать первую (по списку) карту этого ребенка\n")

    c_target = target.get_children()[0]
    c_card = c_target.get_cards()[0]

    info(c_target)

    flashback = str(c_card)
    info(c_card)

    share = round((min(c_card.get_balance(), c_card.get_limit()) + 1) / 3, 2)
    status, message = c_card.checkout(c_target, "Акция Сбера", share, 1)
    assert status  # https://xkcd.com/2200/

    info(message + "\n")

    info(sep)
    info("> Проверим баланс и попробуем купить еще две акции")
    info("> Это сделать уже не получится\n")

    info(c_card)

    status, message = c_card.checkout(c_target, "Акция Сбера", share, 2)
    assert not status

    info(message + "\n")

    info(sep)
    info("> Обратим внимание на то, что баланс и лимит карты снизились\n")

    info("- До: " + flashback)
    info("- После: " + str(c_card))

    info("### Передача денежных средств")

    card = target.get_cards()[0]
    share = round(card.get_balance() / 2, 2)

    info(
        "> Будем использовать первую карту родителя" " и первую карту первого ребенка."
    )
    info("> Карты соответственно:\n")

    info(card)
    info(c_card)

    info("> Снимем со счета родителя %g₽ ...\n", share)
    status, message = card.withdraw(target, share, False)
    assert status

    info(message + "\n")

    # Костыль для того, чтобы вывести строку родителя без детей
    children_chamber = target.get_children()
    target.children = list()

    info(target)
    info(card)

    target.children = children_chamber

    info("> ... и передадим их ребенку\n")
    status, message = target.give_cash(c_target, share)
    assert status

    info(message + "\n")
    info(c_target)

    info("> Теперь ребенок может положить средства на свою карту\n")

    if c_target.get_age() < 6:
        _, message = c_card.add_funds(c_target, 123456.789)
        info(message + "\n")

        info("> ... Ну, когда он научится считать, операция будет выглядеть так:\n")

    status, message = c_card.add_funds(c_target, share)
    assert status

    info(message + "\n")

    info(c_target)
    info(c_card)

    info("### Заработная плата")

    info("> Установим взрослому заработную плату в 80.000₽ и выплатим ее:\n")

    target.set_wage(80_000.0)
    status, message = target.paycheck()
    assert status

    info(message)
    info(target)

    info("> После каждой выплаты заработная плата уменьшается\n")

    info("### Перевод денежных средств")
    info("> Аналогично ранней демонстрации передадим деньги от лица родителя ребенку,")
    info("> используя на сей раз банковские карты:\n")

    status, message = card.transfer(c_card, card.get_balance())
    assert status

    info(message)
    info(card)
    info(c_card)

    info("> Попробуем сделать это в обратную сторону:\n")
    status, message = c_card.transfer(card, c_card.get_balance())
    assert not status

    info(message)

    info("### Обязательные платежи")

    info(
        "> От лица родителя создадим обязательный платеж 'Коммунальные услуги' на 100₽ и совершим его,"
    )
    info("> предварительно начислив 1000₽:\n")

    card.set_balance(1000.0)
    card.add_payment("Коммунальные услуги", 100.0)
    status, message = card.make_payment("Коммунальные услуги")
    assert status

    info(message)
    info(card)

    info("> Попробуем сделать так же со второй картой:\n")
    status, message = c_card.add_payment("Коммунальные услуги", 100.0)
    assert not status

    info(message)

    info("### Накопительные счета")
    info("> Создадим накопительный счет для ребенка со ставкой в 5%")
    info("> и от лица родителя переведем ребенку 500₽.")
    info("> На накопительном счете ребенка окажется 500\\*5/100=25₽\n")

    status, message = c_target.open_savings_account(ante=5.0)
    assert status
    info(message)

    c_account = next(c_target.get_savings_account())

    c_card.set_account(c_account)
    status, message = card.transfer(c_card, 500.0)
    assert status
    info(message)

    info(c_card)
    info(c_account)

    info("### Инвестиционные счета")
    info("> От лица взрослого откроем инвестиционный счет")
    info("> со стартовым взносом в 400₽.")
    info("> Для открытия счетов используются наличные деньги:\n")

    status, message = target.open_investment_account(400.0)
    assert not status

    info(message)
    info("> Разумеется, их нужно предварительно получить:\n")

    target.set_cash(target.get_cash() + 400.0)
    status, message = target.open_investment_account(400.0)
    assert status

    info(message)
    info("> Теперь обновим статус этот счета:\n")

    account = next(target.get_investment_account())
    while not account._is_frozen():
        status, message = account.update()

    info(message)
    info("> Попробуем обновить статус еще раз:\n")
    status, message = account.update()
    assert not status

    info(message)
    info("> И также попробуем снять с него денежные средства:\n")

    status, message = account.withdraw(card, account._get_balance())
    assert not status

    info(message)


def main():
    script_path = os.path.dirname(os.path.realpath(__file__))

    demo_path = os.path.join(script_path, "lab4_demo.md")
    data_path = os.path.join(script_path, "people_cards.json")

    basicConfig(filename=demo_path, filemode="w", format="%(message)s", level=INFO)

    people = list(process_data(data_path))
    demo(people)


if __name__ == "__main__":
    main()

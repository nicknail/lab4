from typing import Type

from lab4.gists.account import *
from lab4.utils.printer import *


P = Printer()


class Person:
    def __init__(self, first_name: str, last_name: str, cards: list):
        self.set_name(first_name, last_name)
        self.set_cards(cards)
        self.set_cash(0.0)
        self.accounts = list()

    def __str__(self) -> str:
        return P("person.base") % (
            self.get_name(),
            self.get_card_string(),
            self.get_cash(),
        )

    def get_name(self) -> str:
        return "%s %s" % (self.first_name, self.last_name)

    def set_name(self, first_name: str, last_name: str):
        if not first_name or not last_name:
            raise ValueError(P("error.empty_name"))

        self.first_name = first_name
        self.last_name = last_name

    def get_cards(self) -> list:
        return self.cards

    def get_card_string(self) -> str:
        match len(self.get_cards()):
            case 0:
                return P("person.wealth.no_cards")
            case 1:
                return P("person.wealth.one_card")
            case _:
                return P("person.wealth.many_cards") % len(self.get_cards())

    def set_cards(self, cards: list):
        self.cards = cards

    def get_cash(self) -> float:
        return self.cash

    def set_cash(self, amount: float):
        self.cash = round(amount, 2)

    def get_accounts(self) -> Type[Account]:
        for account in self.accounts:
            yield account

    def get_savings_account(self):
        for account in self.get_accounts():
            if not isinstance(account, SavingsAccount):
                continue
            yield account

    def add_account(self, account: Type[Account]):
        self.accounts.append(account)

    def open_savings_account(self, amount: float = 0.0, ante: float = 0.0) -> tuple:
        if amount < 0.0 or ante < 0.0:
            return False, P("account.savings.bad_amount")
        if amount > self.get_cash():
            return False, P("person.cash.no_cash")

        self.set_cash(self.get_cash() - amount)
        self.add_account(SavingsAccount(amount, ante))
        return True, P("account.savings.success") % (amount, ante)


class Adult(Person):
    def __init__(self, first_name: str, last_name: str, cards: list, children: list):
        super().__init__(first_name, last_name, cards)
        self.set_children(children)
        self.set_wage(0.0)

    def __str__(self) -> str:
        string = super().__str__()

        if children := self.get_children():
            string += P("person.children") % (
                self.get_wage(),
                "\n".join(
                    P("person.child") % (c.get_name(), c.get_age()) for c in children
                ),
            )
        return string

    def get_children(self) -> list:
        return self.children

    def set_children(self, children: list):
        self.children = children

    def give_cash(self, _to, amount: float) -> tuple:
        if amount < 0:
            return False, P("person.cash.bad_amount")
        if amount > self.get_cash():
            return False, P("person.cash.no_cash")

        self.set_cash(self.get_cash() - amount)
        _to.set_cash(_to.get_cash() + amount)

        return True, P("person.cash.success")

    def get_investment_account(self):
        for account in self.get_accounts():
            if not isinstance(account, InvestmentAccount):
                continue
            yield account

    def open_investment_account(self, amount: float = 0.0) -> tuple:
        if amount < 0.0:
            return False, P("account.investment.bad_amount")
        if amount > self.get_cash():
            return False, P("person.cash.no_cash")

        self.set_cash(self.get_cash() - amount)
        self.add_account(InvestmentAccount(amount))
        return True, P("account.investment.success") % amount

    def get_wage(self) -> float:
        return self.wage

    def set_wage(self, amount: float):
        self.wage = round(amount, 2)

    # Возвращает статус операции и сообщение
    def paycheck(self) -> tuple:
        if not (cards := self.get_cards()):
            return False, P("card.paycheck.no_cards")
        status = cards[0].receive_funds(self.get_wage())

        if status:  # :trollface:
            self.set_wage(self.get_wage() * 2 / 3)
        return status, (
            P("card.paycheck.success") if status else P("card.addition.bad_amount")
        )


class Child(Person):
    def __init__(self, first_name: str, last_name: str, cards: list, age: int):
        super().__init__(first_name, last_name, cards)
        self.set_age(age)

    def __str__(self) -> str:
        return super().__str__() + P("person.age") % self.get_age()

    def get_age(self) -> int:
        return self.age

    def set_age(self, age: int):
        if age < 0:
            raise ValueError(P("error.neg_age") % age)
        self.age = age


def main():
    print("Этот модуль необходим для работы с классами людей")
    print("Класс 'Person' является скелетом, содержащим базовые функции")

    print("Создадим объект ребёнка Butch Tapin:")
    child = Child("Butch", "Tapin", [], 16)
    print(child)
    print()

    print("И создадим объект родителя Gieraths Seline для ребенка:")
    parent = Adult("Gieraths", "Seline", [], [child])
    print(parent)
    print()

    print("Дадим родителю зарплату в 40.000₽ и 2.000₽ на руки:")
    parent.set_wage(40_000.0)
    parent.set_cash(2_000.0)
    print(parent)
    print()

    print("От лица родителя передадим 500₽ на руки ребенку:")
    parent.give_cash(child, 500.0)
    print(parent)
    print(child)
    print()

    print("От лица родителя попробуем получить зарплату:")
    _, message = parent.paycheck()
    print(message)


if __name__ == "__main__":
    main()

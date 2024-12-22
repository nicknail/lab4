from typing import Type

from lab4.gists.account import *
from lab4.gists.person import *
from lab4.utils.printer import *


P = Printer()


class Card:
    def __init__(self, number: str, balance: float):
        self.set_number(number)
        self.set_balance(balance)

        self.set_account(None)
        self.payments = dict()

    def __str__(self) -> str:
        return P("card.base") % (
            self.get_discrete_number(),
            self.get_balance(),
        )

    def get_discrete_number(self) -> str:
        return self.number[-4:]

    def set_number(self, number: str):
        if not number.isdigit():
            raise ValueError(P("error.bad_number") % number)
        self.number = number

    def get_balance(self) -> float:
        return self.balance

    def set_balance(self, amount: float):
        if amount < 0.0:
            raise ValueError(P("error.neg_balance") % amount)
        self.balance = round(amount, 2)

    def get_account(self) -> Type[SavingsAccount] | None:
        return self.account

    def set_account(self, account: Type[SavingsAccount] | None):
        self.account = account

    # Отчисление процентов; возвращает только статус
    def receive_funds(self, amount: float) -> bool:
        if self.account:
            status, leftover = self.account.flow(amount)
        else:
            status, leftover = True, amount

        if status:
            self.set_balance(self.get_balance() + leftover)
        return status

    # Перевод денежных средств
    def transfer(self, receipent, amount: float) -> tuple:
        if amount <= 0.0:
            return False, P("card.withdrawal.bad_amount")

        if amount > self.get_balance():
            return False, P("card.withdrawal.no_funds")

        self.set_balance(self.get_balance() - amount)
        status = receipent.receive_funds(amount)

        return status, (
            P("card.transfer.success") % receipent.get_discrete_number()
            if status
            else P("card.withdrawal.bad_amount")
        )

    # Функции банковских операций вовзращают статусы этих операций и сообщения
    def add_funds(self, user: Type[Person], amount: float) -> tuple:
        if amount <= 0.0:
            return False, P("card.addition.bad_amount")

        if amount > user.get_cash():
            return False, P("card.addition.no_cash")

        user.set_cash(user.get_cash() - amount)
        status = self.receive_funds(amount)

        return status, (
            P("card.addition.success") if status else P("card.addition.bad_amount")
        )

    def withdraw(
        self, user: Type[Person] | None, amount: float, is_checkout: bool
    ) -> tuple:
        if amount <= 0.0:
            return False, P("card.withdrawal.bad_amount")

        if amount > self.get_balance():
            return False, P("card.withdrawal.no_funds")

        self.set_balance(self.get_balance() - amount)
        if not is_checkout:
            user.set_cash(user.get_cash() + amount)

        return True, P("card.withdrawal.success")

    def checkout(
        self, user: Type[Person], item: str, price: float, quantity: int
    ) -> tuple:
        if quantity <= 0:
            return False, P("card.checkout.neg_quantity")
        total = round(price * quantity, 2)

        status, message = self.withdraw(user, total, True)

        args = message, item, price, quantity, total, user.get_name()
        return status, P("card.checkout.base") % args

    # Имя используется как ключ в словаре обязательных платежей
    # Функция ниже возвращает кортеж: статус и размер платежа (если последний существует)
    def get_payment(self, name: str) -> tuple:
        if name in self.payments:
            return True, self.payments[name]
        return False, 0.0

    def add_payment(self, name: str, amount: float) -> tuple:
        if not name or amount <= 0.0:
            return False, P("card.payment.bad_values")
        self.payments[name] = amount
        return True, P("card.payment.success_when_created")

    def make_payment(self, name: str) -> tuple:
        status, amount = self.get_payment(name)
        if not status:
            return False, P("card.payment.not_found")

        status, message = self.withdraw(None, amount, True)
        return status, P("card.payment.success") if status else message


class KidsCard(Card):
    def __init__(self, number: str, balance: float, limit: float):
        super().__init__(number, balance)
        self.set_limit(limit)
        self.payments = None

    def __str__(self) -> str:
        return super().__str__() + P("card.limit") % self.get_limit()

    def get_limit(self) -> float:
        return self.limit

    def set_limit(self, amount: float):
        if amount < 0.0:
            raise ValueError(P("error.neg_limit") % amount)
        self.limit = round(amount, 2)

    def transfer(self, receipent: Type[Card], amount: float) -> tuple:
        return False, P("card.transfer.minor")

    def withdraw(self, user: Type[Child], amount: float, is_checkout: bool) -> tuple:
        if amount > self.get_limit():
            return False, P("card.withdrawal.exceeding")

        status, message = super().withdraw(user, amount, is_checkout)
        if status:
            self.set_limit(self.get_limit() - amount)
        return status, message

    def checkout(
        self, user: Type[Child], item: str, price: float, quantity: int
    ) -> tuple:
        status, message = super().checkout(user, item, price, quantity)
        return status, message + P("card.checkout.age_detail") % user.get_age()

    def get_payment(self, name: str) -> tuple:
        return False, P("card.payment.minor")

    def add_payment(self, name: str, amount: float) -> tuple:
        return False, P("card.payment.minor")

    def make_payment(self, name: str) -> tuple:
        return False, P("card.payment.minor")


def main():
    print("Этот модуль необходим для работы с банковскими картами")
    print("Создадим базовую карту с балансом в 500₽:")
    a = Card("1234", 500.0)
    print(a)
    print()

    print("И создадим детскую карту с балансом в 500₽ и лимитом в 400₽:")
    b = KidsCard("5678", 500.0, 400.0)
    print(b)
    print()

    print("С первой картой переведем на вторую 100₽:")
    a.transfer(b, 100.0)
    print(a)
    print(b)
    print()

    print("Попробуем сделать так же в обратную сторону:")
    _, message = b.transfer(a, 100.0)
    print(message)
    print()

    print("Создадим обязательный платеж 'Коммунальные услуги' на 100₽ и совершим его:")
    a.add_payment("Коммунальные услуги", 100.0)
    _, message = a.make_payment("Коммунальные услуги")
    print(message)
    print(a)
    print()

    print("Попробуем сделать так же со второй картой:")
    _, message = b.add_payment("Коммунальные услуги", 100.0)
    print(message)


if __name__ == "__main__":
    main()

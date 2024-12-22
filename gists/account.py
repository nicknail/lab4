import random

from lab4.utils.printer import *


P = Printer()


class Account:
    def __init__(self, balance: float = 0.0):
        if not self._set_balance(balance):
            raise ValueError(P("error.neg_balance") % balance)

    def __str__(self):
        return P("account.placeholder_base") % self._get_balance()

    @staticmethod
    def _round(amount: float) -> float:
        return round(amount, 2)

    def _get_balance(self) -> float:
        return self.balance

    def _set_balance(self, amount: float) -> bool:
        if amount < 0.0:
            return False
        self.balance = self._round(amount)
        return True

    def add_funds(self, _from, amount: float) -> tuple:
        if amount == 0.0:
            return False, P("card.addition.bad_amount")

        if _from:
            status, _ = _from.withdraw(None, amount, True)
            if not status:
                return False, P("card.addition.no_cash")

        status = self._set_balance(self._get_balance() + amount)
        return status, (
            P("card.addition.success") if status else P("card.addition.bad_amount")
        )

    def withdraw(self, _to, amount: float) -> tuple:
        if amount == 0.0:
            return False, P("card.withdrawal.bad_amount")

        _to.receive_funds(amount)
        status = self._set_balance(self._get_balance() - amount)

        return status, (
            P("card.withdrawal.success") if status else P("card.withdrawal.no_funds")
        )


class SavingsAccount(Account):
    def __init__(self, balance: float = 0.0, ante: float = 0.0):
        super().__init__(balance)
        if not self._set_ante(ante):
            raise ValueError(P("error.neg_ante") % ante)

    def __str__(self):
        return P("account.savings.base") % (self._get_balance(), self._get_ante())

    def _get_ante(self) -> float:
        return self.ante

    def _set_ante(self, amount: float) -> bool:
        if amount < 0:
            return False
        self.ante = self._round(amount)
        return True

    # Отчисление процента (ante) по накопительному счету
    # Возвращает кортеж: статус процедуры и сумму с вычтенным процентом
    def flow(self, amount: float) -> tuple:
        share = self._round(amount * self._get_ante() / 100)
        status, _ = self.add_funds(None, share)
        return status, amount - share if status else amount


class InvestmentAccount(Account):
    def __init__(self, balance: float = 0.0):
        super().__init__(balance)

    def __str__(self):
        return P("account.investment.base") % self._get_balance()

    def _set_balance(self, amount: float) -> bool:
        self.balance = self._round(amount)
        return True

    def _is_frozen(self) -> bool:
        return self._get_balance() < 0

    def withdraw(self, _to, amount: float) -> tuple:
        if self._is_frozen():
            return False, P("account.investment.withdraw_but_frozen")
        return super().withdraw(_to, amount)

    # Обновление состояния инвестиционного счета
    def update(self) -> tuple:
        if self._is_frozen():
            return False, P("account.investment.update_but_frozen")
        self._set_balance(float(random.randint(-500, 500)))
        return True, P("account.investment.update_success") % self._get_balance()


def main():
    print("Этот модуль необходим для работы с накопительными и инвестиционными счетами")
    print(
        "Класс 'Account' является скелетом, содержащим базовые функции для работы основных счетов"
    )
    print()

    print("Создадим накопительный счет с балансом в 500₽ и ставкой (ante) в 10%")
    print("и выведем его в виде строки:")
    account = SavingsAccount(500.0, 10.0)
    print(account)
    print()

    print("Отчислим процент с покупки в 100₽ на счет и выведем строку еще раз:")
    account.flow(100.0)
    print(account)
    print()

    print("Создадим инвестиционный счет со стартовым балансом в 200₽")
    print("и выведем его в виде строки:")
    account = InvestmentAccount(200.0)
    print(account)
    print()

    print("Обновим статус счета и выведем строку еще раз:")
    account.update()
    print(account)
    print()

    if account._is_frozen():
        print("Теперь счет заморожен. Попробуем вывести с него все деньги:")
    else:
        print(
            "Баланс остался положительным, потому счет не заморожен. Выведем с него деньги:"
        )
    _, message = account.withdraw(account._get_balance())
    print(message)
    print(account)


if __name__ == "__main__":
    main()

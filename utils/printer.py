class Printer:
    MESSAGES = {
        "person": {
            "base": "I'm %s.%s I have %g₽ in cash",
            "wealth": {
                "no_cards": " I don't have any debit cards.",
                "one_card": " I have 1 debit card.",
                "many_cards": " I have %s debit cards.",
            },
            "children": ". I also have a wage of %g₽. Here are my children:\n\n%s",
            "child": "- %s, they are %s years old",
            "age": " and I am %s years old",
            "cash": {
                "no_cash": "Incomplete! Not enough cash",
                "bad_amount": "Incomplete! Illegal amount",
                "success": "Complete. Cash given",
            },
        },
        "card": {
            "base": "Card %s has %g₽ on its balance",
            "limit": ". It also has a limit of %g₽",
            "addition": {
                "bad_amount": "Transaction incomplete! Illegal amount",
                "no_cash": "Transaction incomplete! Not enough money",
                "success": "Transaction complete. Funds added",
            },
            "withdrawal": {
                "bad_amount": "Transaction incomplete! Illegal amount",
                "no_funds": "Transaction incomplete! Insufficient funds",
                "exceeding": "Transaction incomplete! Exceeding limit",
                "success": "Transaction complete. Funds withdrawn",
            },
            "checkout": {
                "base": (
                    "%s\n\n"  # Статус транзакции
                    "##### CHECKOUT DETAILS\n\n"
                    "- Item: %s\n"
                    "- Price: %g₽\n"
                    "- Quantity: %s\n"
                    "- Total cost: %g₽\n\n"
                    "- Client name: %s"
                ),
                "age_detail": "\n- Client age: %s",
                "neg_quantity": "Transaction incomplete! Illegal quantity",
            },
            "paycheck": {
                "no_cards": "Transaction incomplete! No cards registered",
                "success": "Transaction complete. Salary transferred",
            },
            "transfer": {
                "minor": "Transaction incomplete! Kids cannot transfer money",
                "success": "Transaction complete. Funds transferred to card %s",
            },
            "payment": {
                "bad_values": "Cannot create an obligatory payment! Illegal values",
                "success_when_created": "Successfully created an obligatory payment '%s' for %g₽",
                "not_found": "Transaction incomplete! Payment not found",
                "success": "Transaction complete. Obligatory payment made",
                "minor": "Kids cannot create or make obligatory payments",
            },
        },
        "account": {
            "placeholder_base": "This placeholder account has %g₽",
            "savings": {
                "base": "This savings account has %g₽ and an ante of %g%%",
                "bad_amount": "Cannot open account! Illegal starting values",
                "success": "Account successfully created with a balance of %g₽ and an ante of %g%%",
            },
            "investment": {
                "base": "This investment account has %g₽",
                "bad_amount": "Cannot open account! Illegal starting balance",
                "success": "Account successfully created with a balance of %g₽",
                "withdraw_but_frozen": "Cannot withdraw! Account is frozen",
                "update_but_frozen": "Cannot update the account! Account is frozen",
                "update_success": "Account updated. Now it has %g₽",
            },
        },
        "error": {
            "empty_name": "name instance can't be blank",
            "neg_age": "age must be greater than zero: '%s'",
            "bad_number": "bad card number: '%s'",
            "neg_balance": "balance can't be negative: '%g'",
            "neg_limit": "limit must be greater than zero: '%g'",
            "neg_ante": "ante can't be negative: '%g'",
        },
    }

    def __call__(self, keys: str) -> str:
        text = self.MESSAGES
        for key in keys.split("."):
            text = text[key]
        return text


def main():
    print("Этот модуль необходим для обработки вывода программы")
    print("Функция класса принимат на вход строку вида 'block1.block2.value',")
    print("эквивалентную MESSAGES['block1']['block2']['value']")
    print()

    P = Printer()

    print("Вывод строки без аргументов на примере 'person.wealth.one_card':")
    print(P("person.wealth.one_card"))
    print()

    print("Вывод строки с аргументами на примере 'person.wealth.many_cards':")
    print(P("person.wealth.many_cards"))
    print()

    print("Добавим аргумент через оператор %:")
    print(P("person.wealth.many_cards") % 42)


if __name__ == "__main__":
    main()

# Как устанавливается?

```shell
git clone https://github.com/nicknail/lab4
```

# Как запускается…

### Основная демонстрация?

```shell
python -m lab4.main
```

### Локальная демонстрация?

```shell
python -m lab4.gists.account
python -m lab4.gists.card
python -m lab4.gists.person
python -m lab4.utils.printer
```

---

- Для корректной работы запускать демонстрации следует из папки на одну выше, чем папка проекта
- Если не распознаются модули, рекурсивно добавьте `__init__.py` в папку проекта

# Как проверяется?

- Ввод читается из файла `lab4/people_cards.json`
- Вывод сохраняется в файле `lab4/lab4_demo.md`. Прочитать его можно любым редактором, поддерживающим отрисовку Markdown
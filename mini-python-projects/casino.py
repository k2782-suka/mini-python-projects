import random
import time


def get_bet(balance):
    while True:
        try:
            bet = int(input(f"Введите ставку (баланс: {balance}): "))

            if 1 <= bet <= balance:
                return bet

            print("Ставка должна быть больше 0 и не превышать баланс.")
        except ValueError:
            print("Введите целое число.")


def roulette(balance):
    print("\n--- РУЛЕТКА ---")
    bet = get_bet(balance)

    print("Выберите ставку:")
    print("1 — красное/чёрное, множитель x2")
    print("2 — чётное/нечётное, множитель x2")
    print("3 — конкретное число от 0 до 36, множитель x36")

    choice = input("Ваш выбор: ").strip()

    if choice == "1":
        user_color = input("Выберите цвет — красное или чёрное: ").lower()

        if user_color not in ("красное", "черное", "чёрное"):
            print("Неверный цвет.")
            return balance

        number = random.randint(0, 36)

        if number == 0:
            color = "зелёное"
        else:
            color = random.choice(["красное", "чёрное"])

        print(f"Выпало число {number}, цвет: {color}")

        if user_color == color:
            print("Вы выиграли!")
            return balance + bet
        else:
            print("Вы проиграли.")
            return balance - bet

    elif choice == "2":
        parity = input("Выберите — чётное или нечётное: ").lower()

        if parity not in ("чётное", "четное", "нечётное", "нечетное"):
            print("Неверный вариант.")
            return balance

        number = random.randint(0, 36)
        print(f"Выпало число: {number}")

        if number == 0:
            print("Ноль — вы проиграли.")
            return balance - bet

        result = "чётное" if number % 2 == 0 else "нечётное"

        if parity.replace("е", "ё") == result:
            print("Вы выиграли!")
            return balance + bet
        else:
            print("Вы проиграли.")
            return balance - bet

    elif choice == "3":
        try:
            selected_number = int(input("Введите число от 0 до 36: "))

            if not 0 <= selected_number <= 36:
                print("Число должно быть от 0 до 36.")
                return balance

            number = random.randint(0, 36)
            print(f"Выпало число: {number}")

            if selected_number == number:
                print("Джекпот! Вы выиграли x36!")
                return balance + bet * 35
            else:
                print("Вы проиграли.")
                return balance - bet

        except ValueError:
            print("Введите целое число.")
            return balance

    else:
        print("Неверный выбор.")
        return balance


def slots(balance):
    print("\n--- СЛОТЫ ---")
    bet = get_bet(balance)

    symbols = ["🍒", "🍋", "🔔", "⭐", "💎"]
    result = [random.choice(symbols) for _ in range(3)]

    print("Крутим барабаны...")
    time.sleep(1)
    print(" | ".join(result))

    if result[0] == result[1] == result[2]:
        winnings = bet * 10
        print(f"Джекпот! Вы выиграли {winnings} монет.")
        return balance + winnings - bet

    elif len(set(result)) == 2:
        winnings = bet * 2
        print(f"Два одинаковых символа! Вы выиграли {winnings} монет.")
        return balance + winnings - bet

    else:
        print("Увы, вы проиграли.")
        return balance - bet


def casino():
    balance = 1000

    print("Добро пожаловать в мини-казино!")
    print("Ваш стартовый баланс: 1000 монет.")

    while balance > 0:
        print(f"\nВаш баланс: {balance}")
        print("1 — Рулетка")
        print("2 — Слоты")
        print("3 — Выйти")

        choice = input("Выберите игру: ").strip()

        if choice == "1":
            balance = roulette(balance)
        elif choice == "2":
            balance = slots(balance)
        elif choice == "3":
            print(f"Вы вышли из игры с балансом {balance} монет.")
            break
        else:
            print("Неверный выбор.")

    if balance <= 0:
        print("\nБаланс закончился. Игра окончена.")


if __name__ == "__main__":
    casino()

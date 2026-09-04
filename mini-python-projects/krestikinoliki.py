def print_board(board):
    print()
    for i in range(3):
        print(f" {board[i][0]} | {board[i][1]} | {board[i][2]} ")
        if i < 2:
            print("---+---+---")
    print()


def check_winner(board, player):
    
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    if all(board[i][i] == player for i in range(3)):
        return True

    if all(board[i][2 - i] == player for i in range(3)):
        return True

    return False


def is_board_full(board):
    return all(cell != " " for row in board for cell in row)


def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    print("Крестики-нолики")
    print("Вводите номер клетки от 1 до 9:")
    print("""
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
""")

    while True:
        print_board(board)

        try:
            choice = int(input(f"Ход игрока {current_player}: "))

            if choice < 1 or choice > 9:
                print("Введите число от 1 до 9.")
                continue

            row = (choice - 1) // 3
            col = (choice - 1) % 3

            if board[row][col] != " ":
                print("Эта клетка уже занята.")
                continue

            board[row][col] = current_player

            if check_winner(board, current_player):
                print_board(board)
                print(f"Игрок {current_player} победил!")
                break

            if is_board_full(board):
                print_board(board)
                print("Ничья!")
                break

            current_player = "O" if current_player == "X" else "X"

        except ValueError:
            print("Введите целое число от 1 до 9.")


if __name__ == "__main__":
    main()

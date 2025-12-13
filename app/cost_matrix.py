ROWS = 12
COLS = 4
COL_LABELS = ["A", "B", "C", "D"]


def get_cost_matrix():
    return [[100, 75, 50, 100] for _ in range(ROWS)]


def print_cost_matrix(matrix):
    print("\nSeat Cost Matrix (in dollars)\n")
    print("     A     B     C     D")
    print("     " + "-" * 26)

    for row_idx in range(ROWS):
        row_num = row_idx + 1
        prices = matrix[row_idx]
        print(
            f"Row {row_num:2} | "
            f"{prices[0]:>3}   "
            f"{prices[1]:>3}   "
            f"{prices[2]:>3}   "
            f"{prices[3]:>3}"
        )
    print()


def parse_seat_code(seat_code):
    seat_code = seat_code.strip().upper()

    if len(seat_code) < 2 or len(seat_code) > 3:
        raise ValueError("Seat code must look like '1A', '10C', etc.")

    row_part = seat_code[:-1]
    col_part = seat_code[-1]

    if not row_part.isdigit():
        raise ValueError("Row must be a number (1-12).")

    row_num = int(row_part)
    if row_num < 1 or row_num > ROWS:
        raise ValueError("Row out of range (1-12).")

    if col_part not in COL_LABELS:
        raise ValueError("Column must be A, B, C, or D.")

    return row_num - 1, COL_LABELS.index(col_part)


def seat_rowcol_to_code(row_num, col_num):
    if row_num < 1 or row_num > ROWS:
        raise ValueError("Row out of range (1-12).")
    if col_num < 1 or col_num > COLS:
        raise ValueError("Column out of range (1-4).")

    return f"{row_num}{COL_LABELS[col_num - 1]}"


def get_seat_price_by_code(matrix, seat_code):
    row_index, col_index = parse_seat_code(seat_code)
    return matrix[row_index][col_index]


def get_seat_price_by_rowcol(matrix, row_num, col_num):
    seat_code = seat_rowcol_to_code(row_num, col_num)
    return get_seat_price_by_code(matrix, seat_code)


def main():
    cost_matrix = get_cost_matrix()

    while True:
        print("=======Cost Matrix Menu=======")
        print("1. Show full cost matrix")
        print("2. Look up price by seat code")
        print("3. Look up price by row/column")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            print_cost_matrix(cost_matrix)

        elif choice == "2":
            seat_code = input("Enter seat (e.g., 1A, 5C): ")
            try:
                price = get_seat_price_by_code(cost_matrix, seat_code)
                print(f"The price for seat {seat_code.upper()} is: ${price}\n")
            except ValueError as e:
                print(f"Error: {e}\n")

        elif choice == "3":
            try:
                row_num = int(input("Enter seat row (1-12): "))
                col_num = int(input("Enter seat column (1-4): "))
                seat_code = seat_rowcol_to_code(row_num, col_num)
                price = get_seat_price_by_rowcol(cost_matrix, row_num, col_num)
                print(f"The price for seat {seat_code} is: ${price}\n")
            except ValueError as e:
                print(f"Error: {e}\n")

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.\n")


if __name__ == "__main__":
    main()

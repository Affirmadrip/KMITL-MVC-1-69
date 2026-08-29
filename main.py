from controller import ContestController
from views import EntryView, ResultView

SEED_PATH = "seed_data.json"

MENU = """
========== Ladkrabang's Got Talent ==========
1) List contestants
2) View contestant detail
3) Submit a normal decision (PASS/FAIL)
4) Use Golden Buzzer
5) View final summary
0) Exit
==============================================
"""


def main():
    controller = ContestController.load_from_seed(SEED_PATH)
    entry_view = EntryView(controller)
    result_view = ResultView(controller)

    while True:
        print(MENU)
        choice = input("Choose an option: ").strip()

        if choice == "1":
            entry_view.display_contestants()

        elif choice == "2":
            cid = input("Contestant id (e.g. P01): ").strip().upper()
            entry_view.display_contestant_detail(cid)

        elif choice == "3":
            jid = input("Judge id (e.g. J01): ").strip().upper()
            cid = input("Contestant id (e.g. P01): ").strip().upper()
            result = input("Result (PASS/FAIL): ").strip().upper()
            entry_view.submit_decision(jid, cid, result)

        elif choice == "4":
            jid = input("Judge id (e.g. J01): ").strip().upper()
            cid = input("Contestant id (e.g. P01): ").strip().upper()
            entry_view.use_golden_buzzer(jid, cid)

        elif choice == "5":
            result_view.display_summary()

        elif choice == "0":
            print("Goodbye")
            break

        else:
            print("Invalid option, please try again")


if __name__ == "__main__":
    main()

"""
This file covers the command line interface (CLI) which is exposed to the user and allows choosing between five
main menu options with additional sub-options as well as the option to exit the app:

(1) Check Off habits
------------------------
    1.1 Current datetime
    1.2 Specific datetime
        Includes validation rules for the datetime format (YYYY-MM-DD hh:mm:ss) and checks that the entered datetime
        is not in the future

(2) Create new habits
------------------------
    2.1 Habit from List
        Allows choosing a habit from a list of five pre-defined habits with pre-defined task and periodicity
    2.2 New Habit
        Allows creating a new habit in terms of free-text field habit name and task as well as free periodicity choice
        (daily or weekly)
    In both cases, a checking mechanism is available making sure that the same habit name is not entered twice.

(3) Modify habits
------------------------
    In a first instance, the habit to be modified has to be chosen from a list showing all available habit names.
    If tracking data is available for the selected habit, the user can choose whether it should be kept or deleted.
    In a next step, the user can choose whether only the task, only the periodicity or both should be modified.

(4) Delete habits
------------------------
    4.1 All
        Allows deleting all habits including their tracking data at once.
        Due to the impact, a message is shown asking for confirmation that all habits should be deleted.
    4.2 Individual
        Allows deleting one habit and its respective tracking data (if available).
        The habit to be deleted can be selected from a list showing all available habit names.

(5) Analyse habits
------------------------
    5.1 List of all currently tracked habits
    5.2 List of all habits with the same periodicity
        Choice between "daily" and "weekly"
    5.3 Longest run streak of all defined habits
    5.4 Longest run streak for a given habit
        Selection of a habit name from a list showing all available habits

(6) Exit
------------------------

Within each option, the possibility is given to return to the main menu without any implications by clicking on
"Back to Menu".

questionary is imported as an intuitive CLI thereby connecting respective choices and selection options to the habits
being available in the database which is the reason why the database file is imported to this file as well.
In addition, the Habit class is imported from habits as well as the file "analyse" to provide the user with all the
analysis functions.
The imported datetime module is used for the storage as well as validation of check-off dates.
Pandas is imported as a basis for manipulating the data and performing the respective analysis functions.
Tabulate supports the displaying of the data in a clean tabular structure.

"""


import questionary
import datetime

import database
from habits import Habit
import analyse
import pandas as pd
from tabulate import tabulate


def cli():

    start_message = """
    ***************************************************************
                  Welcome to your Habit Tracker.              
            Choose one of below menu options to get started.
    ***************************************************************
    """
    print(start_message)

    db = database.get_db()

    stop = False
    while not stop:

        is_valid_list = True
        list_db_habits = list(map(lambda x: x[1], database.get_habit_data(db)))
        if not list_db_habits:
            is_valid_list = False

        if is_valid_list is True:
            choice = questionary.select(
                "What do you want to do?",
                choices=["Create", "Check Off", "Modify", "Delete", "Analyse", "Exit"]).ask()
        else:
            choice = questionary.select(
                "What do you want to do?",
                choices=["Create", "Exit"]).ask()

        if choice == "Create":
            choice_sub = questionary.select("Do you want to choose a habit from a predefined list or do you want "
                                            "to create a new habit?",
                                            choices=["Habit from List", "New Habit", "Back to Menu"]).ask()

            if not list_db_habits:
                is_valid_list = False

            if choice_sub == "Habit from List":
                choice_sub_2 = questionary.select("Please choose a habit from below list:", choices=[
                    "1. Studying | weekly | Study a specific or new subject for at least 10 hours per week",
                    "2. Jogging | weekly | Go jogging at least once per week",
                    "3. Cleaning | weekly | Clean all rooms",
                    "4. Waking up | daily | Wake up at 5am every morning",
                    "5. Doing Workout | daily | Doing workout each day for at least 15 minutes",
                    "6. Back to Menu"]).ask()

                if choice_sub_2 == "1. Studying | weekly | Study a specific or new subject for at least 10 " \
                                   "hours per week":
                    name = "Studying"
                    if is_valid_list is True and name in list_db_habits:
                        print(f"The habit with the name {name} does already exist. Please choose a different habit")
                    else:
                        task = "Study a specific or new subject for at least 10 hours per week"
                        periodicity = "weekly"
                        habit = Habit(name, task, periodicity)
                        habit.store_habit(db)
                        print(f"Habit {name} successfully created.")

                elif choice_sub_2 == "2. Jogging | weekly | Go jogging at least once per week":
                    name = "Jogging"
                    if is_valid_list is True and name in list_db_habits:
                        print(f"The habit with the name {name} does already exist. Please choose a different habit")
                    else:
                        task = "Go jogging at least once per week"
                        periodicity = "weekly"
                        habit = Habit(name, task, periodicity)
                        habit.store_habit(db)
                        print(f"Habit {name} successfully created.")

                elif choice_sub_2 == "3. Cleaning | weekly | Clean all rooms":
                    name = "Cleaning"
                    if is_valid_list is True and name in list_db_habits:
                        print(f"The habit with the name {name} does already exist. Please choose a different habit")
                    else:
                        task = "Clean all rooms"
                        periodicity = "weekly"
                        habit = Habit(name, task, periodicity)
                        habit.store_habit(db)
                        print(f"Habit {name} successfully created.")

                elif choice_sub_2 == "4. Waking up | daily | Wake up at 5am every morning":
                    name = "Waking up"
                    if is_valid_list is True and name in list_db_habits:
                        print(f"The habit with the name {name} does already exist. Please choose a different habit")
                    else:
                        task = "Wake up at 5am every morning"
                        periodicity = "daily"
                        habit = Habit(name, task, periodicity)
                        habit.store_habit(db)
                        print(f"Habit {name} successfully created.")

                elif choice_sub_2 == "5. Doing Workout | daily | Doing workout each day for at least 15 minutes":
                    name = "Doing Workout"
                    if is_valid_list is True and name in list_db_habits:
                        print(f"The habit with the name {name} does already exist. Please choose a different habit")
                    else:
                        task = "Doing workout each day for at least 15 minutes"
                        periodicity = "daily"
                        habit = Habit(name, task, periodicity)
                        habit.store_habit(db)
                        print(f"Habit {name} successfully created.")
                else:
                    ""

            elif choice_sub == "New Habit":
                name = questionary.text("What's the name of the habit which you want to create?").ask()

                if is_valid_list is True and name in list_db_habits:
                    print(f"The habit with the name {name} does already exist. Please enter a different habit name")
                else:
                    task = questionary.text("What's the task?").ask()
                    periodicity = str(questionary.select("What's the periodicity?", choices=["daily", "weekly"]).ask())
                    habit = Habit(name, task, periodicity)
                    habit.store_habit(db)
                    print(f"Habit {name} successfully created.")
            else:
                ""

        elif choice == "Check Off":
            name = str(questionary.select("Which habit do you want to check off?", choices=list_db_habits).ask())
            date_choice = str(questionary.select("Do you want to enter a specific datetime or save the current "
                                                 "datetime?", choices=["Current datetime", "Specific datetime",
                                                                       "Back to Menu"]).ask())

            if date_choice == "Specific datetime":
                date_chosen = questionary.text("Please enter a datetime when you completed the habit "
                                               "(YYYY-MM-DD hh:mm)").ask()
                is_valid_date = True
                try:
                    datetime.datetime.strptime(date_chosen, "%Y-%m-%d %H:%M")
                except ValueError:
                    print("This is not the correct date format (YYYY-MM-DD hh:mm)")
                    is_valid_date = False

                if is_valid_date is True and datetime.datetime.strptime(str(date_chosen), "%Y-%m-%d %H:%M") <= \
                        datetime.datetime.today():
                    tracking = Habit(name, "null", "null")
                    print(f"Habit {name} successfully checked-off.")
                    tracking.check_off_habit(db, name, date_chosen)
                elif is_valid_date is True and datetime.datetime.strptime(str(date_chosen), "%Y-%m-%d %H:%M") >= \
                        datetime.datetime.today():
                    print("Your entered date is in the future. "
                          "Please select the current date or enter a date in the past.")
                else:
                    ""
            elif date_choice == "Current datetime":
                date_chosen = datetime.datetime.today()
                tracking = Habit(name, "null", "null")
                print(f"Habit {name} successfully checked-off.")
                tracking.check_off_habit(db, name, date_chosen)
            else:
                ""

        elif choice == "Modify":
            name = str(questionary.select("Which habit do you want to modify?", choices=list_db_habits).ask())

            habit_name_id = int("".join(str(x) for x in (list(map(lambda x: x[0],
                                                                  (filter(lambda y: y[1] == name,
                                                                          database.get_habit_data(db))))))))

            list_tracking_ids = list(map(lambda x: x[0], database.get_tracking_data(db)))

            verify_tracking_deletion = ""
            if habit_name_id in list_tracking_ids:
                verify_tracking_deletion = questionary.select("Do you want to keep or delete the existing "
                                                              "tracking data?",
                                                              choices=["Keep", "Delete", "Back to Menu"]).ask()
            else:
                ""

            if verify_tracking_deletion == "Back to Menu":
                ""
            else:
                choice_sub = questionary.select("What do you want to modify?",
                                                choices=["Task", "Periodicity", "Task and Periodicity",
                                                         "Back to Menu"]).ask()
                if choice_sub == "Task":
                    task = questionary.text("Please enter an updated task specification:").ask()
                    habit = Habit(name, task, "null")
                    habit.modify_habit_task(db)
                    if verify_tracking_deletion == "Delete":
                        habit.delete_tracking_data(db)
                    else:
                        ""
                    print(f"Task for Habit {name} successfully modified to: {task}")
                elif choice_sub == "Periodicity":
                    periodicity = str(questionary.select("Please select an updated periodicity:",
                                                         choices=["daily", "weekly"]).ask())
                    habit = Habit(name, "null", periodicity)
                    habit.modify_habit_periodicity(db)
                    if verify_tracking_deletion == "Delete":
                        habit.delete_tracking_data(db)
                    else:
                        ""
                    print(f"Periodicity for Habit {name} successfully modified to {periodicity}.")
                elif choice_sub == "Task and Periodicity":
                    task = questionary.text("Please enter an updated task specification:").ask()
                    periodicity = str(questionary.select("Please select an updated periodicity:",
                                                         choices=["daily", "weekly"]).ask())
                    habit = Habit(name, task, periodicity)
                    habit.modify_habit(db)
                    if verify_tracking_deletion == "Delete":
                        habit.delete_tracking_data(db)
                    else:
                        ""
                    print(f"Periodicity for Habit {name} successfully modified to {periodicity} "
                          f"and Task updated to: {task}")
                else:
                    ""

        elif choice == "Delete":
            choice_sub = questionary.select("Do you want to delete all your habits or only individual ones?",
                                            choices=["Individual", "All", "Back to Menu"]).ask()
            if choice_sub == "All":
                verify = questionary.confirm("Do you really want to delete all your habits and respective "
                                             "tracking data?").ask()
                if verify is True:
                    database.delete_all_habit_tracking_data(db)
                    print(f"All habits have been deleted.")
                else:
                    ""
            elif choice_sub == "Individual":
                name = str(questionary.select("What's the name of the habit which you want to delete?",
                                              choices=list_db_habits).ask())

                habit = Habit(name, "null", "null")

                habit_name_id = int("".join(str(x) for x in (list(map(lambda x: x[0],
                                                                      (filter(lambda y: y[1] == name,
                                                                              database.get_habit_data(db))))))))
                list_tracking_ids = list(map(lambda x: x[0], database.get_tracking_data(db)))
                if habit_name_id in list_tracking_ids:
                    habit.delete_tracking_data(db)
                    habit.delete_habit_data(db)
                else:
                    habit.delete_habit_data(db)
                print(f"Habit {name} successfully deleted.")
            else:
                ""

        elif choice == "Analyse":
            choice_sub = questionary.select("Please choose an analysis option:",
                                            choices=["List of all currently tracked habits",
                                                     "List of all habits with the same periodicity",
                                                     "Longest run streak of all defined habits",
                                                     "Longest run streak for a given habit",
                                                     "Back to Menu"]).ask()

            if choice_sub == "List of all currently tracked habits":
                data = analyse.all_habits(db)
                df = pd.DataFrame(data)
                df.drop(columns=[0], inplace=True)
                print(tabulate(df, headers=["Name", "Specification", "Periodicity", "Creation Time",
                                            "Last Update Date"], tablefmt='psql', showindex=False))

            elif choice_sub == "List of all habits with the same periodicity":
                periodicity = str(questionary.select("Please choose the periodicity of your choice:",
                                                     choices=["daily", "weekly"]).ask())
                data = analyse.all_habits_periodicity(db, periodicity)
                df = pd.DataFrame(data)
                if len(df) == 0:
                    print(f"There are currently no habits stored with periodicity {periodicity}")
                else:
                    df.drop(columns=[0], inplace=True)
                    print(tabulate(df, headers=["Name", "Specification", "Periodicity", "Creation Time",
                                                "Last Update Date"],
                                   tablefmt='psql', showindex=False))

            elif choice_sub == "Longest run streak of all defined habits":
                data = analyse.max_streak(db)
                if str(data) == "There is currently no tracking data available":
                    print("There is currently no tracking data available")
                else:
                    df = pd.DataFrame(data)
                    print(tabulate(df, headers=["Name", "Periodicity", "Longest Run Streak"], tablefmt='psql',
                                   showindex=False))

            elif choice_sub == "Longest run streak for a given habit":
                name = str(questionary.select("Which habit do you want to analyse?", choices=list_db_habits).ask())
                data = analyse.max_streak_habit(db, name)
                if str(data) == f"There is no tracking data available for the habit {name}":
                    print(f"There is no tracking data available for the habit {name}")
                else:
                    df = pd.DataFrame(data)
                    print(tabulate(df, headers=["Name", "Periodicity", "Longest Run Streak"], tablefmt='psql',
                                   showindex=False))

            else:
                ""
        else:
            print("""
    ***************************************************************
                Thanks for using the habit tracker app. 
        Keep up with tracking your habits or creating new ones.
    ***************************************************************
            """)
            stop = True


if __name__ == '__main__':
    cli()

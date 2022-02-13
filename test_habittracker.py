
from database import get_db, add_habit_data, tracking_habit, create_table_tracking, create_table_habit, \
    get_habit_data, get_tracking_data, delete_all_habit_tracking_data
from analyse import all_habits, all_habits_periodicity, max_streak, max_streak_habit
from habits import Habit
import datetime


class TestHabit:

    # Setup method for adding testing data including habit and tracking data
    def setup_method(self):
        self.db = get_db("test.db")

        create_table_habit(self.db)
        add_habit_data(self.db, "Studying", "Study a specific or new subject for at least 10 hours per week", "weekly")
        add_habit_data(self.db, "Jogging", "Go jogging at least once per week", "weekly")
        add_habit_data(self.db, "Cleaning", "Clean all rooms", "weekly")
        add_habit_data(self.db, "Waking up", "Wake up at 5am every morning", "daily")
        add_habit_data(self.db, "Doing Workout", "Doing workout each day for at least 15 minutes", "daily")

        create_table_tracking(self.db)
        tracking_habit(self.db, 1, "2021-11-01 06:23")
        tracking_habit(self.db, 2, "2021-11-01 06:31")
        tracking_habit(self.db, 3, "2021-11-01 08:14")
        tracking_habit(self.db, 4, "2021-11-03 19:27")
        tracking_habit(self.db, 5, "2021-11-15 21:56")
        tracking_habit(self.db, 1, "2021-11-06 21:45")
        tracking_habit(self.db, 1, "2021-11-11 19:34")
        tracking_habit(self.db, 1, "2021-11-21 15:32")
        tracking_habit(self.db, 1, "2021-11-22 12:01")
        tracking_habit(self.db, 2, "2021-11-07 12:21")
        tracking_habit(self.db, 2, "2021-11-19 20:15")
        tracking_habit(self.db, 2, "2021-11-21 08:24")
        tracking_habit(self.db, 3, "2021-11-06 16:45")
        tracking_habit(self.db, 3, "2021-11-12 18:41")
        tracking_habit(self.db, 3, "2021-11-22 07:34")
        tracking_habit(self.db, 3, "2021-11-27 16:32")
        tracking_habit(self.db, 4, "2021-11-02 05:04")
        tracking_habit(self.db, 4, "2021-11-03 05:21")
        tracking_habit(self.db, 4, "2021-11-04 11:41")
        tracking_habit(self.db, 4, "2021-11-05 05:02")
        tracking_habit(self.db, 4, "2021-11-06 12:21")
        tracking_habit(self.db, 4, "2021-11-07 16:56")
        tracking_habit(self.db, 4, "2021-11-08 05:21")
        tracking_habit(self.db, 4, "2021-11-12 13:34")
        tracking_habit(self.db, 4, "2021-11-13 06:03")
        tracking_habit(self.db, 4, "2021-11-17 07:21")
        tracking_habit(self.db, 4, "2021-11-21 21:45")
        tracking_habit(self.db, 5, "2021-11-02 06:21")
        tracking_habit(self.db, 5, "2021-11-03 19:28")
        tracking_habit(self.db, 5, "2021-11-04 11:42")
        tracking_habit(self.db, 5, "2021-11-05 19:41")
        tracking_habit(self.db, 5, "2021-11-06 12:21")
        tracking_habit(self.db, 5, "2021-11-08 11:31")
        tracking_habit(self.db, 5, "2021-11-09 07:21")
        tracking_habit(self.db, 5, "2021-11-10 07:32")
        tracking_habit(self.db, 5, "2021-11-11 19:45")
        tracking_habit(self.db, 5, "2021-11-12 17:34")
        tracking_habit(self.db, 5, "2021-11-13 06:57")
        tracking_habit(self.db, 5, "2021-11-14 09:09")
        tracking_habit(self.db, 5, "2021-11-15 15:32")
        tracking_habit(self.db, 5, "2021-11-16 13:21")
        tracking_habit(self.db, 5, "2021-11-17 08:21")
        tracking_habit(self.db, 5, "2021-11-18 08:22")
        tracking_habit(self.db, 5, "2021-11-19 08:34")
        tracking_habit(self.db, 5, "2021-11-20 12:01")
        tracking_habit(self.db, 5, "2021-11-25 09:21")
        tracking_habit(self.db, 5, "2021-11-26 08:23")
        tracking_habit(self.db, 5, "2021-11-27 07:35")
        tracking_habit(self.db, 5, "2021-11-30 08:21")
        tracking_habit(self.db, 4, "2021-11-22 08:45")
        tracking_habit(self.db, 4, "2021-11-23 09:00")
        tracking_habit(self.db, 4, "2021-11-28 21:00")

# Testing of analysis module
    def test_analysis(self):
        # Testing "List of all currently tracked habits"
        data = all_habits(self.db)
        assert len(data) == 5

        # Testing "List of all habits with the same periodicity"
        periodicity = 'daily'
        data = all_habits_periodicity(self.db, periodicity)
        assert len(data) == 2
        periodicity = 'weekly'
        data = all_habits_periodicity(self.db, periodicity)
        assert len(data) == 3

        # Testing "Longest run streak of all defined habits"
        data = max_streak(self.db)
        assert int(data['streak_cum_count']) == 13

        # Testing "Longest run streak for a given habit"
        name = 'Waking up'
        data = max_streak_habit(self.db, name)
        assert int(data['streak_cum_count']) == 7
        name = 'Studying'
        data = max_streak_habit(self.db, name)
        assert int(data['streak_cum_count']) == 4

    def test_habit(self):
        # Testing of habit storage
        habit = Habit("Do meditation", "At least 30 minutes each day", "daily")
        habit.store_habit(self.db)

        # Testing of habit modification (task only)
        habit = Habit("Do meditation", "At least 15 minutes", "daily")
        habit.modify_habit_task(self.db)
        assert habit.task == "At least 15 minutes"

        # Testing of habit modification (periodicity only)
        habit = Habit("Do meditation", "At least 15 minutes", "weekly")
        habit.modify_habit_periodicity(self.db)
        assert habit.periodicity == "weekly"

        # Testing of habit modification (task + periodicity)
        habit = Habit("Do meditation", "At least 10 minutes", "daily")
        habit.modify_habit(self.db)
        assert habit.task == "At least 10 minutes"
        assert habit.periodicity == "daily"

        # Testing of habit checkoff
        habit.check_off_habit(self.db, "Do meditation", datetime.datetime.today())
        habit.check_off_habit(self.db, "Do meditation", "2022-02-01 00:00")
        habit_name_id = int("".join(str(x) for x in (list(map(lambda x: x[0], (filter(lambda y: y[1] == 'Do meditation',
                                                                                      get_habit_data(self.db))))))))
        tracking_list = list(filter(lambda x: x[0] == habit_name_id, get_tracking_data(self.db)))
        assert len(tracking_list) == 2

        # Testing of individual habit deletion including habit and tracking data
        data = get_habit_data(self.db)
        assert len(data) == 6
        habit = Habit("Studying", "null", "null")
        habit_name_id = int("".join(str(x) for x in (list(map(lambda x: x[0], (filter(lambda y: y[1] == 'Studying',
                                                                                      get_habit_data(self.db))))))))
        habit.delete_tracking_data(self.db)
        habit.delete_habit_data(self.db)
        data = get_habit_data(self.db)
        assert len(data) == 5
        tracking_list = list(filter(lambda x: x[0] == habit_name_id, get_tracking_data(self.db)))
        assert len(tracking_list) == 0

        # Testing of complete habit deletion including habit and tracking data
        delete_all_habit_tracking_data(self.db)
        data = get_habit_data(self.db)
        assert len(data) == 0
        tracking = get_tracking_data(self.db)
        assert len(tracking) == 0

    # Teardown method to delete the testing database after each test
    def teardown_method(self):
        import os
        os.remove("test.db")

"""
This file implements the habit class and defines all functions for storing, modifying, deleting and checking off
instances of the habit class.

itertools is imported to create an auto-incremented habit_id column due to database integrity reasons.
datetime is needed for storing auto-creation and auto-update dates.
For storing, updating, deleting and checking off habits, a connection to the database has to be established and thus
the database file imported.
"""

import itertools
import datetime
import database


class Habit:

    new_id = itertools.count()

    # Initialization of the habit class
    def __init__(self, name: str, task: str, periodicity: str):

        """
        This function initializes the habit class.

        :param name: name of the habit
        :param task: task of the habit
        :param periodicity: periodicity (daily or weekly)
        """
        self.habit_id = next(self.new_id)+1  # set a unique id for each habit; add 1 to let id start at 1 instead of 0
        self.name = name
        self.task = task
        self.periodicity = periodicity
        self.creation_date = datetime.date.today()
        self.update_date = datetime.date.today()

    # Function for storing a new habit
    def store_habit(self, db):

        """
        This function refers to the database functions and adds any new habit instance to the habit table.

        :param db: initialized sqlite3 database connection
        """

        database.create_table_habit(db)
        database.add_habit_data(db, self.name, self.task, self.periodicity)

    # Function for updating a habit's task
    def modify_habit_task(self, db):

        """
        This function refers to the database function of updating an existing habit's task

        :param db: initialized sqlite3 database connection
        """

        database.update_habit_task(db, self.task, self.name)

    # Function for updating a habit's periodicity
    def modify_habit_periodicity(self, db):

        """
        This function refers to the database function of updating an existing habit's periodicity

        :param db: initialized sqlite3 database connection
        """

        database.update_habit_periodicity(db, self.periodicity, self.name)

    # Function for updating a habit's task and periodicity
    def modify_habit(self, db):

        """
        This function refers to the database function of updating an existing habit's task and periodicity

        :param db: initialized sqlite3 database connection
        """

        database.update_habit(db, self.task, self.periodicity, self.name)

    # Function for deleting a habit's tracking data
    def delete_tracking_data(self, db):

        """
        This function refers to the database function of deleting a habit's tracking/check-off data

        :param db: initialized sqlite3 database connection
        """

        database.delete_tracking_data(db, self.name)

    # Function for deleting a habit
    def delete_habit_data(self, db):

        """
        This function refers to the database function of deleting a habit from the main habit table

        :param db: initialized sqlite3 database connection
        """

        database.delete_habit_data(db, self.name)

    # Function for checking-off an existing habit
    @staticmethod
    def check_off_habit(db, name, date):

        """
        This function refers to the database function of adding a date to the tracking table

        :param db: initialized sqlite3 database connection
        :param name: name of the habit
        :param date: check-off date
        """

        habit_tracker_id = int("".join(str(x) for x in
                                       (list(map(lambda x: x[0],
                                                 (filter(lambda y: y[1] == name, database.get_habit_data(db))))))))
        database.create_table_tracking(db)
        database.tracking_habit(db, habit_tracker_id, date)

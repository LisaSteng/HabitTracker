"""
This file includes all functions related to the storage, modification, deletion and extraction of data in the database.
For this purpose, sqlite3 is imported as a database engine.
The imported datetime module is used for the automatic storage of creation, update and check-off dates.
"""

import sqlite3
import datetime


# Connecting to the database
def get_db(name="main.db"):

    """
    This function is used establish a connection to the database.

    :param name: name of the database

    :return: database
    """

    db = sqlite3.connect(name)
    return db


# Creating the main habit table
def create_table_habit(db):

    """
    This function is used to create the habit table in which the id, name, task, periodicity as well as creation and
    update date of each habit is stored.

    :param db: initialized sqlite3 database connection
    """

    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habit(
        habit_id INTEGER PRIMARY KEY,
        name TEXT,
        task TEXT,
        periodicity TEXT,
        creation_date DATETIME,
        update_date DATETIME)""")
    db.commit()


# Creating the tracking table
def create_table_tracking(db):

    """
        This function is used to create the habit tracking table in which each checkoff date including the tracking id
        and respective habit id is stored. The habit id is a foreign key referencing the primary key of the habit table.

        :param db: initialized sqlite3 database connection
        """

    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS tracking(
        tracking_id INTEGER PRIMARY KEY,
        habit_tracker_id INTEGER,
        checkoff_date DATETIME,
        FOREIGN KEY(habit_tracker_id) REFERENCES habit(habit_id))""")
    db.commit()


# Function for storing a new habit
def add_habit_data(db, name, task, periodicity):

    """
    This function stores any new habit in the table "habit".

    :param db: initialized sqlite3 database connection
    :param name: name of the habit
    :param task: task specification of the habit
    :param periodicity: periodicity (daily or weekly)
    """

    cur = db.cursor()
    date_time = datetime.datetime.today()
    cur.execute("INSERT INTO habit VALUES(null,?,?,?,?,?)", (name, task, periodicity, date_time, date_time))
    db.commit()


# Function for checking-off an existing habit
def tracking_habit(db, habit_tracker_id: int, date_tracking: datetime):

    """
    This function stores any new check-off date in the table "tracking".

    :param db: initialized sqlite3 database connection
    :param habit_tracker_id: habit_id as a foreign key referencing the primary key "habit_id" of the habit table
    :param date_tracking: check-off date when the user has completed the habit which can either be the current datetime
    or a manually entered datetime in the past
    """

    cur = db.cursor()
    cur.execute("INSERT INTO tracking VALUES (null, ?, ?)", (int(habit_tracker_id), date_tracking))
    db.commit()


# Functions for updating habits
def update_habit_task(db, task, name):

    """
    This function is used for updating the task of a selected habit in the database. The datetime of modification will
    be stored in the column "update_date".

    :param db: initialized sqlite3 database connection
    :param task: updated task specification
    :param name: name of the habit for which the task specification should be modified
    """
    cur = db.cursor()
    date_update = datetime.datetime.today()
    cur.execute("UPDATE habit SET task = ? WHERE name = ?", (task, name))
    cur.execute("UPDATE habit SET update_date = ? WHERE name = ?", (date_update, name))
    db.commit()


def update_habit_periodicity(db, periodicity, name):

    """
    This function is used for updating the periodicity of a selected habit in the database. The datetime of modification
    will be stored in the column "update_date".

    :param db: initialized sqlite3 database connection
    :param periodicity: updated periodicity in terms of daily or weekly
    :param name: name of the habit for which the periodicity should be modified
    """

    cur = db.cursor()
    date_update = datetime.datetime.today()
    cur.execute("UPDATE habit SET periodicity = ? WHERE name = ?", (periodicity, name))
    cur.execute("UPDATE habit SET update_date = ? WHERE name = ?", (date_update, name))
    db.commit()


def update_habit(db, task, periodicity, name):

    """
    This function is used for updating the task and periodicity of a selected habit in the database. The datetime of
    modification will be stored in the column "update_date".

    :param db: initialized sqlite3 database connection
    :param task: updated task specification
    :param periodicity: updated periodicity in terms of daily or weekly
    :param name: name of the habit for which the task and periodicity should be modified
    """

    cur = db.cursor()
    date_update = datetime.datetime.today()
    cur.execute("UPDATE habit SET task = ?, periodicity = ? WHERE name = ?", (task, periodicity, name))
    cur.execute("UPDATE habit SET update_date = ? WHERE name = ?", (date_update, name))
    db.commit()


# Functions for deleting habits
def delete_habit_data(db, name):

    """
    This function deletes a selected habit from the table "habit"

    :param db: initialized sqlite3 database connection
    :param name: name of the habit which should be deleted
    """

    cur = db.cursor()
    cur.execute("DELETE FROM habit WHERE name=?", (name,))
    db.commit()


def delete_tracking_data(db, name):

    """
    This function deletes all check off dates and related data from the table "tracking" for a selected habit

    :param db: initialized sqlite3 database connection
    :param name: name of the habit for which the tracking data should be deleted
    """

    cur = db.cursor()
    habit_tracking_id = str(cur.execute("SELECT DISTINCT habit_id FROM habit WHERE name = ?", (name,)))
    habit_tracking_id = cur.fetchone()[0]
    cur.execute("DELETE FROM tracking WHERE habit_tracker_id=?", (habit_tracking_id,))
    db.commit()


def delete_all_habit_tracking_data(db):

    """
    This function deletes all data from the habit as well as tracking table.

    :param db: initialized sqlite3 database connection
    """

    cur = db.cursor()
    cur.execute("DELETE FROM tracking")
    cur.execute("DELETE FROM habit")
    db.commit()


# Functions for the analysis module
def get_habit_data(db):

    """
    This function selects all data entries from the table "habit" as a basis for the analysis modules.

    :param db: initialized sqlite3 database connection
    """

    cur = db.cursor()
    cur.execute("SELECT habit_id, name, task, periodicity, STRFTIME('%Y-%m-%d %H:%M', creation_date), "
                "STRFTIME('%Y-%m-%d %H:%M',update_date) FROM habit")
    return cur.fetchall()


def get_tracking_data(db):
    """
    This function selects all data entries from the table "tracking" as a basis for the analysis modules.

    :param db: initialized sqlite3 database connection
    """

    cur = db.cursor()
    cur.execute("SELECT habit_tracker_id AS habit_id, STRFTIME('%Y-%m-%d', checkoff_date) FROM tracking")
    return cur.fetchall()

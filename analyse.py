"""
This file includes all functions for the analysis module, i.e.:
(1) A list of all currently tracked habits,
(2) A list of all habits with the same periodicity,
(3) The longest run streak of all defined habits,
(4) The longest run streak for a given habit

The database file is imported in order to refer back to the sqlite SELECT statements for the habit and tracking data.
Pandas and NumPy are imported as a basis for manipulating the data and performing the respective analysis functions.
"""

import database
import pandas as pd
import numpy as np


# Function to return a list of all currently tracked habits
def all_habits(db):

    """
     Shows all habits stored in the database.

     :param db: initialized sqlite3 database connection

     :return: List of all habits showing the name, task/specification, periodicity, creation datetime and last update
     datetime of each habit.
     """

    data_all = database.get_habit_data(db)
    return data_all


# Function to return a list of all habits with the same periodicity
def all_habits_periodicity(db, periodicity):

    """
    Shows all habits stored in the database with the selected periodicity.

    :param db: initialized sqlite3 database connection
    :param periodicity: periodicity ("weekly" or "daily") for which a list of available habits should be displayed

    :return: List of all habits with the selected periodicity showing the name, task/specification, periodicity,
     creation datetime and last update datetime of each habit. If no habits are stored with the selected periodicity,
    the message "There are currently no habits stored with periodicity x".
    """

    data_all = database.get_habit_data(db)
    data_filtered = list(filter(lambda x: x[3] == periodicity, data_all))
    df = pd.DataFrame(data_filtered)
    return df


# Support functions and function to return the longest run streak of all defined habits
def daily_streak_count(db):

    """
    This function is a support function for defining the longest run streak of all defined habits by
    (1) creating a sorted list of all unique combinations of daily habits and respective check-off dates and
    (2) calculating the difference in days between two subsequent check-off events so that
    (3) a cumulated streak count can be calculated for the period where the difference between two subsequent dates
    is equal to 1

    :param db: initialized sqlite3 database connection

    :return: List of daily habits and check-off date history with the cumulated streak count. If no tracking data is
    available for a daily habit, "No data" is returned to be respectively considered in the subsequent function to
    avoid any unintended program errors and/or exit.
    """

    data_tracking = pd.DataFrame(database.get_tracking_data(db))
    if len(data_tracking) == 0:
        return "No data"
    else:
        data_tracking.columns = ['habit_id', 'check_off_date']
        data_habits = pd.DataFrame(database.get_habit_data(db))
        data_habits.columns = ['habit_id', 'name', 'task', 'periodicity', 'creation_date', 'update_date']
        data_all = pd.merge(data_tracking, data_habits[['habit_id', 'name', 'periodicity']], how="left",
                            left_on='habit_id', right_on='habit_id')
        tracking_daily = (data_all[data_all['periodicity'] == 'daily']).sort_values(by=['name', 'check_off_date'])
        if len(tracking_daily) == 0:
            return "No data"
        else:
            df = tracking_daily
            df.drop_duplicates(subset=['name', 'check_off_date'], inplace=True)
            df['check_off_date'] = df[['check_off_date']].apply(pd.to_datetime)
            for _ in df.itertuples():
                df['day_diff'] = df['check_off_date'].diff()
                x = df.day_diff.ne('1 days')
                df['streak_helper'] = df[~x].groupby(x.cumsum()).cumcount().add(1)
                mask = (df['name'] != df.shift()['name']) | (df['day_diff'] != '1 days')
                v1 = 1
                v2 = df['streak_helper']+1
                df['streak_cum_count'] = np.where(mask, v1, v2)
            return df


def weekly_streak_count(db):

    """
    This function is having the same purpose as the function "daily_streak_count" but is focusing on the weekly
    habits, i.e. it
    (1) creates a sorted list of all unique combinations of weekly habits and respective check-off weeks and
    (2) calculates the difference between two subsequent check-off weeks so that
    (3) a cumulated streak count can be calculated for the period where the difference between two subsequent weeks
    is equal to 1

    :param db: initialized sqlite3 database connection

    :return: List of weekly habits and check-off week history with the cumulated streak count. If no tracking data is
    available for a weekly habit, "No data" is returned to be respectively considered in the subsequent function to
    avoid any unintended program errors and/or exit.
    """

    data_tracking = pd.DataFrame(database.get_tracking_data(db))
    if len(data_tracking) == 0:
        return "No data"
    else:
        data_tracking.columns = ['habit_id', 'check_off_date']
        data_habits = pd.DataFrame(database.get_habit_data(db))
        data_habits.columns = ['habit_id', 'name', 'task', 'periodicity', 'creation_date', 'update_date']
        data_all = pd.merge(data_tracking, data_habits[['habit_id', 'name', 'periodicity']], how="left",
                            left_on='habit_id', right_on='habit_id')
        tracking_weekly = (data_all[data_all['periodicity'] == 'weekly']).sort_values(by=['name', 'check_off_date'])
        if len(tracking_weekly) == 0:
            return "No data"
        else:
            df = tracking_weekly
            df['check_off_date'] = df[['check_off_date']].apply(pd.to_datetime)
            df['check_off_week'] = df['check_off_date'].dt.isocalendar().week
            df.drop_duplicates(subset=['name', 'check_off_week'], inplace=True)
            for _ in df.itertuples():
                mask_1 = (df['check_off_week'] == 1) & (df.shift()['check_off_week'] == 52)
                v1_1 = 1
                v2_1 = df['check_off_week'].diff()
                df['week_diff'] = np.where(mask_1, v1_1, v2_1)
                x = df.week_diff.ne(1)
                df['streak_helper'] = df[~x].groupby(x.cumsum()).cumcount().add(1)
                mask_2 = (df['name'] != df.shift()['name']) | (df['week_diff'] != 1)
                v1_2 = 1
                v2_2 = df['streak_helper']+1
                df['streak_cum_count'] = np.where(mask_2, v1_2, v2_2)
            return df


def max_daily_streak(db):

    """
    This function is the second-layer support function for identifying the habit(s) with the maximum run streak over
    all habits based on the output of the "daily_streak_count" function. As the same habit could appear several times
    with the same longest run streak in cases where the max run streak has been achieved multiple times, the function
    removes duplicates in the table.

    :param db: initialized sqlite3 database connection

    :return: Daily habit with the longest run streak. If more than one habit has the same maximum run streak, all
    respective habits are displayed. Based on the "daily_streak_count" function, "No data" is carried along to be
    respectively considered in the subsequent function to avoid any unintended program errors and/or exit.
    """

    data_all = daily_streak_count(db)
    if str(data_all) == "No data":
        return "No data"
    else:
        df = pd.DataFrame(data_all)
        data_max = df['streak_cum_count'].max()
        df = df.loc[df['streak_cum_count'] == data_max]
        df.drop(columns=['habit_id', 'check_off_date', 'day_diff', 'streak_helper'], inplace=True)
        df.drop_duplicates(inplace=True)
        return df


def max_weekly_streak(db):

    """
    This function is having the same purpose and functionality as the function "max_daily_streak" but related to the
    weekly habits.

    :param db: initialized sqlite3 database connection

    :return: Weekly habit with the longest run streak. If more than one habit has the same maximum run streak, all
    respective habits are displayed. Based on the "weekly_streak_count" function, "No data" is carried along to be
    respectively considered in the subsequent function to avoid any unintended program errors and/or exit.
    """

    data_all = weekly_streak_count(db)
    if str(data_all) == "No data":
        return "No data"
    else:
        df = pd.DataFrame(data_all)
        data_max = df['streak_cum_count'].max()
        df = df.loc[df['streak_cum_count'] == data_max]
        df.drop(columns=['habit_id', 'check_off_date', 'week_diff', 'check_off_week', 'streak_helper'], inplace=True)
        df.drop_duplicates(inplace=True)
        return df


def max_streak(db):

    """
    Identifies the habit(s) with the maximum run streak over all habits and irrespective of their periodicity.

    :param db: initialized sqlite3 database connection

    :return: Habit and its periodicity with the longest run streak. If more than one habit has the same maximum run
    streak, all respective habits are displayed. If there is no tracking data for neither the daily nor the weekly
    habits, the message "There is currently no tracking data available" is printed out.
    """

    df1 = max_daily_streak(db)
    df2 = max_weekly_streak(db)
    if (str(df1) == "No data") & (str(df2) == "No data"):
        return "There is currently no tracking data available"
    elif (str(df1) == "No data") & (str(df2) != "No data"):
        df = pd.DataFrame(df2)
        max_streak_count = df['streak_cum_count'].max()
        df = df.loc[df['streak_cum_count'] == max_streak_count]
        return df
    elif (str(df1) != "No data") & (str(df2) == "No data"):
        df = pd.DataFrame(df1)
        max_streak_count = df['streak_cum_count'].max()
        df = df.loc[df['streak_cum_count'] == max_streak_count]
        return df
    elif (str(df1) != "No data") & (str(df2) != "No data"):
        frames = [df1, df2]
        df = pd.concat(frames)
        max_streak_count = df['streak_cum_count'].max()
        df = df.loc[df['streak_cum_count'] == max_streak_count]
        return df


# Function to return the longest run streak of a habit
def max_streak_habit(db, name):

    """
    Identifies the maximum run streak of the selected habit.

    :param db: initialized sqlite3 database connection
    :param name: name of the habit for which the maximum run streak should be displayed

    :return: Selected habit and its periodicity with the longest run streak. If there is no tracking data available
    for the selected habit, the message "There is no tracking data available for the habit x" is printed out.
    """

    habit_name_id = int("".join(str(x) for x in
                                list(map(lambda x: x[0],
                                         (filter(lambda y: y[1] == name, database.get_habit_data(db)))))))
    list_tracking_ids = list(map(lambda x: x[0], database.get_tracking_data(db)))
    if habit_name_id not in list_tracking_ids:
        return f"There is no tracking data available for the habit {name}"
    else:
        data_all = database.get_habit_data(db)
        data_filtered = list(filter(lambda x: x[1] == name, data_all))
        if 'daily' in str(data_filtered):
            df = pd.DataFrame(daily_streak_count(db))
            df = df.loc[df['name'] == name]
            df.drop(columns=['habit_id', 'check_off_date', 'day_diff', 'streak_helper'], inplace=True)
            max_streak_count = df['streak_cum_count'].max()
            df = df.loc[df['streak_cum_count'] == max_streak_count]
            return df
        else:
            df = pd.DataFrame(weekly_streak_count(db))
            df = df.loc[df['name'] == name]
            df.drop(columns=['habit_id', 'check_off_date', 'check_off_week', 'week_diff', 'streak_helper'],
                    inplace=True)
            max_streak_count = df['streak_cum_count'].max()
            df = df.loc[df['streak_cum_count'] == max_streak_count]
            return df

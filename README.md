# Habit Tracker

*Habit Tracker* represents the backend for a basic habit 
tracking app following the main intention to support
users in keeping track of certain habits and achieving 
personal goals.

A *habit* is defined as a practice in daily life which 
one should/wants to adhere to in a regular frequency.

This project has been created using Python 3.7.

## Table of Contents

1. [Scope and Functionality](#Scope-and-Functionality)
2. [Prerequisites](#Prerequisites)
3. [Running the Program](#Running-the-Program)
4. [Testing the Project](#Testing-the-Project)

## Scope and Functionality

The app includes the options of
1. creating,
2. checking-off
3. modifying, 
4. deleting and
5. analysing habits.

An intuitive main menu is provided which gives more detailed questions and/or
choices within the individual options. 

At least one habit needs to be created 
before unlocking the options of modifying, deleting, checking-off and analysing 
habits.

From an interaction perspective, each user action is 
confirmed in case of success or respectively commented in
case of non-compliance with relevant validity rules.

### (1) Creating a Habit
When creating a habit, either a habit from a list of five predefined habits can be selected or a new habit can be entered. 

When creating a new habit, a respective task specification needs to be specified as well as a periodicity selected. 
From a periodicity perspective, *daily and weekly* habits are currently in the scope of 
the Habit Tracker.

In order to avoid the storage of duplicated habits, each habit name is only allowed to be stored once.

### (2) Checking-off a Habit
A task can be completed, i.e. *checked-off* by a user at any
point in time. 

After having selected a habit to be checked-off from the list of created habits, the user can either check-off the
habit with the *current datetime* or a *specific datetime*. While *current datetime* does not require any further
user input, *specific datetime* requires the user to enter a valid date (YYYY-MM-DD hh:mm) which is not allowed to be 
in the future.

Each task should be checked-off at least once
during the period the user defined. 

If a user misses completing a habit during the specified 
period, the user is said to *break the habit*.

If a user manages to complete the task of a habit x 
consecutive periods in a row, the user is said to have 
established a *streak of x periods*.

### (3) Modifying a Habit
For modifying a habit, a habit first needs to be selected from the list of all created habits.

If tracking (=check-off) data is available for the selected habit, the user can select whether the existing tracking data
should be kept or deleted.

The user can either modify only the task, only the periodicity or both for the selected habit.
As in case of habit creation, the task specification can be entered in the form of a free-text field whereas the 
periodicity (daily or weekly) has to be selected. 

### (4) Deleting a Habit
The user can either delete one selected habit or all habits at once. If all habits have been selected to be deleted, the
user needs to confirm deletion before final execution. 

Deleting one or all habits results in a deletion 
of the general habit data as well as the respective tracking data.

### (5) Analysing Habits
Within the current scope, there are four options of analysis:
1. List of all currently tracked habits
2. List of all habits with the same periodicity
3. Longest run streak of all defined habits
4. Longest run streak for a given habit

Upon selection of the respective option and - if needed - further details, a table with the results is shown. 

The following information should be taken into consideration
for a correct interpretation of the analysis results:
- First day of a week is Monday
- The *datetime* of habit creation, update and check-off is tracked
but, in the current scope, streak calculations are based on
*dates* only
  - For streak calculations of a daily habit, the habit needs
  to be checked-off at least once per day (the time is not
  relevant)
  - For streak calculations of a weekly habit, the habit needs
  to be checked-off at least once per week, i.e. checking-off
  a habit on Monday in week 1 and on Sunday in week 2 is equally
  resulting in a two-week-streak as it would be the case for
  checking-off a habit on Sunday in week 1 and on Monday in week 2
- Independent of daily or weekly habits, the streak counting always starts with the first check-off date and not with the
habit creation date

## Prerequisites

For running the program, Python 3.7 or higher must be installed.

Install all further requirements for the habit tracker app 
backend by typing the following code into your console:

```shell
pip install - r requirements.txt
```

## Running the Program

Type:

```shell
python main.py
```

into your console and navigate through the menu options and 
subsequent questions/choices on the screen.

## Testing the Project

For testing the project, enter into the console:
```shell
pytest .
```
All the described main functionalities are covered within the test suite 
and should return a green-coloured test confirmation message.

# Swiss
Udacity Swiss Pairings tournament project

#Overview
Files:
1. *tournament.sql*: A database schema for the tournament application. 
2. *tournament.py*: A python module to register, delete, and count players, report and delete matches, rank players, and create next swiss pairings.
3. *tournament_test.py*: functional tests to verify correctness 

#Requirements
PostgreSQL, Python 2.7 

#Installation

#1. Setup database
Type the following command in terminal to setup the database schema:
(Which will delete the exist "tournament" database)

>  > _psql -f tournament.sql_

#2. Run the test for checking
Type the following command in terminal
>  > _python tournament _ test.py_

if all tests pass, there will be a confirmation

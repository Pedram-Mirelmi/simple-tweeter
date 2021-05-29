# simple tweeter

## client:
The client UI version now has these features:
* write new tweet 
* like tweets
* view comments
* leave new comments
* like others comments
* user profile tab (managing user's own tweets)


## UI:
Recently i've added a UI written by PyQT5.<br />
I built my own widgets using inheritance in OOP. which all are in the client/UIPackages/Widgets <br />
The main window contains a tab environment. 
* home tab(all tweets)
* search tab(to search and visit others profile) which is still incomplete
* profile tab(user's own profile)

## server:
The comunication between client and server is based on socket programming and json.<br /> 
Also i used threading so it can talk to multiple clients at the same time and if one of them crashes servers stays running. <br /> 

## database:
The database uses MYSQL DBMS and server connects to the database using sql-connector <br /> 
The commands related to database creation is in the "database sources/" directory

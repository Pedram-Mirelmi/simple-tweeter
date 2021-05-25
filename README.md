# simple tweeter

## client:
The client terminal version has these features:
* writing new tweet 
* like tweets
* leave comments
## UI
Recently i've added a UI written by PyQT5, which the comment feature doesn't work yet. but the UI design has it.<br />
I built my own widgets using inheritance in OOP. which all are in the client/UIPackages/Widgets

## server
The comunication between client and server is based on socket programming and json.<br /> 
Also i used threading so it can talk to multiple clients at the same time and if one of them crashes servers stays running. <br /> 

## database
The database uses MYSQL DBMS and server connects to the database using sql-connector <br /> 
The commands related to database creation is in the "database sources/" directory

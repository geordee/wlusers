# WebLogic User Management

## Introduction
This script provides an easy interface to manage users in a WebLogic domain.
The script processes a list of groups, users and memberships are maintained in
an Excel workbook in a  pre-defined format.

## Workbook Format
The Excel workbook should have three worksheets as given below:

* groups
* users
* memberships

Excel worksheet names are case-insensitive.

Each of the sheet contains an operation and necessary information for the
entity or association. Operation can be one of "add", "chg" or "del".

The format required for each sheet is given below.

### groups
Operation |Group       |Group Description
----------|------------|------------------
add       |SuperHeroes |Super Heroes

### users
Operation |User      |User Name    |Password
----------|----------|-------------|----------
add       |batman    |Bruce Wayne  |b4tm4n88
chg       |superman  |Clark Kent   |5uperm4n
chg       |spiderman |Peter Parker |5p1derm4n

### memberships
Operation |Group       |User
----------|------------|----------
add       |SuperHeroes |batman
add       |SuperHeroes |spiderman
add       |SuperHeroes |superman

## Installation
This script is written in Python which gets processed by WLST's Jython
interpreter. Reading from Excel workbook is implemented using Apache POI
due to the current Jython version (2.2) distributed along with WebLogic.
Openpyxl could have been an alternative, which is a pure Python library, but
it requires Python 2.6+.

Download Apache POI and copy the following classes to the classpath.

* dom4j-x.x.x.jar
* poi-x.x-xxxxxxxx.jar
* poi-ooxml-x.x-xxxxxxxx.jar
* poi-ooxml-schemas-x.x-xxxxxxxx.jar
* stax-api-x.x.x.jar
* xmlbeans-x.x.x.jar

Alternatively, copy the files into a directory and add that to classpath. For
example, if the jar files are copied into classes subdirectory:

In UNIX
export CLASSPATH=$CLASSPATH:/home/geordee/code/wlusers/classes/*

In Windows
set CLASSPATH=%CLASSPATH%;D:\Code\WLUsers\classes\*

## Configuration
The scripts prompts for administrator username, password and the Excel Workbook
name. The only probable change that is required is the connect string, which
is currently hardcoded to t3://localhost:7001.

## Running the Script
The script is invoked using wlst.sh or wlst.cmd script found in
$ORACLE_FMW/wlserver_10.3/common/bin directory, where ORACLE_FMW is the
installation directory for Oracle Fusion Middleware.

$ORACLE_FMW/wlserver_10.3/common/bin/wlst.sh wlusers.py

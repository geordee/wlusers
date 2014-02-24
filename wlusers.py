# Manage OBIEE Users
"""
    wlusers.py
    ----------------------------------------------------------------------------

    Manage Weblogic Users using Microsoft Excel workbook

    :copyright: (c) 2014 by Geordee Naliyath
"""

# $ORACLE_FMW/wlserver_10.3/common/bin/wlst.sh wlusers.py

from java.io import FileInputStream
from weblogic.management.utils import AlreadyExistsException, NotFoundException, InvalidParameterException
from org.apache.poi.xssf.usermodel import *

def print_title(title):
    print title
    print '--------------------------------------------------------------------------------'

print_title('Manage Weblogic Security')

username = raw_input('Enter administrator username: ')
password = raw_input('Enter administrator password: ')

userbook = raw_input('Enter path for user workbook: ')

try:
    fis = FileInputStream(userbook)
except java.io.FileNotFoundException:
    print '*** ERROR *** File not found : %s' % (userbook)
    exit()
except:
    print '*** ERROR *** An error occured in opening the file %s' % (userbook)
    exit()

wb = XSSFWorkbook(fis)

try:
    connect(username, password, 't3://localhost:7001')
except:
    print '*** ERROR *** Error occured while performing connect'
    exit()

serverConfig()
atnr=cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider('DefaultAuthenticator')

print_title('Processing Groups...')

ws = wb.getSheet('groups')
rows = ws.getPhysicalNumberOfRows()
# todo: handle exceptions
for r in range(1, rows, 1):
    row = ws.getRow(r)
    if(row != None):
        oper  = str(row.getCell(0))
        group = str(row.getCell(1))
        desc  = str(row.getCell(2))

    if group.strip() == '': continue

    if oper.lower() == 'add':
        if not atnr.groupExists(group):
            try:
                atnr.createGroup(group, desc)
            except:
                print '*** ERROR *** Could not create group %s' % (group)
    elif oper.lower() == 'chg':
        if atnr.groupExists(group):
            try:
                atnr.setGroupDescription(group, desc)
            except:
                print '*** ERROR *** Could not change group %s' % (group)
    elif oper.lower() == 'del':
        if atnr.groupExists(group):
            try:
                atnr.removeGroup(group)
            except:
                print '*** ERROR *** Could not remove group %s' % (group)
    else:
        pass


print_title('Processing Users...')

ws = wb.getSheet('users')
rows = ws.getPhysicalNumberOfRows()
# todo: handle exceptions
for r in range(1, rows, 1):
    row = ws.getRow(r)
    if(row != None):
        oper  = str(row.getCell(0))
        user  = str(row.getCell(1))
        name  = str(row.getCell(2))
        pswd  = str(row.getCell(3))

    if user.strip() == '' or pswd.strip() == '': continue

    if oper.lower() == 'add':
        if not atnr.userExists(user):
            try:
                atnr.createUser(user, pswd, name)
            except InvalidParameterException:
                print '*** ERROR *** Invalid parameters for %s' % (user)
            except:
                print '*** ERROR *** Could not create user %s' % (user)
            try:
                atnr.setUserAttributeValue(user, 'displayname', name)
            except:
                print '*** ERROR *** Could not create user %s' % (user)
    elif oper.lower() == 'chg':
        if atnr.userExists(user):
            try:
                atnr.setUserDescription(user, name)
            except:
                print '*** ERROR *** Could not change description for %s' % (user)
            try:
                atnr.resetUserPassword(user, pswd)
            except InvalidParameterException:
                print '*** ERROR *** Invalid parameters for %s' % (user)
            except:
                print '*** ERROR *** Could not change password for %s' % (user)
            try:
                atnr.setUserAttributeValue(user, 'displayname', name)
            except:
                print '*** ERROR *** Could not create user %s' % (user)
    elif oper.lower() == 'del':
        if atnr.userExists(user):
            try:
                atnr.removeUser(user)
            except:
                print '*** ERROR *** Could not remove user %s' % (user)
    else:
        pass


print_title('Processing Memberships...')

ws = wb.getSheet('memberships')
rows = ws.getPhysicalNumberOfRows()
# todo: handle exceptions
for r in range(1, rows, 1):
    row = ws.getRow(r)
    if(row != None):
        oper  = str(row.getCell(0))
        group = str(row.getCell(1))
        user  = str(row.getCell(2))

    if group.strip() == '' or user.strip() == '': continue

    if oper.lower() == 'add':
        try:
            atnr.addMemberToGroup(group, user)
        except NotFoundException:
            print '*** WARN  *** Could not find group %s or user %s' % (group, user)
        except:
            print '*** ERROR *** Could not add user %s to %s' % (group, user)
    elif oper.lower() == 'del':
        try:
            atnr.removeMemberFromGroup(group, user)
        except NotFoundException:
            print '*** WARN  *** Could not find group %s or user %s' % (group, user)
        except:
            print '*** ERROR *** Could not remove user %s from %s' % (group, user)
    else:
        pass

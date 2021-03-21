# designed by github.com/csraea - All rights reserved. 2021. Korotetskyi(c)
import hashlib
import sys

f = None
name = ""
password = ""
key = ""

# get login info from console
def getLoginInfo():
    try:
        global name, password, key
        name = input("meno: ")
        password = input("heslo: ")
        key = input("kluc: ")
    except:
        print("chyba")
        sys.exit()
    if name == '\0' or password == '\0' or key == '\0' or name == '\n' or password == '\n' or key == '\n' or name == '' or password == '' or key == '':
        print("chyba")
        sys.exit()


# try to open the file & save the contents
def getFileContens(name):
    try:
        global f
        f = open(name, 'r+')
    except OSError:
        print("chyba")
        sys.exit()
    
    return f.read()


def verifyLoginCredentials(inputFile):
    # split hesla.csv in lines
    lines = inputFile.split('\n')

    # clear hesla.csv before editing
    global f
    f.seek(0)
    f.truncate(0)

    # flags for tracing the state of authenification
    flagN = False
    flagP = False
    flagK = False

    # analyze line literals
    for l in lines:
        literals = l.split(':')
        for lt in literals:
            # if name and password are correct check the keys
            if flagP and flagN:
                keys = lt.split(',')
                if keys == '':
                    break
                if key in keys:
                    keys.remove(key)
                    flagK = True
                    literals[literals.index(lt)] = ','.join(keys)
            # if user with such a name exists
            elif lt == name:
                flagN = True
                continue
            # check the password encryption
            elif flagN and hashlib.md5(password.encode('utf-8')).hexdigest() == lt:
                flagP = True
                continue

        if lines.index(l) == len(lines) - 1:
            print(':'.join(literals), file=f, end='')
        else:
            print(':'.join(literals), file=f, end='\n')

        flagN = False
        flagP = False
    
    # close the file
    f.close()

    return flagK
  

def main():
    getLoginInfo()
    inputFile = getFileContens("hesla.csv")
    if verifyLoginCredentials(inputFile):
        print("ok")
    else:
        print("chyba")
    sys.exit()



if __name__ == "__main__":
    main()

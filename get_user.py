import os
import pwd

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

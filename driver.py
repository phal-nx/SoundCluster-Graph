import getpass
from termcolor import colored
import utils.db as db



sc_username = input(colored("Soundcloud Username:", "blue"))
sc_pass = getpass.getpass(colored("Password:", "blue"))


db.put_followers_in_db(sc_username, sc_pass)

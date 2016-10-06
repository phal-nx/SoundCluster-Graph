import getpass
import utils.db as db
import utils.helpers as helpers
from termcolor import colored


if __name__ == "__main__":
    sc_username = input(colored("Soundcloud Username:", "blue"))
    sc_pass = getpass.getpass(colored("Password:", "blue"))

    client = helpers.get_client(sc_username, sc_pass)
    my_user = helpers.get_my_user(client)

    print("Welcome {}\n".format(colored(my_user.username, "green")))
    print("id: {}".format(my_user.id))
    # Add Hub User to DB as a hub
    db.add_user(my_user, hub_user=True)

    db.put_followers_in_db(client)
    helpers.get_and_draw_neo4j_graph()
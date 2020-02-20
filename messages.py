from models import User, Message
import argparse, sys

parser = argparse.ArgumentParser(description='Message manager.')

# Argumenty obowiązkowe - `required=True`
parser.add_argument('-u','--user', help='user name', required=True)
parser.add_argument('-p','--passwd', help='user password', required=True)
# Argumentu opcjonalne
parser.add_argument('-t','--to-user', help='send message to')
parser.add_argument('-m','--message', help='message')
parser.add_argument('-l','--list', help='show my message', action='store_true')
parser.add_argument('-d','--delete', help='delete message by given ID')

args = parser.parse_args()

# Sprawdzenie usera
user = User.load_by_username(args.user)
if not user:
    print('Nie znaleziono', args.user)
    sys.exit(1)
if not user.check_password(args.passwd):
    print('Błędne hasło')
    sys.exit(2)

################################################################################
if args.list: # Listowanie wiadomości
    for message in user.load_all_messages():
        user_from = User.load_by_id(message.from_id)
        if user_from:
            print("AT {} USER {} wrote:".format(message.creation_date, user_from.username))
            print(message.text)
            print(message.id)
            print()
        else:
            # if user_from got deleted
            print("AT {} USER anonymous wrote:".format(message.creation_date))
            print(message.text)
            print(message.id)
            print()
elif args.delete: # Usuwanie wiadomości
    mesg = Message.load_by_id(args.delete)
    if mesg:
        if mesg.to_id == user.id:
            mesg.delete()
        else:
            print('Nie możesz usunąć tej wiadomości!')
    else:
        print('Nie znaleziono wiadomości o podanym ID')
else: # Wysyłka wiadomości - zachowanie domyślne
    target_user = User.load_by_username(args.to_user)
    if target_user:
        mesg = Message()
        mesg.from_id = user.id 
        mesg.to_id = target_user.id
        mesg.text = args.message
        mesg.save_to_db()
from models import User
#####
# Arg parse odczytuje z cli
username = 'jo'
passwd = 'jo_pass'
message_text = 'jakis tekst'
message_to = 'jim'

## Creating User table
# User.create_storage()

## creating user Jo
# jo = User()
# jo.username = 'Jo'
# jo.password ='coderslab'
# jo.email = 'joe@gmail.com'
# jo.save()

# do = User()
# do.username = 'Dorothy'
# do.password ='coderslab'
# do.email = 'dor@gmail.com'
# do.save()

# ka = User()
# ka.username = 'Kacper'
# ka.password = 'qwerty'
# ka.email = 'kacper@wp.pl'
# ka.save()

## changing the user email by id:
# usr = User.load_by_id(3)
# usr.email = 'jo@gmail.com'
# usr.save()

## deleting user Jo:
# usr = User.load_by_username('Jo')
# usr.delete()

# user = User.load_by_username(username)

# if user.check_password(passwd):
    # for message in user.get_all_message():
    #     print(message)
    #
    # user_to = User.load_by_username(message_to)
    # mesg = Message()


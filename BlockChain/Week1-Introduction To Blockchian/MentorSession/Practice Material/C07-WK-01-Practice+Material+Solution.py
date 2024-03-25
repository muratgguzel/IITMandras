import hashlib

users = {} # A simple demo storage

def hash_password(password):
    hash_value = hashlib.sha256(password)
    return hash_value.hexdigest()

def save_user_details(username, password):
    hashed_pass = hash_password(password)
    users[username] = hashed_pass


def verify(username, newpassword):
    if username in users:
        new_pass = hash_password(newpassword)
        existing_pass = users[username]
        if existing_pass == new_pass:
            print('Both Username and Password match')
        else:
            print('Username matches But Password mismatch')
    else:
        print('Username mismatch')




if __name__ == "__main__":

    # Add a user
    username = 'Brent' # The users username
    password = b'password123' # The users password
    save_user_details(username, password)
    print("Stored user details")

    # Verification attempt 1 (incorrect username)
    print("Verifying username - ", end="")
    username = 'Breant'
    newpassword = b'password123'
    verify(username, newpassword)

    # Verification attempt 2 (incorrect password)
    print("Verifying password - ", end="")
    username = 'Brent'
    newpassword = b'notmypassword'
    verify(username, newpassword)


    # Verification attempt 3 (correct username and password)
    print("Verifying username and password - ", end="")
    username = 'Brent'
    newpassword = b'password123'
    verify(username, newpassword)

    print(users)
from hashlib import md5
import json

'''
Data format:
{
    username: [md5(username).hexdigest(), password],
    .
    .
    .
}
'''
users = {
    'HTBUser132' : [md5(b'HTBUser132').hexdigest(), 'secure123!'],
    'JohnMarcus' : [md5(b'JohnMarcus').hexdigest(), '0123456789']
}

def get_option():
    return input('''
    Welcome to my login application scaredy cat ! I am using MD5 to save the passwords in the database.
                          I am more than certain that this is secure.                       
                                   You can't prove me wrong!          
    
    [1] Login
    [2] Register
    [3] Exit

    Option (json format) :: ''')


def main():
    while True:
        option = json.loads(get_option())

        if 'option' not in option:
            print('[-] please, enter a valid option!')
            continue

        option = option['option']
        if option == 'login':
            creds = json.loads(input('enter credentials (json format) :: '))

            usr, pwd = creds['username'], creds['password']
            usr_hash = md5(usr.encode()).hexdigest()
            for db_user, v in users.items():
                if [usr_hash, pwd] == v:
                    if usr == db_user:
                        print(f'[+] welcome, {usr} 🤖!')
                    else:
                        print(f"[+] what?! this was unexpected. shutting down the system :: {open('flag.txt').read()} 👽")
                        exit()
                    break
            else:
                print('[-] invalid username and/or password!')
        
        elif option == 'register':
            creds = json.loads(input('enter credentials (json format) :: '))

            usr, pwd = creds['username'], creds['password']
            if usr.isalnum() and pwd.isalnum():
                usr_hash = md5(usr.encode()).hexdigest()
                if usr not in users.keys():
                    users[usr] = [md5(usr.encode()).hexdigest(), pwd]
                else:
                    print('[-] this user already exists!')
            else:
                print('[-] your credentials must contain only ascii letters and digits.')

        elif option == 'exit':
            print('byeee.')
            break


if __name__ == '__main__':
    main()
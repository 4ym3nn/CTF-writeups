```
$ python message.py 

    Welcome to my login application scaredy cat ! I am using MD5 to save the passwords in the database.
                          I am more than certain that this is secure.                       
                                   You can't prove me wrong!          
    
    [1] Login
    [2] Register
    [3] Exit

    Option (json format) :: {"option": "register"}
enter credentials (json format) :: {"username": "TEXTCOLLBYfGiJUETHQ4hAcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak", "password": "123"}

    Welcome to my login application scaredy cat ! I am using MD5 to save the passwords in the database.
                          I am more than certain that this is secure.                       
                                   You can't prove me wrong!          
    
    [1] Login
    [2] Register
    [3] Exit

    Option (json format) :: {"option": "login"}
enter credentials (json format) :: {"username": "TEXTCOLLBYfGiJUETHQ4hEcKSMd5zYpgqf1YRDhkmxHkhPWptrkoyz28wnI9V0aHeAuaKnak", "password": "123"}
Traceback (most recent call last):
  File "/Users/jb/Downloads/message.py", line 75, in <module>
    main()
  File "/Users/jb/Downloads/message.py", line 50, in main
    print(f"[+] what?! this was unexpected. shutting down the system :: {open('flag.txt').read()} 👽")
                                                                         ^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'flag.txt'
```
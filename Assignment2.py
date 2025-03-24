import sys
import os

class MiniBank:
    def __init__(self):
        self.text_file = 'users.txt'
        self.user_list = {}
        self.load_users()


    def load_users(self):
        '''Load user data from a text file into user_list.'''
        if not os.path.exists(self.text_file):
            open(self.text_file, 'x').close()
        with open(self.text_file, 'r') as file:
            for line in file.readlines():
                if line.strip() == '':
                    continue    # skip empty lines
                userID, userName, password, amount = line.strip().split(',')
                self.user_list[int(userID)] = {
                    'username' : userName,
                    'password' : password,
                    'amount' : int(amount)
                }

    def save_user(self):
        '''Save current user_list back to the text file.'''
        with open(self.text_file, 'w') as file:
            for userId, userdata in self.user_list.items():
                line = f"{userId},{userdata['username']},{userdata['password']},{userdata['amount']}\n"
                file.write(line)


    def first_option(self):
        while True:
            try:
                option: int = int(
                    input('\nPress 1 for Login,\nPress 2 for Register,\nPress 3 for Exit,\nChoose Option :'))
                if option == 1:
                    self.login()
                elif option == 2:
                    self.register()
                elif option == 3:
                    print('Thank You for Using Our Service.')
                    sys.exit()
                else:
                    print('Please Enter Valid Number. ( 1 , 2 or 3 )')
            except Exception as err:
                print(err)

    def login(self):
        print("\n#####    Account Login   #####")
        l_username: str = input("Enter Username :").strip()
        l_password: str = input("Enter Password :").strip()
        if self.l_name_pass_check(l_username, l_password):
            print(f"\n#####    Login Successfull   #####\n")
            self.second_option(l_username)
        else:
            print("Account not found.\nPlease Enter User Name and Password Carefully.")

    def second_option(self, l_username):
        while True:
            user: str = l_username
            print(f'\nWelcome {user}')
            print("1. Transfer\n2. Withdraw\n3. Update Information\n4. Account Info\n5. Logout\n6. Exit")
            try:
                option: int = int(input("Choose Option ( 1 - 6 ) :"))
                if option == 1:
                    self.transfer(user)
                elif option == 2:
                    self.withdraw(user)
                elif option == 3:
                    self.update_information(user)
                elif option == 4:
                    print(f"\nUserName : {self.user_list[self.return_id(user)]['username']}")
                    print(f"Balance : $ {self.user_list[self.return_id(user)]['amount']}")
                elif option == 5:
                    print("Logging out...\n")
                    self.first_option()
                elif option == 6:
                    print('Thank You for Using Our Service.')
                    sys.exit()
                else:
                    print('Please Enter Valid Number. ( 1 - 6 )')
            except Exception as err:
                print(err)

    def transfer(self, sender):
        sender_name: str = sender
        sender_id: int = self.return_id(sender_name)
        print("\n#####  Transfer    #####")
        receiver: str = input("Enter User Name to Transfer :").strip()
        if sender_name == receiver:
            print('\nYou Cannot Transfer to Yourself\n')
        else:
            if self.r_name_check(receiver):
                sure: str = input(f"\nAre you sure you want to Transfer to {receiver}? (y/n) : ").lower()
                if sure == 'y':
                    receiver_id: int = self.return_id(receiver)
                    amount: int = int(input("Enter Amount to Transfer : $ "))
                    if amount <= 0:
                        print("Amount must be greater than 0.")
                    elif amount > self.user_list[sender_id]['amount']:
                        print('\nInsufficient Balance.\n')
                    else:
                        confirmation :str = input("Confirm your Password to Transfer : ").strip()
                        if confirmation == self.user_list[sender_id]['password']:
                            self.user_list[sender_id]['amount'] -= amount
                            self.user_list[receiver_id]['amount'] += amount
                            self.save_user()
                            print("\n#####  Transfer Complete   #####")
                        else:
                            print("Wrong Password.\nPlease enter your password correctly.")
                elif sure == 'n':
                    print("\n#####  Transfer Cancelled    #####")
                else:
                    print("Please Enter Valid Character.\n")
            else:
                print("\nUser Name not Found.\n")

    def withdraw(self, l_username):
        print("\n#####    Withdraw    #####\n")
        amount: int = int(input("Enter the amount to withdraw : $ "))
        user_id: int = self.return_id(l_username)
        if amount <= 0:
            print("Amount must be greater than 0.")
        elif amount > self.user_list[user_id]['amount']:
            print("\n#####   Insufficient Balance   #####")
        else:
            self.user_list[user_id]['amount'] -= amount
            self.save_user()
            print("\n#####   Withdraw Complete  #####\n")

    def update_information(self, username):
        print("\n#####   Update   #####")
        print("1. Change Username\n2. Change Password\n3. Deposit\n4. Back")
        option: int = int(input("What do you want to update ( 1 - 4 ) :"))
        user_id: int = self.return_id(username)

        if option == 1:
            before: str = username
            after: str = input("\nEnter Name to change :")
            sure = input(f"Are you sure you want to change from {before} to {after}? (y/n) :").lower()
            if sure == 'y':
                user_confirmation: str = input("Please enter your password to change name : ").strip()
                if user_confirmation == self.user_list[user_id]['password']:
                    if self.r_name_check(after):
                        print('\n#####  UserName already exist  #####\nPlease Use Different Username.\n')
                    else:
                        self.user_list[user_id]['username'] = after
                        self.save_user()
                        print("\n#####  Name Change Complete   #####\n")
                        self.second_option(self.user_list[user_id]['username'])
                else:
                    print("\nWrong password.\nPlease enter your password carefully.")
            elif sure == 'n':
                print("\n#####  Name change cancelled   #####")
            else:
                print("\n#####  Please Enter Valid Characters   #####")


        elif option == 2:
            before: str = self.user_list[user_id]['password']
            after: str = input("\nPlease Enter New Password : ")
            after1: str = input("Confirm New Password :")
            if after1 == after:
                sure: str = input(f"Are you sure You want to change your password to {after}. (y/n) :").lower()
                if before == after:
                    print("\nYou can't change to your Old password.")
                else:
                    if sure == 'y':
                        confirm: str = input("\nPlease Enter your Old Password to change :")
                        if before == confirm:
                            self.user_list[user_id]['password'] = after
                            print('\n#####  Changing Password Complete    #####')
                            self.save_user()
                        else:
                            print('\n#####  Wrong Password  #####\nPlease Enter your old password Carefully.')
                    else:
                        print("\n#####  Password change cancelled   #####")
            else:
                print("\n#####  Please Enter your New password carefully    #####")

        elif option == 3:
            amount: int = int(input("\nPlease Enter the amount to Deposit : $ "))
            sure: str = input(f"Are you sure You want to Deposit $ {amount}. ( y/n ) :").lower()
            if sure == 'y':
                if amount <= 0:
                    print("Amount must be greater than 0.")
                else:
                    self.user_list[user_id]['amount'] += amount
                    print('#####    Deposit Complete    #####')
                    self.save_user()
            else:
                print('#####    Deposit Cancelled    #####')

        elif option == 4:
            return

        else:
            print("Please Enter the Valid Number ( 1 - 4 )")

    def return_id(self, name):
        for i in self.user_list:
            if self.user_list[i]['username'] == name:
                return i

    def l_name_pass_check(self, l_name, l_pass):
        for id in self.user_list:
            if self.user_list[id]['username'] == l_name and self.user_list[id]['password'] == l_pass:
                return True
        return False

    def register(self):
        print("\n#####    Account Register    #####")
        r_name: str = input("Enter Username :").strip()
        r_password: str = input("Enter Password :").strip()
        r_password2: str = input("Confirm Password :").strip()
        if self.r_name_check(r_name):
            print("User Name Already Exist.\nPlease Enter Different User Name.")
        else:
            if r_password == r_password2:
                id: int = self.check_user_count()
                user_form: dict = {id: {'username': r_name, 'password': r_password, 'amount': 0}}
                self.user_list.update(user_form)
                self.save_user()
                print('\n#####  Account Register Successfully   #####')
            else:
                print('Please Enter Your Password Carefually.')

    def r_name_check(self, r_name):
        for id in self.user_list:
            if self.user_list[id]['username'] == r_name:
                return True
        return False

    def check_user_count(self):
        user_count = len(self.user_list)
        return user_count + 1


if __name__ == '__main__':
    mini_bank: MiniBank = MiniBank()
    mini_bank.first_option()
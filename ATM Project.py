# ATM app - Erkan-Kerim

class User:
    def __init__(self, user_name, user_password, user_id):
        self.user_name = user_name
        self.user_password = user_password
        self.user_id = user_id

class Bank(User):
    def __init__(self):
        pass

    def trigger(self):
        while True:
            try:
                print("""
                --- Welcome to our Bank! ---
                [1] Bank user Login
                [2] I want to be a new Bank user

                """)
                user_login_choice = input("Make your choise: ")

                if user_login_choice == "1":
                    self.login()
                elif user_login_choice == "2":
                    self.be_bank_user()
            except:
                print("Please choose 1 or 2!")

    
    def atm_menu(self):
        while True:
            try:
                print("""
                --- Main Menu ---
                [1] Check balance
                [2] Insert Money
                [3] Withdraw Money
                [4] Transfer Money
                [5] Edit user information
                [Q] Log out
                """)

                customer_choise = input("Make your choise: ")

                if customer_choise == "1":
                    self.check_balance()
                elif customer_choise == "2":
                    self.insert_money()
                elif customer_choise == "3":
                    self.withdraw_money()
                elif customer_choise == "4":
                    self.transfer_money()
                elif customer_choise == "5":
                    self.edit_user()
                elif customer_choise == "Q" or customer_choise == "q":
                    self.trigger()
            except:
                print("Please try again!")
                
    def login(self):
        while True:
            try:
                with open("./users/all_users.txt", "r") as file:
                    users_list = file.readlines()

                all_users = []
                for user in users_list: 
                    all_users.append("-".join(user[:-1].split("-"))) 
                
                #---- TEST --- Program calistiktan sonra bu asagidaki for dongusu kalkacak
                # for user in all_users:
                #     print(user)
                
                # girilen user_id kontrol etmek icin tum user_id lerin oldugu bir liste yapiyoruz
                user_ids = []
                for user in users_list:
                    user_ids.append(int(user.split(")")[0]))

                entered_id = int(input("\nPlease enter your Bank Account ID: "))
                self.user_id = entered_id # User id bilgisine her yerden ulasabilmek icin yapiyoruz -> Cunku Bank(User) inherit ettik
                # Bu asagidaki parola ve sifre kontrol edildikten sonra da yapilabilir
                
                if entered_id in user_ids:
                    entered_user_name = input("Please enter your name: ")
                    entered_user_password = input("Please enter your password: ")
                    chosen_user = all_users[entered_id-1].split("-")
                    if entered_user_name == chosen_user[0][2:] and entered_user_password == chosen_user[1]:
                        print("\nWelcome {}".format(entered_user_name))                        
                        self.atm_menu()
                    else:
                        print("You entered a wrong User name or Password!")
                else:
                    print("User not found!")
            except:
                print("Fout!")

    def check_balance(self):
        print("\n   Your current balance is: {}\n".format(self.get_user_balance()))
        # input("Press Enter to go back to the Main menu!\n")

    def insert_money(self):
        print("\nYour current balance is: {}\n".format(self.get_user_balance()))
        while True:
            try:
                amount = int(input("Enter the amount of money you wish to deposit: "))
                confirmation = input("\nDo you approve a deposit of {} euro into your own account? Y/N \n".format(amount))
                if confirmation == "Y" or confirmation == "y":
                    self.change_user_balance(amount)
                    print("\n{} euro has been successfully deposited into your own account.\n".format(amount))
                    print("\n   Your current balance is: {}\n".format(self.get_user_balance()))
                    break
                elif confirmation == "N" or confirmation == "n":
                    print("transaction canceled!\n")
            except:
                print("Please enter amount of money that you want to deposit")

    def withdraw_money(self):
        print("---WITHDRAW MONEY---")
        print("\nYour current balance is: {}\n".format(self.get_user_balance()))
        while True:
            try:
                amount = int(input("Enter the amount of money you wish to withdraw: "))
                #burada if yapisi ile amount un user_balance'dan buyuk olup olmadigi kontrol edilmeli
                # sonrasinda asagidaki kisim gelmeli
                if amount > int(self.get_user_balance()):
                    print("\nYou dont have enough money to complete this transaction!\n !!!Please choose an amount less then {} euro!!!\n".format(self.get_user_balance()))
                else:
                    confirmation = input("Do you approve a withdraw of {} euro from your own account? Y/N \n".format(amount))
                    if confirmation == "Y" or confirmation == "y":
                        amount = (-1) * amount 
                        self.change_user_balance(amount)
                        amount = (-1) * amount
                        print("{} euro has been successfully withdrawed from your account.\n".format(amount)) # Amount degeri - de oldugu icin birinci degerden itibaren aliyoruz
                        print("\n   Your current balance is: {}".format(self.get_user_balance()))
                        break
                    elif confirmation == "N" or confirmation == "n":
                        print("transaction canceled!")
            except:
                print("Please enter amount of money that you want to withdraw")

    def transfer_money(self):
        # Buraya while dongusu eklenebilir
        try:
            print("\nYour current balance is: {}\n".format(self.get_user_balance()))

            with open("./users/all_users.txt", "r") as file:
                        users_list = file.readlines()
            user_ids = []
            for user in users_list:
                user_ids.append(int(user.split(")")[0]))

            amount =  int(input("Enter the amount that you want to transfer: "))
            id_to_transfer = int(input("Enter the Bank User ID to transfer money: "))

            if id_to_transfer in user_ids:
                if amount > int(self.get_user_balance()):
                    print("\nYou dont have enough money to complete this transaction!\n !!!Please choose an amount less then {} euro!!!\n".format(self.get_user_balance()))
                else:
                    self.change_user_balance((amount * (-1)))

                    id_before = self.user_id

                    self.user_id = id_to_transfer # Burada secilen ID ye para yatirmasi icin 
                    self.change_user_balance(amount)

                    self.user_id = id_before

                    print(str(amount) + " euro successfully transferred!")
            else:
                print("Could not find any user for this ID! Please try again!")
        except:
            print("Failed to transfer money!")

    def edit_user(self):
        # Bu kisim gelistirilebilir, Su an direk 3 veriyi sorarak degisiklik yapiliyor
        # Burada hangi veriyi degistirmek istedigi sorulabilir ve ona gore islem yapilabilir

        with open("./users/all_users.txt", "r") as file:
                    users_list = file.readlines()
        
        new_user_name = input("Enter your new User Name: ")
        new_password = input("Enter your new Password: ")
        new_email = input("Enter your new Email: ")
        updated_user_data = updated_user = (str(self.user_id) + ")" + new_user_name + "-"+new_password+"-"+new_email+"-"+str(self.get_user_balance())+"\n")

        users_list.pop(self.user_id-1) #Girilen ID deki satiri sildi ve ben buraya guncellenmis versiyonun eklemek istiyorum
        users_list.insert(self.user_id-1,updated_user_data)

        with open("./users/all_users.txt","w") as file:
            file.writelines(users_list)
    
    def be_bank_user(self):
        
        print("---Creating new user account---\n")
        bank_user_id = 1
        bank_user_balance = 0
        user_name = input("Enter your name: ")
        user_password = input("Create your password: ")
        user_email = input("Enter your email: ")

        with open("./users/all_users.txt", "r") as file:
            users_list = file.readlines() # readlines ile bir liste olusur

        if len(users_list) == 0:
            bank_user_id = 1
        else:
            with open("./users/all_users.txt", "r") as file:
                bank_user_id = int(file.readlines()[-1].split(")")[0]) +1 # Burada user filemizi read modunda acip ) isaretine gore split yaparak user_id degerini bir artiriyoruz


        with open("./users/all_users.txt", "a+") as file: # a+ ile -> dosyayi acar ve son satirina gider
            file.write("{}){}-{}-{}-{}\n".format(bank_user_id,user_name,user_password,user_email,bank_user_balance))
        
        print("Your account has been successfully created")
        user_info = """

Your User ID is: {}
Your User Name is: {}
Your Password is: {}

Please DON'T FORGET your credentials! You are going to login with this data!

        """.format(bank_user_id,user_name,user_password)
        print(user_info)
        input("If you have saved your user information, press Enter to login!")


    def change_user_balance(self, amount):

        with open("./users/all_users.txt", "r") as file:
                all_users = file.readlines()

        # current_data_only = all_users[self.user_id-1].split("-")[:-1]
        # updated_user_balance = int(all_users[self.user_id-1].split("-")[3]) + amount
        # updated_user = (current_data_only+"-"+str(updated_user_balance)+"\n")
        # all_users.pop(self.user_id-1) #Girilen ID deki satiri sildi ve ben buraya guncellenmis versiyonun eklemek istiyorum
        # all_users.insert(self.user_id-1,updated_user)
                
        chosen_user_name = all_users[self.user_id-1].split("-")[0]
        chosen_user_password = all_users[self.user_id-1].split("-")[1]
        chosen_user_email = all_users[self.user_id-1].split("-")[2]
        updated_user_balance = int(all_users[self.user_id-1].split("-")[3]) + amount
        updated_user = (chosen_user_name+"-"+chosen_user_password+"-"+chosen_user_email+"-"+str(updated_user_balance)+"\n")
        all_users.pop(self.user_id-1) #Girilen ID deki satiri sildi ve ben buraya guncellenmis versiyonun eklemek istiyorum
        all_users.insert(self.user_id-1,updated_user)

        with open("./users/all_users.txt","w") as file:
            file.writelines(all_users)

    def get_user_balance(self):
        with open("./users/all_users.txt", "r") as file:
                    users_list = file.readlines()
        
        database_user_balance = users_list[self.user_id - 1].split("-")[-1][:-1]
        
        return database_user_balance
        
def main():
    Bank().trigger()  


if __name__ == "__main__":
    main()
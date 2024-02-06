import mysql.connector

conn = mysql.connector.connect(
    host="localhost", user="root", password="root@1997", port="3306", autocommit=True
)
my_cursor = conn.cursor()
my_cursor.execute("Create Database if not Exists Bank_db")
my_cursor.execute("Use Bank_db")

#  create table....

my_cursor.execute(
    "Create table if not exists bank_account(acc_no int primary key auto_increment,name varchar(30),city char(20),mobile_no varchar(10),balance int(10))"
)
my_cursor.execute(
    "Create table if not exists Transaction(acc_no int,amount int(10),ttype char(3),foreign key (acc_no) references bank_account(acc_no))"
)
print(".....Welcome to ICICI Bank.....")
while True:
    print(
        "1.Create Account 2.Deposit Money 3.Withdraw Money 4.View Account Details 5.EXIT"
    )
    ch = int(input("Enter your choice for Transactions..."))
    # Create new account.....
    if ch == 1:
        name = input("Enter Your name :")
        city = input("Enter your city name: ")
        mn = input("Enter your Mobile Number: ")
        balance = 0
        sql = "Insert into bank_account(name,city,mobile_no,balance)values(%s,%s,%s,%s)"
        val = (name, city, mn, balance)
        my_cursor.execute(sql, val)
        my_cursor.execute("select * from bank_account where name=' " + name + "'")
        print("New Account is created Successfully....")
        for i in my_cursor:
            print(i)

    #  Deposit Money...
    elif ch == 2:
        accno = input("Enter Account Number to Deposit Money :")
        dp = int(input("Enter amount to Deposit into Account :"))
        ttype = "d"
        my_cursor.execute(
            "insert into transaction values('"
            + accno
            + "','"
            + str(dp)
            + "','"
            + ttype
            + "')"
        )
        my_cursor.execute(
            "Update bank_account set balance= balance+'"
            + str(dp)
            + "' where acc_no='"
            + accno
            + "'"
        )
        print("RS.", dp, "has been deposited into your bank account: ", accno)

    elif ch == 3:
        accno = input("Enter Your account number to withdraw money:")
        wd = int(input("Enter amount to be withdrawn:"))
        select_Query = (
            "Select balance from bank_account where acc_no = '" + accno + "' "
        )
        my_cursor.execute(select_Query)
        bal = my_cursor.fetchone()[0]
        if wd < bal:
            ttype = "W"
            my_cursor.execute(
                "Insert into transaction values('"
                + accno
                + "','"
                + str(wd)
                + "','"
                + ttype
                + "')"
            )
            my_cursor.execute(
                "Update bank_account set balance=balance-'"
                + str(wd)
                + "' WHERE acc_no='"
                + accno
                + "'"
            )
            print("RS.", wd, "has  been withdrawan successfully from account_no", accno)
        else:
            print("Can't withdraw money. Insufficient Balance!...")

    # Display Account Details...
    elif ch == 4:
        accno = input("Enter account number to fetch account details :")
        my_cursor.execute("select * from bank_account where acc_no='" + accno + "'")
        for i in my_cursor:
            print(i)
    else:
        break

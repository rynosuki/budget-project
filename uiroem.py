import os
import databases
import datetime

class UI():
  vers = "1.0"
  db = databases.createDatabase()

  def mainMenu(self):
    self.headerText()
    print("Main Menu:\n")
    print("1. Add Income\n2. Add Expense\n3. Show Table Values for Month\n4. Run Queries\n5. Quit\n")
    try:
        value = int(input("Choose option (1-5) to continue: "))
    except TypeError as err:
        print(err)

    if value == 1:
        self.addIncome()
    elif value == 2:
        self.addExpenses()
    elif value == 3:
        self.showTables()
    elif value == 4:
        self.runQuery()
    elif value == 5:
        self.quitMenu()

  def addIncome(self):
    i_text = "Add Income:\n"
    self.headerText()
    print(i_text)
    i_amount = input("Income amount: ")
    
    self.headerText()
    print(i_text)
    i_contributor = input("Income contributor: ")

    self.headerText()
    print(i_text)
    i_source = input("Income source: ")

    self.headerText()
    print(i_text)
    i_date = input("Income date (yyyymmdd): ")

    self.db.importData(table = "income", amount = i_amount, contributor = i_contributor, source = i_source, date = i_date)

    value = input("Return to main menu or retry? Y/R/N: ")

    if value.lower() == "y":
        self.mainMenu()
    elif value.lower() == "r":
        self.addIncome()
    else:
        self.quitMenu()

  def addExpenses(self):
    self.headerText()
    print("Add Expense:\n")
    i_amount = input("Expense amount: ")
    
    self.headerText()
    print("Add Expense:\n")
    i_contributor = input("Expense contributor: ")

    self.headerText()
    print("Add Expense:\n")
    i_source = input("Expense source (store): ")

    self.headerText()
    print("Add Expense:\n")
    i_date = input("Expense date (yyyymmdd): ")

    self.headerText()
    print("Add Expense:\n")
    i_note = input("Expense note: ")

    self.db.importData(table = "expenses", amount = i_amount, contributor = i_contributor, source = i_source, 
        date = i_date, note = i_note)

    value = input("Do you want to add any items to the expense? (Y/N) ")

    if value.lower() == "y":
        self.addItems(int(i_amount))
    else:
        self.mainMenu()

  def addItems(self, spent_amount):
    cur_index = self.db.getIndexID()

    self.headerText()
    print("Add Items:\n Spent this expense: ", spent_amount, "\n")
    i_name = input("Item name: ")
    
    self.headerText()
    print("Add Items:\n Spent this expense: ", spent_amount, "\n")
    i_quantity = input("How many?: ")

    self.headerText()
    print("Add Items:\n Spent this expense: ", spent_amount, "\n")
    i_price = input("Price per unit: ")

    self.headerText()
    print("Add Items:\n Spent this expense: ", spent_amount, "\n")
    i_type = input("Expense type: ") 
    spent_amount = spent_amount-(int(i_quantity) * int(i_price))   

    self.db.importData(table = "items", name = i_name, quantity = i_quantity, price = i_price, expense_type = i_type, expenseid = cur_index)

    value = input("Do you want to add more items to the expense? (Y/N) ")

    if value.lower() == "y":
        self.addItems(spent_amount)
    else:
        self.mainMenu()

  def showTables(self):
    self.headerText()

    i_table = input("Which table do you want to view? (income, expenses): ")
    self.headerText()

    i_month = input("Which month of the year? (1-12): ")
    self.headerText()

    pos_year = input("Which year? (empty for current): ")
    if pos_year == "":
        now = datetime.datetime.now()
        year = str(now.year)
    else:
        year = pos_year

    self.setHeader(i_table)
    data = self.db.fetchData(table = i_table, month = i_month, year = year)
    for i in data:
      for n in i:
        print(n, end="\t")
      print("")

    value = input("Return to main menu or retry? Y/R/N: ")

    if value.lower() == "y":
        self.mainMenu()
    elif value.lower() == "r":
        self.showTables()
    else:
        self.quitMenu()

  def runQuery(self):
    self.headerText()
    print("\n1. Get a overlook of all expense types and the combined expense of a given month")
    print("2. Most expensive item during a month")
    print("3. Get details from receipt")
    print("4. Income - Expenses monthly over the year")
    print("5. Amount spent on a specified product in the different stores")
    print("6. Quit")

    value = input("\nChoose menu type: ")

    if value == "1":
        self.headerText()
        month = input("\nWhich month do you want to view? (1-12) ")
        self.headerText()
        year = input("\nWhich year? (nothing for current) ")
        if year == "":
            now = datetime.datetime.now()
            year = str(now.year)
        else:
            year = year
        print("Name", end = " " * 16)
        print("Price", end = " " * 15)
        print()
        data = self.db.queryHandler(choice = 1, month = month, year = year)
        self.printValues(data)
        value = input("\nReturn to main menu? Y/N ")
        if value.lower() == "y":
            self.runQuery()
        else:
            self.quitMenu()
    elif value == "2":
        self.headerText()
        year = input("\nWhich year? (nothing for current) ")
        if year == "":
            now = datetime.datetime.now()
            year = str(now.year)
        else:
            year = year
        data = self.db.queryHandler(choice = 2, year = year) 
        print("Month", end = " " * 15)
        print("Year", end = " " * 16)
        print("Price", end = " " * 15)
        print()
        self.printValues(data)
        value = input("\nReturn to main menu? Y/N ")
        if value.lower() == "y":
            self.runQuery()
        else:
            self.quitMenu() 
    elif value == "3":
        self.headerText()
        data = self.db.showExpenses()
        print("\nID", end = " " * 18)
        print("Amount", end = " " * 14)
        print("Date", end = " " * 16)
        print()
        self.printValues(data)
        print("")
        value = input("Choose an ID to view receipt: ")
        self.headerText()
        data = self.db.queryHandler(choice = 3, expenseid = value)
        print("\nName", end = " " * 16)
        print("Amount", end = " " * 14)
        print("Price", end = " " * 15)
        print()
        self.printValues(data)
        value = input("\nReturn to main menu? Y/N ")
        if value.lower() == "y":
            self.runQuery()
        else:
            self.quitMenu()
    elif value == "4":
        self.headerText()
        year = input("Which year do wish to view? ")
        data = self.db.queryHandler(choice = 4, year = year)
        print("\nMonth", end=" " * 15)
        print("Income", end=" " * 14)
        print("Expense", end=" " * 13)        
        print("Profit", end=" " * 14)
        print()
        self.printValues(data)
        value = input("\nReturn to main menu? Y/N ")
        if value.lower() == "y":
            self.runQuery()
        else:
            self.quitMenu()
    elif value == "5":
        self.headerText()
        name = input("Which product do you wish to see? ")
        data = self.db.queryHandler(choice = 5, name = name)
        print("\nSource", end = " " * 14)
        print("Sum", end = " " * 17)
        print("Name", end = " " * 16)
        print()
        self.printValues(data)
        value = input("\nReturn to main menu? Y/N ")
        if value.lower() == "y":
            self.runQuery()
        else:
            self.quitMenu()
    elif value == "6":
        self.quitMenu()
    else:
        self.runQuery()

  def quitMenu(self):
    os.close(fd=0)

  def headerText(self):
    clear = lambda: os.system('cls')
    clear()
    print("RoEm BudgetProgram v" + self.vers)

  def setHeader(self, table):
      if table == "income":
          print("Amount\tName\tSource")
      elif table == "expenses":
          print("Amount\tName\tSource\tNote")
      elif table == "items":
          print("Name\tPrice\tQuantity\tType")

  def printValues(self, values):
    for i in values:
        for j in i: print(j, end=" " * (20-len(str(j))))
        print("")
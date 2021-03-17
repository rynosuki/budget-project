import mysql.connector
from mysql.connector import errorcode

class createDatabase():
  db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "root"
  )
  db_name = "budgetproject"
  my_cursor = db.cursor()

  def dbCreate(self):
    try:
      self.my_cursor.execute("CREATE DATABASE " + self.db_name)
      self.my_cursor.execute("use " + self.db_name)
      a = ["income", "expenses", "items"]
      for i in a: self.createTable(i)
      self.importBulkData()
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with ur username or password.")
      elif err.errno == errorcode.ER_DB_CREATE_EXISTS:
        self.my_cursor.execute("use " + self.db_name)
      else:
        print(err)

  def createTable(self, table):
    try:
      if table == "income":
        self.my_cursor.execute("CREATE TABLE income ("
        "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
        "amount INT,"
        "contributor VARCHAR(32),"
        "source VARCHAR(20),"
        "date DATE);")
      elif table == "expenses":
        self.my_cursor.execute("CREATE TABLE expenses ("
        "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,"
        "amount INT,"
        "contributor VARCHAR(32),"
        "source VARCHAR(32),"
        "date DATE,"
        "note VARCHAR(255));")
      elif table == "items":
        self.my_cursor.execute("CREATE TABLE items ("
        "expenseid INT NOT NULL,"
        "name VARCHAR(20) NOT NULL,"
        "price INT NOT NULL,"
        "quantity INT NOT NULL,"
        "type VARCHAR(20) NOT NULL);")
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        return

  def createView(self):
    try:
      self.my_cursor.execute("CREATE VIEW totincome AS "
                            "SELECT sum(amount) AS total, date "
                            "FROM budgetproject.income "
                            "GROUP BY year(date),month(date);")
      self.my_cursor.execute("CREATE VIEW totexpenses AS "
                            "SELECT sum(amount) AS total, date "
                            "FROM budgetproject.expenses "
                            "GROUP BY year(date),month(date);")                                         
      self.my_cursor.execute("CREATE VIEW stuff AS "
                            "SELECT items.type AS type, (items.price * items.quantity) AS total, MONTH(expenses.date) AS month "
                            "FROM items "
                            "LEFT JOIN expenses "
                            "ON expenses.id = items.expenseid;")
    except Exception as e:
      print(e)


  def importData(self, **kwargs):
    if kwargs["table"] == "income":
      self.my_cursor.execute("INSERT INTO income (amount, contributor, source, date) " +
      "VALUES (" + str(kwargs["amount"]) + ",\'" + kwargs["contributor"] + "\',\'" + kwargs["source"] + "\',\'" + kwargs["date"] + "\')")

    elif kwargs["table"] == "expenses":
      self.my_cursor.execute("INSERT INTO expenses (amount, contributor, source, date, note) " +
      "VALUES (" + str(kwargs["amount"]) + ",\'" + kwargs["contributor"] + "\',\'" + kwargs["source"] + "\',\'" + kwargs["date"] + "\',\'"
      + kwargs["note"] + "\')")

    elif kwargs["table"] == "items":
      self.my_cursor.execute("INSERT INTO items (name, price, quantity, type, expenseid) " +
      "VALUES (\'" + kwargs["name"] + "\',\'" + str(kwargs["price"]) + "\',\'" + str(kwargs["quantity"]) + "\',\'" + kwargs["expense_type"] +"\',\'" + str(kwargs["expenseid"]) + "\')")
    self.db.commit()

  def fetchData(self, **kwargs):
    if kwargs["table"] == "income":
      self.my_cursor.execute("SELECT amount, contributor, source FROM income WHERE year(date) = " + kwargs["year"] + " AND month(date) = " + kwargs["month"])
    elif kwargs["table"] == "expenses":
      self.my_cursor.execute("SELECT amount, contributor, source ,note FROM expenses WHERE year(date) = " + kwargs["year"] + " AND month(date) = " + kwargs["month"])
    data = self.my_cursor.fetchall()
    return data

  def importBulkData(self):
    with open('db.sql', 'r', encoding="utf-8") as f:
      sql_file = f.read()
      sql_commands = sql_file.split(';')
      for command in sql_commands:
        try:
          self.my_cursor.execute(command)
        except Exception as msg:
          print ("Command skipped: ", msg)


  def getIndexID(self):
    self.my_cursor.execute("SELECT id FROM expenses")
    data = self.my_cursor.fetchall()
    i = data[len(data)-1][0]
    return i

  def showExpenses(self):
    self.my_cursor.execute("SELECT id, amount, date "
                          "FROM Expenses")
    data = self.my_cursor.fetchall()
    return data

  def queryHandler(self, **kwargs):
    if kwargs["choice"] == 1:
      self.my_cursor.execute("SELECT items.type, sum(items.price*items.quantity) AS total_price "
                            "FROM items "
                            "JOIN expenses "
                            "ON expenses.id = items.expenseid AND MONTH(expenses.date) = " + kwargs["month"] + " AND YEAR(expenses.date) = " + kwargs["year"]
                            + " GROUP BY type")
    elif kwargs["choice"] == 2:
      self.my_cursor.execute("SELECT monthname(expenses.date) AS month, items.name, items.price*items.quantity as price "
                            "FROM budgetproject.items "
                            "JOIN budgetproject.expenses "
                            "ON expenses.id = items.expenseid "
                            "WHERE year(expenses.date) = " + kwargs["year"] + " AND items.price*items.quantity IN ("
                            "SELECT max(items.price*items.quantity) FROM budgetproject.items GROUP BY type) "
                            "GROUP BY month(expenses.date)")
    elif kwargs["choice"] == 3:
      self.my_cursor.execute("SELECT items.name, items.quantity, items.quantity*items.price "
                            "FROM budgetproject.items "
                            "JOIN budgetproject.expenses "
                            "ON expenses.id = items.expenseid "
                            "WHERE expenseid = " + kwargs["expenseid"])
    elif kwargs["choice"] == 4:
      self.my_cursor.execute("SELECT monthname(income.date) AS MONTH, income.total AS income, expense.total AS expenses, coalesce(income.total,0) - coalesce(expense.total,0) AS Profit "
                            "FROM budgetproject.totincome AS income "
                            "LEFT OUTER JOIN budgetproject.totexpenses AS expense "
                            "ON month(income.date) = month(expense.date) "
                            "WHERE year(expense.date) = " + kwargs["year"] + " AND year(income.date) = " + kwargs["year"] +
                            " UNION "
                            "SELECT monthname(expense.date) AS MONTH, income.total AS income, expense.total AS expenses, coalesce(income.total,0) - coalesce(expense.total,0) AS Profit "
                            "FROM budgetproject.totincome AS income "
                            "RIGHT OUTER JOIN budgetproject.totexpenses AS expense "
                            "ON month(income.date) = month(expense.date) "
                            "WHERE year(expense.date) = " + kwargs["year"] + " AND year(income.date) = " + kwargs["year"] +
                            " ORDER BY MONTH")
    elif kwargs["choice"] == 5:
      self.my_cursor.execute("SELECT expenses.source, SUM(items.quantity*items.price), items.name "
                            "FROM items "
                            "JOIN expenses "
                            "ON expenses.id = items.expenseid "
                            "WHERE NAME = \'" + kwargs["name"] +
                            "\' GROUP BY source ")
    data = self.my_cursor.fetchall()
    return data
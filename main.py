import databases
import uiroem as u

menu = u.UI()
db = databases.createDatabase()

def main():
  menu.mainMenu()

if __name__ == "__main__":
  db.dbCreate()
  db.createView()
  main()
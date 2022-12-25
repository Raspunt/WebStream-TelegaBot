import sqlite3


class SubscriberDb:

    def __init__(self):
        self.Connect()
        self.CreateUserTable()


    def Connect(self):
        self.con = sqlite3.connect("./Files/Sub.db", check_same_thread=False)

    def CreateUserTable(self):
        cur = self.con.cursor()

        cur.execute("""
                CREATE TABLE IF NOT EXISTS  Users(
                    id INTEGER PRIMARY KEY,
                    FirstName TEXT NOT NULL,
                    SecondName TEXT NOT NULL,
                    userID TEXT NOT NULL
                )
            """)

    def CreateUser(self, userID,FirstName,SecondName):

        cur = self.con.cursor()

        cur.execute(f"""
        INSERT INTO Users (userID,FirstName,SecondName)
        VALUES('{userID}','{FirstName}','{SecondName}')
        """)

        self.con.commit()

    def GetAllUserID(self):
        cur = self.con.cursor()
        res = cur.execute("SELECT userID FROM Users")

        return res.fetchall()

    def GetByUserID(self, userID):
        cur = self.con.cursor()

        res = cur.execute(
            f"SELECT * FROM Users WHERE userID LIKE '{userID}'")

        return res.fetchone()

    def DeleteByUserID(self,userID):
        
        cur = self.con.cursor()

        cur.execute(f"""
            DELETE FROM Subscribers
            WHERE userID LIKE '{userID}';
        """)

        self.con.commit()






# db.Connect()
# db.CreateSubscribeTable()
# db.CreateSubscriber("228")

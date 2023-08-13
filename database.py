import sqlite3

class Database():
    def __init__(self):
        self.db = sqlite3.connect('board.db', check_same_thread=False)
        self.cursor = self.db.cursor()

    def execute(self, query, args={}) :
        self.cursor.execute(query, args)

    def execute_fetch(self, query, args={}) :
        self.cursor.execute(query, args)
        result = self.cursor.fetchall()
        return result
    
    def execute_fetch_one(self, query, args={}) :
        self.cursor.execute(query, args)
        result = self.cursor.fetchone()
        return result
    
    def commit(self):
        self.db.commit()

if __name__ == "__main__" :
    db = Database()

    db.execute("INSERT INTO board(title, message) VALUES (?, ?)", ('new NOTE', 'MESSAGE'))
    db.commit()

    db.execute_fetch("SELECT * FROM board")
    print(db.execute_fetch("SELECT * FROM board"))

    db.execute("DELETE FROM board WHERE id=?", (1, ))
    db.commit()
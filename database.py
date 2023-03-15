import sqlite3


def makeDatabase():
    conn = sqlite3.connect('cats.db')
    cur = conn.cursor()

    cur.execute("""
                CREATE TABLE IF NOT EXISTS cats
                (URL TEXT PRIMARY KEY, AWESOME INTEGER DEFAULT 0, EXTRAAWESOME INTEGER DEFAULT 0)
                """)

    conn.commit()

def main():
    makeDatabase()

if __name__ == '__main__':
    main()
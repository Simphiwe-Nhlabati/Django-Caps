import MySQLdb

try:
    db = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="simphiwe@7",
        db="hyper_news"
    )
    print("✅ Connected to database.")
except Exception as e:
    print("❌ Error:", e)
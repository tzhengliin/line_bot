from pymongo import MongoClient, UpdateOne
from pymongo.errors import DuplicateKeyError

# MongoDB 連接設定
PORT_FORWARDED_HOSTNAME = "hnd1.clusters.zeabur.com"
DATABASE_PORT_FORWARDED_PORT = "32030"

MONGO_URI = f"mongodb://mongo:78HR235kN9qUg6SLC1Aps0haV4YMQGez@{PORT_FORWARDED_HOSTNAME}:{DATABASE_PORT_FORWARDED_PORT}"
client = MongoClient(MONGO_URI)

# 替換為您的資料庫名稱和集合名稱
db = client['coaches_database']
collection = db['students_collection']

# 設置唯一索引
collection.create_index("name", unique=True)

# 學員資料
students_data = [
    {"name": "楊佩芸", "coach": "王秋蓉", "start_date": "2024-09-18", "status": "Start"},
    {"name": "阿荷", "coach": "洪郁惠", "start_date": "2024-10-09", "status": "Start"},
    {"name": "阿香", "coach": "洪郁惠", "start_date": "2024-10-09", "status": "Start"},
    {"name": "許庭瑄", "coach": "洪郁惠", "start_date": None, "status": "NoStarted"},
    {"name": "呂孟惟", "coach": "林子恆", "start_date": "2024-09-04", "status": "Pause"},
    {"name": "王宣又", "coach": "林子恆", "start_date": "2024-09-27", "status": "Start"},
    {"name": "胡勝智", "coach": "林子恆", "start_date": None, "status": "NoStarted"},
    {"name": "李佳玫", "coach": "游忠達", "start_date": "2024-10-02", "status": "Start"},
    {"name": "蔡富秉", "coach": "游忠達", "start_date": "2024-10-09", "status": "Start"},
    {"name": "林永倫", "coach": "游忠達", "start_date": None, "status": "NoStarted"},
    {"name": "楊紅儀", "coach": "陳可欣", "start_date": None, "status": "NoStarted"}
]

# 插入或更新學員資料
def initialize_database():
    operations = []
    for student in students_data:
        operations.append(
            UpdateOne(
                {"name": student["name"]},  # 查找條件
                {"$set": student},  # 更新的內容
                upsert=True  # 如果不存在則插入
            )
        )
    
    # 批量執行更新操作
    result = collection.bulk_write(operations)
    print(f"Inserted: {result.upserted_count}, Updated: {result.modified_count}")

# 呼叫函數以初始化資料庫
initialize_database()

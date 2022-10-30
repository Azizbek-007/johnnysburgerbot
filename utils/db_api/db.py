from unicodedata import category
import mysql.connector

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sx48Bq3A68NvPun",
        database="bot_fastofood"
        )
except: print("Mysql connection error")



def register_user(user_id, first_name, username, phone_number=None):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `members` WHERE `user_id`={}".format(str(user_id)))
    result = mycursor.fetchall()
    print(len(result))
    if len(result) == 0:
        sql = "INSERT INTO `members`(`user_id`, `first_name`, `username`, `phone_number`, `lang`) VALUES (%s, %s, %s, %s, %s)"
        val = (str(user_id), str(first_name), str(username), str(phone_number), str('ru'))
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    return True

def get_users():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT user_id FROM members")
    result = mycursor.fetchall()
    return result

def get_users_count():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM members")
    result = mycursor.fetchall()
    return result[0][0]

def phone_update(user_id, phone_number):
    mycursor = mydb.cursor()
    sql = "UPDATE `members` set `phone_number`=%s WHERE `user_id`=%s"
    val = (str(phone_number), str(user_id))
    print(sql, val)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record updated.")

def userBy(user_id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM `members` WHERE `user_id`={}".format(str(user_id)))
    result = mycursor.fetchall()
    return result

def add_order(order_id):
    mycursor = mydb.cursor()
    sql = "UPDATE `orders` set `status`=1 WHERE `id`=" + order_id
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record updated.")
    
def get_order(order_id):
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sx48Bq3A68NvPun",
    database="bot_fastofood"
    )
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM `orders` WHERE `id`={order_id};"
    mycursor.execute(sql)
    result = mycursor.fetchall()[0][1]
    return result

# CATEGORIES
def create_category(name, image=None):
    mycursor = mydb.cursor()
    sql = "INSERT INTO `category` (`name`, `image`) VALUES (%s, %s)"
    val = (str(name), str(image))
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def GetAllCategory():
    mycursor = mydb.cursor()
    sql = "SELECT * FROM category"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    print(result)
    return result

def DeleteCategory(category_id):
    mycursor = mydb.cursor()
    sql = f"DELETE FROM `category` WHERE `id`={category_id}"
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record deleted.")

def ProductRegister(category_id, name, price, image):
    mycursor = mydb.cursor()
    sql = "INSERT INTO `product` (`categoryId`, `name`, `price`, `image`) VALUES (%s, %s, %s, %s)"
    val = (str(category_id), str(name), str(price), str(image))
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record product inserted")

def GetAllProducts(category_id):
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM `product` where `categoryId`={category_id}"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    if len(result) == 0: return False
    return result

def DeleteProduct(product_id):
    mycursor = mydb.cursor()
    sql = f"DELETE FROM `product` WHERE `id`={product_id}"
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record deleted.")

def Set_Lang(lang, user_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sx48Bq3A68NvPun",
        database="bot_fastofood"
    )
    mycursor = mydb.cursor()
    sql = f"UPDATE `members` set `lang`='{lang}' WHERE `user_id`='{user_id}';"
    mycursor.execute(sql)
    mydb.commit()
    print(mycursor.rowcount, "record updated.")

def Get_Lang(user_id):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sx48Bq3A68NvPun",
        database="bot_fastofood"
    )
    mycursor = mydb.cursor()
    sql = f"SELECT * FROM `members` where `user_id`={user_id}"
    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result[0][5]

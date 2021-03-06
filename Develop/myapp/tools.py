from datetime import datetime
import pymysql

def get_conn():
    conn=pymysql.connect(host="localhost",user="root",passwd="926434",db='cov')
    cursor=conn.cursor()
    return conn,cursor

def close_conn(conn,cursor):
    cursor.close()
    conn.close()

def query(sql):
    conn,cursor=get_conn()
    cursor.execute(sql)
    res=cursor.fetchall()
    close_conn(conn,cursor)
    return res

def get_time():
    return datetime.now().strftime('%Y年%m月%d日 %X')

def get_mid1():
    sql="""select sum(confirm),
(select suspect from history ORDER BY ds desc limit 1),
sum(heal),
sum(dead)
from details
where update_time=(select update_time FROM details ORDER BY update_time desc LIMIT 1)
"""
    res=query(sql)
    return res[0]
def get_mid2():
    sql="""select province,sum(confirm) from details where update_time=
(select update_time from details order by update_time desc limit 1)
GROUP BY province"""
    res=query(sql)
    return res

def get_left1():
    sql="""
    SELECT ds,confirm,suspect,heal,dead from history
    """
    res=query(sql)
    return res

def get_left2():
    sql = """
    SELECT ds,confirm_add,suspect_add from history
        """
    res = query(sql)
    return res

def get_right1():
    sql = """
    select city,confirm from 
(SELECT city,confirm from details 
where update_time=(SELECT update_time FROM details ORDER BY update_time desc limit 1)
and province not in ('湖北','北京','上海','天津','重庆') 
UNION all 
SELECT province as city,sum(confirm) as confirm from details
where update_time=(SELECT update_time from details ORDER BY update_time desc limit 1)
and province in ('北京','上海','天津','重庆') GROUP BY province) as a 
ORDER BY confirm DESC LIMIT 5
        """
    res = query(sql)
    return res

def get_right2():
    sql = """
    SELECT content from hotsearch order by id desc limit 20
        """
    res = query(sql)
    return res

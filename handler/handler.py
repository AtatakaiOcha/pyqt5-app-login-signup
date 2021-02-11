import MySQLdb
import gc


# use your connection here
HOST, USER, PASSWORD, BD = "", "", "", ""


class HandlerBd:
    """
    This class is used to create sql queries and commit changes
    """
    def __init__(self):
        self.db = MySQLdb.connect(host=HOST, user=USER, password=PASSWORD, db=BD)
        self.cur = self.db.cursor()

    def close_connect(self):
        self.db.close()
        gc.collect()

    def query_insert(self, data):
        insert = "INSERT INTO user_data (first_name, second_name, last_name, email, address," \
                 " telephone, passwd) VALUES (%s ,%s, %s, %s, %s, %s, %s);"
        self.cur.execute(insert, data)
        self.db.commit()

    def query_select_all(self):
        select_all = "SELECT * FROM user_data;"
        self.cur.execute(select_all)
        data = self.cur.fetchall()
        return data

    def query_select_current_user(self, data):
        select_user_data = "SELECT id, first_name, second_name, last_name " \
                           "FROM user_data WHERE telephone IN('%s');" % data
        self.cur.execute(select_user_data)
        data = self.cur.fetchall()
        return data

    def query_check_user(self, data):
        select_user_telephone = "SELECT telephone FROM user_data WHERE telephone = '%s'" % data
        self.cur.execute(select_user_telephone)
        data = self.cur.fetchall()
        if not data:
            return True
        else:
            return False

    def query_select_login_passwd(self, telephone, password):
        select_phone = "SELECT telephone FROM user_data WHERE telephone = '%s';" % telephone
        self.cur.execute(select_phone)
        _telephone = self.cur.fetchall()
        select_passwd = "SELECT passwd FROM user_data WHERE passwd = '%s';" % password
        self.cur.execute(select_passwd)
        _password = self.cur.fetchall()
        try:
            if (str(telephone),) == _telephone[0]:
                if (str(password),) == _password[0]:
                    return True
                else:
                    return False
            else:
                return False
        except IndexError:
            pass

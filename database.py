# coding:utf-8

import sqlite3
import argparse

db = 'data/savedata.db'
cdb = 'data/cheat.db'


"""
# データベース
conn = sqlite3.connect(db)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# rankingテーブルが存在しないとき、作成する
cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='ranking'")
if cur.fetchone()[0] == 0:
    cur.execute('CREATE TABLE ranking(id INTEGER PRIMARY KEY, stage INTEGER, score INTEGER)')

# dataテーブルが存在しないとき、作成する
cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='data'")
if cur.fetchone()[0] == 0:
    cur.execute("CREATE TABLE data(key TEXT, value TEXT)")

# データベースへのコネクションを閉じる
conn.close()
"""

def create_table(table_name, keys):
    """
    - table_name : string
    - keys : string list ['key_name type', ...]
    - name type :
        - INTEGER(int)
        - TEXT(str)
        - REAL(float)
    """
    for database in (db, cdb):
        # データベース
        conn = sqlite3.connect(database)
        # sqliteを操作するカーソルオブジェクトを作成
        cur = conn.cursor()

        # rankingテーブルが存在しないとき、作成する
        cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", [table_name])
        execute_text = 'CREATE TABLE ' + table_name + '(' + ', '.join(keys) + ')'
        if cur.fetchone()[0] == 0:
            cur.execute(execute_text)

        # データベースへのコネクションを閉じる
        conn.close()


def insert_score(stage_id, score, cheat):
    # データベース
    if cheat:
        conn = sqlite3.connect(cdb)
    else:
        conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # そのステージのスコアが1000を超えているならdeleteする
    ranking = [data for data in cur.execute('SELECT id, score FROM ranking WHERE stage=?', str(stage_id))]
    if len(ranking) > 1000:
        ranking = sorted(ranking, lambda x:x[1])
        data_id = ranking[0][0]
        cur.execute("DELETE FROM ranking WHERE id=?", [data_id])

    cur.execute('INSERT INTO ranking(stage, score) values(?, ?)', [stage_id, score])


    # データベースへの変更をコミット
    conn.commit()
    # データベースへのコネクションを閉じる
    conn.close()

def load_ranking(stage_id, cheat):
    # データベース
    if cheat:
        conn = sqlite3.connect(cdb)
    else:
        conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    ranking = [data for data in cur.execute('SELECT id, score FROM ranking WHERE stage=?', str(stage_id))]
    # データベースへのコネクションを閉じる
    conn.close()
    return ranking

def _save_gun(cur, values):
    for gun_id, dic in values.items():
        # keyがテーブル内に存在するなら更新、存在しないなら追加する。
        cur.execute("SELECT COUNT(*) FROM gun WHERE id=? AND name=?", [gun_id, dic['name']])
        if cur.fetchone()[0] == 0:
            data_list = [gun_id, dic['name'], dic['bullet_size'], dic['reload_size'], dic['own']]
            cur.execute("INSERT INTO gun(id, name, bullet_size, reload_size, own) values(?, ?, ?, ?, ?)", data_list)
        else:
            cur.execute("UPDATE gun SET own=? WHERE id=?", [dic['own'], gun_id])
        
def _save_equip(cur, data):
    cur.execute("SELECT COUNT(*) FROM equipment WHERE id=?", [1])
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO equipment(gun1, gun2, gun3) values(?,?,?)", data)
    else:
        cur.execute("UPDATE equipment SET gun1=?, gun2=?, gun3=?", data)

def _save_chip(cur, data):
    cur.execute("SELECT COUNT(*) FROM chips WHERE id=?", [1])
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO chips(chip1, chip2, chip3, chip4, chip5, chip6) values(?,?,?,?,?,?)", data)
    else:
        cur.execute("UPDATE chips SET chip1=?, chip2=?, chip3=?, chip4=?, chip5=?, chip6=?", data)

def _save_chip_data(cur, dic):
    for i, value in dic.items():
        # keyがテーブル内に存在するなら更新、存在しないなら追加する。
        cur.execute("SELECT COUNT(*) FROM own_chip WHERE id=?", [i])
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO own_chip(id, num) values(?, ?)", [i, value['num']])
        else:
            cur.execute("UPDATE own_chip SET num=? WHERE id=?", [value['num'], i])

def save(data_dic, cheat):
    # データベース
    if cheat:
        conn = sqlite3.connect(cdb)
    else:
        conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()
    for key, value in data_dic.items():
        if key == 'gun_data':
            _save_gun(cur, value)
            value = 'gun table'
        elif key == 'equip':
            _save_equip(cur, value)
            value = 1       # id
        elif key == 'chip':
            _save_chip(cur, value)
            value = 1       # id
        elif key == 'chip_data':
            _save_chip_data(cur, value)
            value = 'own_chipTABLE'
        # keyがテーブル内に存在するなら更新、存在しないなら追加する。
        cur.execute("SELECT COUNT(*) FROM data WHERE key=?", [key])
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO data(key, value) values(?, ?)", [key, value])
        else:
            cur.execute("UPDATE data SET value=? WHERE key=?", [value, key])
    # データベースへの変更をコミット
    conn.commit()
    # データベースへのコネクションを閉じる
    conn.close()

def _load_gun(cur):
    dic = {}
    for gun_data in cur.execute("SELECT * FROM gun"):
        data = {}
        gun_key = gun_data[0]
        data['name'], data['bullet_size'], data['reload_size'], data['own'] = gun_data[1:5]
        dic[gun_key] = data
    return dic

def _load_equip(cur):
    equipment = list(cur.execute("SELECT gun1, gun2, gun3 FROM equipment"))[0]
    return equipment

def _load_chip(cur):
    chip = list(cur.execute("SELECT chip1, chip2, chip3, chip4, chip5, chip6 FROM chips"))[0]
    return chip

def _load_chip_data(cur):
    data = {}
    for i, num in cur.execute("SELECT id, num FROM own_chip"):
        data[i] = {'num':num}
    return data

def load(flag=False):
    # データベース
    if flag:
        conn = sqlite3.connect(cdb)
    else:
        conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # dataテーブル内から全てのデータを辞書にして取り出す。
    data_dic = {}
    data_list = list(cur.execute("SELECT * FROM data"))
    for key, value in data_list:
        if key == 'gun_data':
            data_dic[key] = _load_gun(cur)
        elif key == 'equip':
            data_dic[key] = _load_equip(cur)
        elif key == 'chip':
            data_dic[key] = _load_chip(cur)
        elif key == 'chip_data':
            data_dic[key] = _load_chip_data(cur)
        else:
            data_dic[key] = value

    # データベースへのコネクションを閉じる
    conn.close()
    return data_dic

if __name__=='__main__':
    # このプログラムをメインで実行したとき
        
    parser = argparse.ArgumentParser(description='ReKにおけるデータベースを管理するファイル')
    parser.add_argument('--delete', action='store_true', help="すべてのデータベースを初期化する")
    parser.add_argument('-s', '--show', action='store_true', help="すべてのデータベースの中身を表示する")
    parser.add_argument('-c', '--cheat', action='store_true', help='操作するデータベースをチートデータに変更')
    args = parser.parse_args()
    
    if args.cheat:
        db = cdb
    
    # データベース
    conn = sqlite3.connect(db)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()


    if args.show:
        tables = cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
        for table in list(tables):
            print(table[4][13:])
            table = table[1]
            print('-'*100)
            for row in cur.execute("SELECT * FROM "+table):
                print(row)
            print()


    if args.delete:
        tables = cur.execute("SELECT * FROM sqlite_master WHERE type='table'")
        for table in list(tables):
            table = table[1]
            cur.execute("DROP TABLE "+table)
            cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?", [table])
            if cur.fetchone()[0] == 0:
                print(table, "TABLE deleted")
            else:
                print("error :", table, "TABLE didn't deleted")
    """cur.execute("DROP TABLE ranking")
    cur.execute("DROP TABLE data")
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='ranking'")
    print("ranking table deleted :", cur.fetchone()[0] == 0)
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='data'")
    print("data table deleted :", cur.fetchone()[0] == 0)
    """
    conn.commit()
    conn.close()
else:
    # このプログラムがimportなどで別ファイルから実行されたとき

    # rankingテーブル
    create_table('ranking', ['id INTEGER PRIMARY KEY', 'stage INTEGER', 'score INTEGER'])
    # dataテーブル
    create_table('data', ['key TEXT', 'value TEXT'])
    # gunテーブル
    create_table('gun', ['id INTEGER', 'name TEXT', 'bullet_size INTEGER', 'reload_size INTEGER', 'own INTEGER'])
    # equipmentテーブル
    create_table('equipment', ['id INTEGER PRIMARY KEY', 'gun1 INTEGER', 'gun2 INTEGER', 'gun3 INTEGER'])
    # chipsテーブル
    create_table('chips', ['id INTEGER PRIMARY KEY', 'chip1 INTEGER', 'chip2 INTEGER', 'chip3 INTEGER', \
                 'chip4 INTEGER', 'chip5 INTEGER', 'chip6 INTEGER'])
    # own_chipテーブル
    create_table('own_chip', ['id INTEGER', 'num INTEGER'])
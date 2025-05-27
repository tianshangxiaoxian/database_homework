from flask import Flask, render_template, request, redirect, session
import mysql.connector
from config import db_config

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 可自定义任意字符串

# 数据库连接函数
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 首页 => 登录页
@app.route('/')
def home():
    return render_template('login.html')

# 登录处理
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor()

    # 一个 user 表
    cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    
    cursor.close()
    conn.close()

    if user:
        session['username'] = username
        return redirect('/index')
    else:
        return "登录失败，请检查用户名或密码。"

# 主页面
@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect('/')

@app.route('/competition')
def competition():
    if 'username' not in session:
        return redirect('/')
    
    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM Competition")
    total = cursor.fetchone()['total']
    total_pages = (total + per_page - 1) // per_page

    cursor.execute("SELECT * FROM Competition LIMIT %s OFFSET %s", (per_page, offset))
    competitions = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('competition.html', competitions=competitions, page=page, total_pages=total_pages)

@app.route('/add_competition', methods=['POST'])
def add_competition():
    if 'username' not in session:
        return redirect('/')

    competition_ID = request.form['competition_ID']
    place = request.form['place']
    winner = request.form['winner']
    time = request.form['time']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Competition (`competition_ID`, `place`, `winner`, `time`) VALUES (%s, %s, %s, %s)",
        (competition_ID, place, winner, time)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/competition')

@app.route('/delete_competition/<int:competition_ID>')
def delete_competition(competition_ID):
    if 'username' not in session:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Competition WHERE competition_ID = %s", (competition_ID,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/competition')

@app.route('/edit_competition/<competition_ID>')
def edit_competition(competition_ID):
    if 'username' not in session:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Competition WHERE competition_ID = %s", (competition_ID,))
    comp = cursor.fetchone()
    cursor.close()
    conn.close()

    if comp:
        return render_template('edit_competition.html', comp=comp)
    else:
        return "未找到该比赛记录", 404

@app.route('/update_competition', methods=['POST'])
def update_competition():
    if 'username' not in session:
        return redirect('/')

    original_id = request.form['original_id']
    competition_ID = request.form['competition_ID']
    place = request.form['place']
    winner = request.form['winner']
    time = request.form['time']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE Competition
        SET competition_ID = %s, place = %s, winner = %s, time = %s
        WHERE competition_ID = %s
    """, (competition_ID, place, winner, time, original_id))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/competition')

@app.route('/gamer')
def gamer():
    if 'username' not in session:
        return redirect('/')

    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM Gamer")
    total = cursor.fetchone()['total']
    total_pages = (total + per_page - 1) // per_page

    cursor.execute("SELECT * FROM Gamer LIMIT %s OFFSET %s", (per_page, offset))
    gamers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('gamer.html', gamers=gamers, page=page, total_pages=total_pages)

@app.route('/add_gamer', methods=['POST'])
def add_gamer():
    if 'username' not in session:
        return redirect('/')

    gamer_ID = request.form['gamer_ID']
    gamer_name = request.form['gamer_name']
    club_name = request.form['club_name']
    gamer_location = request.form['gamer_location']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Gamer ( gamer_name,gamer_ID, club_name, gamer_location) VALUES (%s, %s, %s, %s)",
        (gamer_name, gamer_ID, club_name, gamer_location)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/gamer')

@app.route('/delete_gamer/<int:gamer_ID>')
def delete_gamer(gamer_name):
    if 'username' not in session:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Gamer WHERE gamer_name = %s", (gamer_name,))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/gamer')

@app.route('/grade')
def grade():
    if 'username' not in session:
        return redirect('/')

    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM Grade")
    total = cursor.fetchone()['total']
    total_pages = (total + per_page - 1) // per_page

    cursor.execute("SELECT * FROM Grade LIMIT %s OFFSET %s", (per_page, offset))
    grades = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('grade.html', grades=grades, page=page, total_pages=total_pages)

@app.route('/add_grade', methods=['POST'])
def add_grade():
    if 'username' not in session:
        return redirect('/')

    club_name = request.form['club_name']
    competition = request.form['competition']
    award = request.form['award']
    bonus = request.form['bonus']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Grade (club_name, competition, award, bonus) VALUES (%s, %s, %s, %s)",
        (club_name, competition, award, bonus)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/grade')

@app.route('/delete_grade')
def delete_grade():
    if 'username' not in session:
        return redirect('/')

    competition = request.args.get('competition')
    award = request.args.get('award')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Grade WHERE competition = %s AND award = %s", (competition, award))
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/grade')

@app.route('/club')
def club():
    if 'username' not in session:
        return redirect('/')

    page = int(request.args.get('page', 1))
    per_page = 5
    offset = (page - 1) * per_page

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM Club")
    total = cursor.fetchone()['total']
    total_pages = (total + per_page - 1) // per_page

    cursor.execute("SELECT * FROM Club LIMIT %s OFFSET %s", (per_page, offset))
    clubs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('club.html', clubs=clubs, page=page, total_pages=total_pages)

@app.route('/add_club', methods=['POST'])
def add_club():
    if 'username' not in session:
        return redirect('/')

    club_name = request.form['club_name']
    coach = request.form['coach']
    club_location = request.form['club_location']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Club (club_name, coach, club_location) VALUES (%s, %s, %s)",
        (club_name, coach, club_location)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/club')

@app.route('/delete_club/<club_name>')
def delete_club(club_name):
    if 'username' not in session:
        return redirect('/')
    # conn = get_db_connection()
    # cursor = conn.cursor()
    # try:
    #     # 开始事务
    #     conn.start_transaction()

    #     # 删除成员
    #     cursor.execute("DELETE FROM Gamer WHERE club_name = %s", (club_name,))
    #     # 删除俱乐部
    #     cursor.execute("DELETE FROM Club WHERE club_name = %s", (club_name,))

    #     # 提交事务
    #     conn.commit()
    #     flash("俱乐部及其成员删除成功", "success")
    # except Exception as e:
    #     conn.rollback()
    #     flash(f"删除失败，事务已回滚：{e}", "danger")
    # finally:
    #     cursor.close()
    #     conn.close()

    # return redirect('/club')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Club WHERE club_name = %s", (club_name,))
    
    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/club')

@app.route('/edit_club/<club_name>')
def edit_club(club_name):
    if 'username' not in session:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Club WHERE club_name = %s", (club_name,))
    club = cursor.fetchone()
    cursor.close()
    conn.close()

    if club:
        return render_template('edit_club.html', club=club)
    else:
        return "未找到该俱乐部信息", 404
    
@app.route('/update_club', methods=['POST'])
def update_club():
    if 'username' not in session:
        return redirect('/')

    original_name = request.form['original_name']
    new_name = request.form['club_name']
    new_coach = request.form['coach']
    new_location = request.form['club_location']

    conn = get_db_connection()
    cursor = conn.cursor()

    # 调用定义的存储过程
    cursor.callproc('update_club_info_only', (original_name, new_name, new_coach, new_location))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect('/club')

@app.route('/view')
def view_joined_data():
    if 'username' not in session:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Competition_Club_View")
    joined_data = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('view.html', data=joined_data)

if __name__ == '__main__':
    app.run(debug=True)

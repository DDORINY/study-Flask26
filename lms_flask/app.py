from flask import Flask, render_template, request, redirect, url_for, session, flash

from domain import Member
from service.MemberService import MemberService

app = Flask(__name__)
app.secret_key = "lms_flask_MBC320!"

# --------------------------------------------
# MAIN
@app.route('/')
def index():
    return render_template("main.html")

# --------------------------------------------
# MEMBER
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('member/login.html')  # 실제 위치에 맞게 조정

    uid = request.form.get('uid', '').strip()
    pw = request.form.get('pw', '').strip()

    if not uid or not pw:
        flash("아이디/비밀번호를 입력해주세요.")
        return redirect(url_for('login'))

    try:
        member = MemberService.login(uid, pw)
        session['user_id'] = member.id
        session['user_uid'] = member.uid
        session['user_name'] = member.name
        session['role'] = member.role
        flash("로그인되었습니다.")
        return redirect(url_for('index'))

    except ValueError as e:
        flash(f"로그인 오류: {e}")
        return redirect(url_for('login'))

    except Exception as e:
        flash(f"서버 오류: {e}")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    flash("로그아웃되었습니다.")
    return redirect(url_for('index'))


@app.route('/mypage')
def mypage():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    user_info, board_count = MemberService.my_page(
        uid=session['user_id']
    )
    return render_template(
        'member/mypage.html',
        user=user_info,
        board_count=board_count
    )




@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'GET':
        return render_template('member/join.html')  # 로그인화면용 프론트로 연결
    uid = request.form.get('uid', '').strip()
    pw = request.form.get('password', '').strip()
    name = request.form.get('name', '').strip()

    try:
        member = MemberService.join(uid, pw, name)

        session['user_id'] = member.id
        session['user_uid'] = member.uid
        session['user_name'] = member.name
        session['role'] = member.role

        flash("회원가입 + 자동 로그인 완료")
        return redirect(url_for("index"))

    except ValueError as e:
        flash(str(e))
        return redirect(url_for('index'))

    except Exception as e:
        print("회원가입 에러:", e)
        return "가입 중 오류가 발생했습니다. join 메서드를 확인하세요."

@app.route('/member/edit', methods=['GET', 'POST'])
def member_edit():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    if request.method == 'GET':
        uid = session['user_id']
        user_info, _ = MemberService.my_page(uid)
        return render_template('member/edit.html', user=user_info)

    uid = session['user_id']
    name = request.form.get('name', '').strip()
    pw = request.form.get('password', '').strip()

    try:
        MemberService.member_edit(uid,name,pw)

        session['user_name'] = name

        flash("회원정보가 수정되었습니다.")
        return redirect(url_for('mypage'))
    except ValueError as e:
        flash(str(e))
        return redirect(url_for('index'))

@app.route('/member/delete', methods=['POST'])
def member_delete():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    uid = session['user_id']
    pw = request.form.get('password', '').strip()

    try:
        MemberService.member_delete(uid,pw)
        session.clear()
        flash('회원탈퇴되었습니다.')
        return redirect(url_for('index'))

    except ValueError as e:
        flash(str(e))
        return redirect(url_for('member_edit'))





# --------------------------------------------
# BOARD
@app.route("/board")
def board_list():
    return "게시판 목록(임시)"
    # return render_template("board_list.html")

# --------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

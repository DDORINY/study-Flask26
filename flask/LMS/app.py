# pip install flask
# flask란?
# python으로 만든 DB연동 콘솔 프로그램을 웹으로 연결하는 프레임워크임
# 프레임워크 : 미리 만들어 놓은 틀 안에서 작업하는 공간
# app.py는 flask로 서버를 동작하기 위한 파일명 ( 기본파일 )
# static, templates 폴터 필수 (프론트용 파일 모이는 곳)
# static 정적 파일을 모아두는 곳  (HTMl, CSS, JS)
# templates : 동적파일을 모아놓음 (CRUD화면, 인덱스, 레이아웃 등)
from flask import Flask, render_template,request,redirect,url_for,session
from LMS.common import Session

#                 Flask  프론트 연결      요청에 응답 ,주소전달,주소생성,상태저장

app = Flask(__name__)
app.secret_key = "LMS_secret_key"
#세션을 사용하기 위한 보안 키 설정

@app.route('/login', methods=['GET', 'POST'])# http://localhost:5000/login
# methods는 웹에 도작에 관여한다.
# GET은 URL 주소로 데이터를 처리하여 (보안상 좋지 않지만 빠름)
# POST는 BODY영역에서 데이터를 처리(보안상 좋고 대용량에서 많이 사용함)
# 대부분 처음에 화면 (HTML렌더)을 요청할때는 GET방식으로 처리
# 화면에 있는 내용을 백엔드로 전달할때는 POST 방식으로 처리
def login():
    if request.method == 'GET': # 처음 접속하면 GET방식으로 화면이 출력된다.
        return render_template('login.html') # GET 방식으로 요청하면 'login.html'화면이 나온다.
    # login.html 에서 action ="/login" method = "POST"처리용 코드
    # login.html에서 넘어온 폼 데이터는 uid/upw
    uid = request.form.get('uid','').strip() # 요청한     폼내용을  가져온다.
    upw = request.form.get('upw','').strip() # request.  form.   get

    # print("/login에서 넘어온 폼 데이터 출력테스트")
    # print(uid,upw)
    # print("-"*50)

    conn =Session.get_connection() # 교사용 DB에 접속용 객체
    try : # 예외발생이 생길 수 있음
        with conn.cursor() as cursor: # DB에 cursor 객체 사용
            # 1. 회원정보 조회
            sql="select id,name,uid,role from members where uid = %s and password = %s "
            #                                               uid가 동일 & pw가 동일
            #           id,name,uid,role를 가져온다.
            cursor.execute(sql,(uid,upw))
            user = cursor.fetchone() # 쿼리 결과를 1개 가져온다.

            if user:
                # 찾은 계정이 있으면 브라우저 세션영역에 보관한다.
                session['user_id'] = user['id'] # 계정 일련번호(회원번호)
                session['user_name'] = user['name'] # 계정이름
                session['user_uid'] = user['uid'] # 계정의 ID
                session['user_role'] = user['role'] # 계정 권한
                # 세션에 저장완료
                # 브라우저에서 F12번을 누르고 애플리케이션 탭에서 쿠키항목에 가면 세션객체가 보인다.
                # 이것을 삭제하면 로그아웃 처리된다.
                return redirect(url_for('index'))
                # 처리 후 이동하는 경로 http://localhost:/index로 감 (get 메서드 방식)

            else :
                # 계정이 없다.
                return "<script>alert('아이디나 비번이 틀렸습니다.');history.back()</script>"
                # alert : 경고창                                  history.back(): 뒤로가기
    finally:
        conn.close()  #DB 연결 종료

@app.route('/logout') # 기본 동작이 GET 방식이라서 생략이 가능하다.
def logout():
    session.clear() #세션비우기
    return redirect(url_for('login')) # http://localhost:5000/login =GET메서드

@app.route('/join', methods=['GET', 'POST']) #회원가입용 함수
def join(): #http://localhost:5000/ get메서드(화면 출력) post메서드(화면폼처리용)
    if request.method == 'GET':
        return render_template('join.html') # 로그인화면용 프론트로 연결

    # POST 메서드인 경우/폼으로 데이터가 넘어온다.
    uid = request.form.get('uid','').strip()
    password = request.form.get('password','').strip()
    name =request.form.get('name','').strip() # 폼에서 넘어온 값을 변수에 넣음

    conn =Session.get_connection() #DB에 연결
    try: # 예외발생 가능성이 있는 코드
        with conn.cursor() as cursor:
            cursor.execute("select id from members where uid = %s" ,(uid,))
            if cursor.fetchone() :
               return  "<script>alert('이미 존재하는 아이디입니다.');history.back()</script>"

            sql="insert into members (uid,password,name) values (%s,%s,%s)"
            cursor.execute(sql,(uid,password,name))
            conn.commit()

            return "<script>alert('회원가입이 완료되었습니다.');location.href='/login';</script>"

    except Exception as e: #예외 발생 시 실행문
        print(f"회원가입 에러{e}")
        return "가입 중 오류가 발생했습니다./n join메서드를 확인하세요."

    finally: # 항상 실행문
        conn.close()

@app.route('/member/edit', methods=['GET', 'POST'])
def member_edit():
    if 'user_id' not in session: # 세션에 유저 아이디가 없으면 로그인경로로 보낸다
        return redirect(url_for('login'))

    # 있으면 DB연결 시작
    conn =Session.get_connection()
    try :
        with conn.cursor() as cursor:
            if request.method == 'GET':
                cursor.execute("select * from members where id = %s ",(session['user_id'],))
                user_info = cursor.fetchone()
                return render_template('member_edit.html',user=user_info)
                #                                        GET 요청시 페이지   객체 전달용 코드

            new_name = request.form.get('name', '').strip()
            new_pw = request.form.get('password', '').strip()

            if new_pw:
                sql = "UPDATE members SET name =%s, password = %s WHERE id = %s "
                cursor.execute(sql, (new_name, new_pw, session['user_id']))

            else:
                sql = "UPDATE members SET name = %s WHERE id = %s "
                cursor.execute(sql, (new_name, session['user_id']))

            conn.commit()
            session['user_name'] = new_name
            return "<script>alert('정보가 수정되었습니다.');location.href='/mypage';</script>"

    except Exception as e:
        print(f"회원수정 중 오류 발생{e}")
        return "수정 중 오류가 발생되었습니다.\n member_edit() 확인하세요"
    finally:
        conn.close()

@app.route('/mypage') #http://localhost:5000/mypage
def mypage():
    if 'user_id' not in session: # 로그인 상태가 아니라면 로그인으로 보낸다.
        return redirect(url_for('login')) #http://localhost:5000/login

    conn =Session.get_connection() #DB 연결
    try :
        with conn.cursor() as cursor:
            cursor.execute("select * from members where id = %s ",(session['user_id'],))
            # 로그인한 유저의 정보를 가지고 DB에서 찾아온다.
            user_info = cursor.fetchone() # 찾아온 값 1개를 ser_info에 담는다. (dict)

            cursor.execute("select count(*) as board_count from boards where id = %s ",(session['user_id'],))
            #                                                   boards 테이블 조건 member_id값을 가지고 찾아옴
            #                                  개수를 세어 fetchone()에 넣음 board_count 이름으로 개수를 가지고 있음
            board_count =cursor.fetchone()['board_count']

            return render_template('mypage.html',user=user_info,board_count=board_count)
            # 결과를 리턴한다.                         mypage.html에게 user 객체와 board_count 객체를 잠아보냄
            # 프론트에서 사용하려면 {{user.????}}  {{board_count}}
    finally:
        conn.close()



@app.route('/') #URL 생서용 코드 http://localhost:5000/
def index():
    return render_template('main.html')
    # render_template 웹브라우저로 보낼 파일명
    # template 라는 폴더에서 main.html을 찾아 보냄


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    # host='0.0.0.0' 누가요청하던 응답해라
    # port=5000 flask에서 사용하는 포트번호
    # debug=True 콘솔에 디버그를 보겠다.
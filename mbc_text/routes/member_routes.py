from flask import Blueprint, render_template, request, url_for, flash, session, redirect

from common.auth import Auth
from common.upload import save_profile_image
from repository.member_repo import MemberRepo
from service.member_service import MemberService


bp = Blueprint('member',__name__,url_prefix="/member")

@bp.route("/join", methods=["GET","POST"])
def join():
    if request.method == "GET":
        return render_template("member/join.html")

    try:
        profile_img = save_profile_image(request.files.get("profile_img"))
    except Exception:
        profile_img = None
        flash("프로필 이미지는 png/jpg/jpeg/webp만 가능합니다.", "warning")

    ok, msg = MemberService.join(request.form, profile_img)
    flash(msg, "success" if ok else "danger")
    return redirect(url_for("member.login")) if ok else redirect(url_for("member.join"))

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("member/login.html")

    uid = (request.form.get("uid") or "").strip()
    password = (request.form.get("password") or "").strip()

    insert,member,msg = MemberService.login(uid, password)
    if not insert:
        flash(msg,"danger")
        return redirect(url_for("member.login"))

    Auth.login(member)
    flash("로그인 되었습니다.", "success")
    return redirect(url_for("member.mypage"))

@bp.route("/logout")
def logout():
    Auth.logout()
    flash("로그아웃 되었습니다.")
    return redirect(url_for("main.index"))

@bp.route("/mypage")
def mypage():
    if not Auth.is_login():
        return redirect(url_for("member.login"))
    user =MemberRepo.find_by_id(session["user_id"])
    return render_template("member/mypage.html",user=user)

@bp.route("/edit", methods=["GET","POST"])
def edit():
    if not Auth.is_login():
        return redirect(url_for("member.login"))

    user = MemberRepo.find_by_id(session["user_id"])

    if request.method == "GET":
        return render_template("member/edit.html", user=user)

    try:
        profile_img = save_profile_image(request.files.get("profile_img"))
    except Exception:
        profile_img = None
        flash("프로필 이미지는 png/jpg/jpeg/webp만 가능합니다.", "warning")

    name = (request.form.get("name") or "").strip()
    phone = (request.form.get("phone") or "").strip()
    email = (request.form.get("email") or "").strip()
    address = (request.form.get("address") or "").strip()


    ok = MemberRepo.update(session["user_id"], name, phone,  email, address, profile_img)
    flash("수정 완료" if ok else "수정 실패", "success" if ok else "danger")
    return redirect(url_for("member.mypage"))

@bp.route("/withdraw", methods=["POST"])
def withdraw():
    if not Auth.is_login():
        return redirect(url_for("member.login"))
    ok = MemberRepo.delete(session["user_id"])
    Auth.logout()
    flash("탈퇴 처리되었습니다.", "success" if ok else "danger")
    return redirect(url_for("member.login"))
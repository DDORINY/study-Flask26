from flask import Blueprint, render_template, request, redirect, url_for, flash
from common.auth import Auth
from repository.member_repo import MemberRepo
from service.admin_service import AdminService

bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_guard():
    if not Auth.is_login() or not Auth.is_admin():
        flash("권한이 없습니다.","danger")
        return False
    return True

@bp.route('/dashboard')
def dashboard():
    #위 메서드가 돌아감 (로그아웃회원인 경우 로그인, 또는 권한없음 알림)
    if not admin_guard():
        return redirect(url_for('member.login'))
        #로그인 페이지로 이동한다.
    stats = AdminService.get_dashboard()
    return render_template("admin/dashboard.html", stats=stats)

@bp.route('/members')
def members():
    if not admin_guard():
        return redirect(url_for('member.login'))

    mode = request.args.get("mode","all")
    q = (request.args.get("q") or "").strip()

    active = None
    if mode == "active":active = 1
    if mode == "inactive":active = 0

    rows = MemberRepo.list_members(active=active,keyword=q)

    # 관리자 화면은 템플릿에 전달
    members = []
    for row in rows:
        members.append({
            "id": row["id"],
            "uid": row["uid"],
            "name": row["name"],
            "phone": row["phone"],
            "email": row["email"],
            "address": row["address"],
            "active": row["active"],
            "created_at": row["created_at"],
        })

    return render_template("admin/members_list.html", members=members, mode=mode, q=q)

@bp.route('/member/<int:member_id>')
def member_detail(member_id):
    if not admin_guard():
        return redirect(url_for('member.login'))

    row = MemberRepo.find_by_id(member_id)
    if not row:
        flash("회원이 존재하지 않습니다.","danger")
        return redirect(url_for("member.member"))

    m = {
        "id": row["id"],
        "uid": row["uid"],
        "name": row["name"],
        "phone": row["phone"],
        "email": row["email"],
        "address": row["address"],
        "active": row["active"],
        "created_at": row["created_at"],
    }
    return render_template("admin/member_detail.html", m=m)

@bp.route("/members/<int:member_id>/disable", methods=["POST"])
def member_disable(member_id):
    if not admin_guard():
        return redirect(url_for("member.login"))
    insert = MemberRepo.delete(member_id)
    flash("비활성 처리 완료" if insert else "처리 실패", "success" if insert else "danger")
    return redirect(url_for("admin.members"))


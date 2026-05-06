import os
import re
import uuid
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path

from dotenv import load_dotenv
from flask import (
    Flask, Response, abort, jsonify, render_template, request,
    send_from_directory, url_for,
)
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from werkzeug.utils import secure_filename

from models import (
    Contact, ContactSubmission, Experience, ExperienceBullet, HeroRole,
    PageView, Project, ProjectTag, SiteSetting, SkillCluster, SkillTag, Stat,
    db,
)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)
UPLOAD_DIR = BASE_DIR / "static" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_EXT = {"png", "jpg", "jpeg", "gif", "webp", "svg"}
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5MB

app = Flask(__name__, instance_path=str(INSTANCE_DIR))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-insecure-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{INSTANCE_DIR / 'portfolio.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES

db.init_app(app)

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")
TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # 7 days

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

PUBLIC_TRACKED_PREFIXES = ("/", "/blog", "/cv")


def serializer():
    return URLSafeTimedSerializer(app.config["SECRET_KEY"], salt="admin-auth")


def require_admin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "unauthorized"}), 401
        token = auth[7:]
        try:
            data = serializer().loads(token, max_age=TOKEN_MAX_AGE)
        except SignatureExpired:
            return jsonify({"error": "expired"}), 401
        except BadSignature:
            return jsonify({"error": "invalid"}), 401
        if data.get("role") != "admin":
            return jsonify({"error": "forbidden"}), 403
        return fn(*args, **kwargs)
    return wrapper


# ---------- pages ----------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/admin")
def admin_page():
    return render_template("admin.html")


# ---------- auth ----------

@app.post("/api/login")
def login():
    payload = request.get_json(silent=True) or {}
    if payload.get("password") != ADMIN_PASSWORD:
        return jsonify({"error": "bad password"}), 401
    token = serializer().dumps({"role": "admin"})
    return jsonify({"token": token})


# ---------- site settings (key/value) ----------

@app.get("/api/site")
def get_site():
    rows = SiteSetting.query.all()
    return jsonify({r.key: r.value for r in rows})


@app.patch("/api/site")
@require_admin
def patch_site():
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        return jsonify({"error": "expected object"}), 400
    for key, value in payload.items():
        row = SiteSetting.query.get(key)
        if row is None:
            row = SiteSetting(key=key, value=str(value or ""))
            db.session.add(row)
        else:
            row.value = str(value or "")
    db.session.commit()
    return jsonify({"ok": True})


# ---------- generic CRUD helpers ----------

def _apply(obj, payload, fields):
    for f in fields:
        if f in payload:
            setattr(obj, f, payload[f])


def _list(model, order_by="order"):
    rows = model.query.order_by(getattr(model, order_by).asc(), model.id.asc()).all()
    return jsonify([r.to_dict() for r in rows])


# ---------- stats ----------

STAT_FIELDS = ("num", "label", "color", "order")


@app.get("/api/stats")
def stats_list():
    return _list(Stat)


@app.post("/api/stats")
@require_admin
def stats_create():
    p = request.get_json(silent=True) or {}
    s = Stat(num=p.get("num", ""), label=p.get("label", ""),
             color=p.get("color", ""), order=p.get("order", 0))
    db.session.add(s)
    db.session.commit()
    return jsonify(s.to_dict()), 201


@app.patch("/api/stats/<int:item_id>")
@require_admin
def stats_update(item_id):
    s = Stat.query.get_or_404(item_id)
    _apply(s, request.get_json(silent=True) or {}, STAT_FIELDS)
    db.session.commit()
    return jsonify(s.to_dict())


@app.delete("/api/stats/<int:item_id>")
@require_admin
def stats_delete(item_id):
    s = Stat.query.get_or_404(item_id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"ok": True})


# ---------- contacts ----------

CONTACT_FIELDS = ("kind", "label", "value", "url", "icon", "order")


@app.get("/api/contacts")
def contacts_list():
    return _list(Contact)


@app.post("/api/contacts")
@require_admin
def contacts_create():
    p = request.get_json(silent=True) or {}
    c = Contact(kind=p.get("kind", "other"), label=p.get("label", ""),
                value=p.get("value", ""), url=p.get("url", ""),
                icon=p.get("icon", "mail"), order=p.get("order", 0))
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201


@app.patch("/api/contacts/<int:item_id>")
@require_admin
def contacts_update(item_id):
    c = Contact.query.get_or_404(item_id)
    _apply(c, request.get_json(silent=True) or {}, CONTACT_FIELDS)
    db.session.commit()
    return jsonify(c.to_dict())


@app.delete("/api/contacts/<int:item_id>")
@require_admin
def contacts_delete(item_id):
    c = Contact.query.get_or_404(item_id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"ok": True})


# ---------- skill clusters + tags ----------

CLUSTER_FIELDS = ("kicker", "title", "title_ru", "icon", "accent", "order")
SKILL_TAG_FIELDS = ("name", "order")


@app.get("/api/skill-clusters")
def clusters_list():
    rows = SkillCluster.query.order_by(SkillCluster.order.asc(),
                                       SkillCluster.id.asc()).all()
    return jsonify([r.to_dict() for r in rows])


@app.post("/api/skill-clusters")
@require_admin
def clusters_create():
    p = request.get_json(silent=True) or {}
    c = SkillCluster(kicker=p.get("kicker", ""), title=p.get("title", "Cluster"),
                     icon=p.get("icon", "code-2"))
    _apply(c, p, CLUSTER_FIELDS)
    db.session.add(c)
    db.session.commit()
    return jsonify(c.to_dict()), 201


@app.patch("/api/skill-clusters/<int:item_id>")
@require_admin
def clusters_update(item_id):
    c = SkillCluster.query.get_or_404(item_id)
    _apply(c, request.get_json(silent=True) or {}, CLUSTER_FIELDS)
    db.session.commit()
    return jsonify(c.to_dict())


@app.delete("/api/skill-clusters/<int:item_id>")
@require_admin
def clusters_delete(item_id):
    c = SkillCluster.query.get_or_404(item_id)
    db.session.delete(c)
    db.session.commit()
    return jsonify({"ok": True})


@app.post("/api/skill-clusters/<int:cluster_id>/tags")
@require_admin
def skill_tag_create(cluster_id):
    SkillCluster.query.get_or_404(cluster_id)
    p = request.get_json(silent=True) or {}
    t = SkillTag(cluster_id=cluster_id, name=p.get("name", ""),
                 order=p.get("order", 0))
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@app.patch("/api/skill-tags/<int:item_id>")
@require_admin
def skill_tag_update(item_id):
    t = SkillTag.query.get_or_404(item_id)
    _apply(t, request.get_json(silent=True) or {}, SKILL_TAG_FIELDS)
    db.session.commit()
    return jsonify(t.to_dict())


@app.delete("/api/skill-tags/<int:item_id>")
@require_admin
def skill_tag_delete(item_id):
    t = SkillTag.query.get_or_404(item_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"ok": True})


# ---------- projects + tags ----------

PROJECT_FIELDS = ("num", "title", "title_ru", "description", "description_ru",
                  "cover_image", "code_url", "live_url", "order")
PROJECT_TAG_FIELDS = ("name", "order")


@app.get("/api/projects")
def projects_list():
    rows = Project.query.order_by(Project.order.asc(), Project.id.asc()).all()
    return jsonify([r.to_dict() for r in rows])


@app.post("/api/projects")
@require_admin
def projects_create():
    p = request.get_json(silent=True) or {}
    pr = Project(title=p.get("title", "Untitled"))
    _apply(pr, p, PROJECT_FIELDS)
    db.session.add(pr)
    db.session.commit()
    return jsonify(pr.to_dict()), 201


@app.patch("/api/projects/<int:item_id>")
@require_admin
def projects_update(item_id):
    pr = Project.query.get_or_404(item_id)
    _apply(pr, request.get_json(silent=True) or {}, PROJECT_FIELDS)
    db.session.commit()
    return jsonify(pr.to_dict())


@app.delete("/api/projects/<int:item_id>")
@require_admin
def projects_delete(item_id):
    pr = Project.query.get_or_404(item_id)
    db.session.delete(pr)
    db.session.commit()
    return jsonify({"ok": True})


@app.post("/api/projects/<int:project_id>/tags")
@require_admin
def project_tag_create(project_id):
    Project.query.get_or_404(project_id)
    p = request.get_json(silent=True) or {}
    t = ProjectTag(project_id=project_id, name=p.get("name", ""),
                   order=p.get("order", 0))
    db.session.add(t)
    db.session.commit()
    return jsonify(t.to_dict()), 201


@app.patch("/api/project-tags/<int:item_id>")
@require_admin
def project_tag_update(item_id):
    t = ProjectTag.query.get_or_404(item_id)
    _apply(t, request.get_json(silent=True) or {}, PROJECT_TAG_FIELDS)
    db.session.commit()
    return jsonify(t.to_dict())


@app.delete("/api/project-tags/<int:item_id>")
@require_admin
def project_tag_delete(item_id):
    t = ProjectTag.query.get_or_404(item_id)
    db.session.delete(t)
    db.session.commit()
    return jsonify({"ok": True})


# ---------- experience + bullets ----------

EXP_FIELDS = ("period", "role", "role_ru", "company", "company_meta",
              "company_meta_ru", "order")
BULLET_FIELDS = ("text", "text_ru", "order")


@app.get("/api/experience")
def experience_list():
    rows = Experience.query.order_by(Experience.order.asc(),
                                     Experience.id.asc()).all()
    return jsonify([r.to_dict() for r in rows])


@app.post("/api/experience")
@require_admin
def experience_create():
    p = request.get_json(silent=True) or {}
    e = Experience(period=p.get("period", ""), role=p.get("role", "Role"),
                   company=p.get("company", "Company"))
    _apply(e, p, EXP_FIELDS)
    db.session.add(e)
    db.session.commit()
    return jsonify(e.to_dict()), 201


@app.patch("/api/experience/<int:item_id>")
@require_admin
def experience_update(item_id):
    e = Experience.query.get_or_404(item_id)
    _apply(e, request.get_json(silent=True) or {}, EXP_FIELDS)
    db.session.commit()
    return jsonify(e.to_dict())


@app.delete("/api/experience/<int:item_id>")
@require_admin
def experience_delete(item_id):
    e = Experience.query.get_or_404(item_id)
    db.session.delete(e)
    db.session.commit()
    return jsonify({"ok": True})


@app.post("/api/experience/<int:exp_id>/bullets")
@require_admin
def bullet_create(exp_id):
    Experience.query.get_or_404(exp_id)
    p = request.get_json(silent=True) or {}
    b = ExperienceBullet(experience_id=exp_id, text=p.get("text", ""))
    _apply(b, p, BULLET_FIELDS)
    db.session.add(b)
    db.session.commit()
    return jsonify(b.to_dict()), 201


@app.patch("/api/experience-bullets/<int:item_id>")
@require_admin
def bullet_update(item_id):
    b = ExperienceBullet.query.get_or_404(item_id)
    _apply(b, request.get_json(silent=True) or {}, BULLET_FIELDS)
    db.session.commit()
    return jsonify(b.to_dict())


@app.delete("/api/experience-bullets/<int:item_id>")
@require_admin
def bullet_delete(item_id):
    b = ExperienceBullet.query.get_or_404(item_id)
    db.session.delete(b)
    db.session.commit()
    return jsonify({"ok": True})


# ---------- hero roles ----------

ROLE_FIELDS = ("text", "text_ru", "order")


@app.get("/api/hero-roles")
def hero_roles_list():
    rows = HeroRole.query.order_by(HeroRole.order.asc(), HeroRole.id.asc()).all()
    return jsonify([r.to_dict() for r in rows])


@app.post("/api/hero-roles")
@require_admin
def hero_roles_create():
    p = request.get_json(silent=True) or {}
    r = HeroRole(text=p.get("text", "Role"))
    _apply(r, p, ROLE_FIELDS)
    db.session.add(r)
    db.session.commit()
    return jsonify(r.to_dict()), 201


@app.patch("/api/hero-roles/<int:item_id>")
@require_admin
def hero_roles_update(item_id):
    r = HeroRole.query.get_or_404(item_id)
    _apply(r, request.get_json(silent=True) or {}, ROLE_FIELDS)
    db.session.commit()
    return jsonify(r.to_dict())


@app.delete("/api/hero-roles/<int:item_id>")
@require_admin
def hero_roles_delete(item_id):
    r = HeroRole.query.get_or_404(item_id)
    db.session.delete(r)
    db.session.commit()
    return jsonify({"ok": True})


# ---------- file uploads ----------

@app.post("/api/upload")
@require_admin
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "empty filename"}), 400
    ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else ""
    if ext not in ALLOWED_IMAGE_EXT:
        return jsonify({"error": f"extension .{ext} not allowed"}), 400
    safe = secure_filename(f.filename)
    name = f"{uuid.uuid4().hex[:12]}_{safe}"
    path = UPLOAD_DIR / name
    f.save(path)
    url = url_for("static", filename=f"uploads/{name}")
    return jsonify({"url": url, "name": name}), 201


# ---------- contact form (public) ----------

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _send_telegram(name, email, message):
    if not (TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID):
        return
    try:
        import urllib.request, urllib.parse
        text_msg = f"📬 New contact\n\nFrom: {name} <{email}>\n\n{message}"
        data = urllib.parse.urlencode({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text_msg,
        }).encode()
        urllib.request.urlopen(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data=data, timeout=5,
        )
    except Exception as e:
        app.logger.warning("telegram notify failed: %s", e)


@app.post("/api/contact-form")
def contact_form_submit():
    p = request.get_json(silent=True) or {}
    name = (p.get("name") or "").strip()[:120]
    email = (p.get("email") or "").strip()[:200]
    message = (p.get("message") or "").strip()[:5000]
    if not name or not message or not EMAIL_RE.match(email):
        return jsonify({"error": "invalid input"}), 400
    sub = ContactSubmission(name=name, email=email, message=message,
                            ip=request.headers.get("X-Forwarded-For",
                                                   request.remote_addr or ""))
    db.session.add(sub)
    db.session.commit()
    _send_telegram(name, email, message)
    return jsonify({"ok": True})


@app.get("/api/contact-submissions")
@require_admin
def contact_submissions_list():
    rows = ContactSubmission.query.order_by(
        ContactSubmission.created_at.desc()).limit(200).all()
    return jsonify([r.to_dict() for r in rows])


@app.patch("/api/contact-submissions/<int:item_id>")
@require_admin
def contact_submissions_update(item_id):
    s = ContactSubmission.query.get_or_404(item_id)
    p = request.get_json(silent=True) or {}
    if "read" in p:
        s.read = bool(p["read"])
    db.session.commit()
    return jsonify(s.to_dict())


@app.delete("/api/contact-submissions/<int:item_id>")
@require_admin
def contact_submissions_delete(item_id):
    s = ContactSubmission.query.get_or_404(item_id)
    db.session.delete(s)
    db.session.commit()
    return jsonify({"ok": True})


# ---------- analytics ----------

@app.before_request
def _track_view():
    p = request.path
    if request.method != "GET":
        return
    if p.startswith("/static") or p.startswith("/api"):
        return
    if p == "/admin" or p.startswith("/admin/"):
        return
    day = datetime.utcnow().strftime("%Y-%m-%d")
    try:
        row = PageView.query.filter_by(path=p, day=day).first()
        if row is None:
            row = PageView(path=p, day=day, count=1)
            db.session.add(row)
        else:
            row.count = (row.count or 0) + 1
        db.session.commit()
    except Exception:
        db.session.rollback()


@app.get("/api/analytics")
@require_admin
def analytics_overview():
    days = int(request.args.get("days", "30"))
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    rows = PageView.query.filter(PageView.day >= cutoff).all()
    by_day = {}
    by_path = {}
    for r in rows:
        by_day[r.day] = by_day.get(r.day, 0) + (r.count or 0)
        by_path[r.path] = by_path.get(r.path, 0) + (r.count or 0)
    return jsonify({
        "days": sorted(by_day.items()),
        "paths": sorted(by_path.items(), key=lambda x: -x[1]),
        "total": sum(by_day.values()),
    })


# ---------- /cv (printable HTML resume) ----------

@app.get("/cv")
def cv_page():
    site = {r.key: r.value for r in SiteSetting.query.all()}
    experience = Experience.query.order_by(Experience.order).all()
    clusters = SkillCluster.query.order_by(SkillCluster.order).all()
    contacts = Contact.query.order_by(Contact.order).all()
    return render_template("cv.html", site=site, experience=experience,
                           clusters=clusters, contacts=contacts)


# ---------- robots.txt + sitemap.xml ----------

@app.get("/robots.txt")
def robots():
    body = "User-agent: *\nDisallow: /admin\nDisallow: /api/\n" \
           f"Sitemap: {request.url_root.rstrip('/')}/sitemap.xml\n"
    return Response(body, mimetype="text/plain")


@app.get("/sitemap.xml")
def sitemap():
    base = request.url_root.rstrip("/")
    urls = [f"{base}/", f"{base}/cv"]
    today = datetime.utcnow().strftime("%Y-%m-%d")
    items = "".join(
        f"<url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls
    )
    body = (f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f'{items}</urlset>')
    return Response(body, mimetype="application/xml")


# ---------- bootstrap ----------

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("DB initialized at", app.config["SQLALCHEMY_DATABASE_URI"])


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="127.0.0.1", port=5000)

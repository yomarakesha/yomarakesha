import os
from functools import wraps
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from models import (
    Contact, Experience, ExperienceBullet, Project, ProjectTag, SiteSetting,
    SkillCluster, SkillTag, Stat, db,
)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(exist_ok=True)

app = Flask(__name__, instance_path=str(INSTANCE_DIR))
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-insecure-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{INSTANCE_DIR / 'portfolio.db'}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")
TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # 7 days


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

CLUSTER_FIELDS = ("kicker", "title", "icon", "accent", "order")
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
    c = SkillCluster(kicker=p.get("kicker", ""), title=p.get("title", ""),
                     icon=p.get("icon", "code-2"), accent=p.get("accent", ""),
                     order=p.get("order", 0))
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

PROJECT_FIELDS = ("num", "title", "description", "code_url", "live_url", "order")
PROJECT_TAG_FIELDS = ("name", "order")


@app.get("/api/projects")
def projects_list():
    rows = Project.query.order_by(Project.order.asc(), Project.id.asc()).all()
    return jsonify([r.to_dict() for r in rows])


@app.post("/api/projects")
@require_admin
def projects_create():
    p = request.get_json(silent=True) or {}
    pr = Project(num=p.get("num", ""), title=p.get("title", ""),
                 description=p.get("description", ""),
                 code_url=p.get("code_url", ""), live_url=p.get("live_url", ""),
                 order=p.get("order", 0))
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

EXP_FIELDS = ("period", "role", "company", "company_meta", "order")
BULLET_FIELDS = ("text", "order")


@app.get("/api/experience")
def experience_list():
    rows = Experience.query.order_by(Experience.order.asc(),
                                     Experience.id.asc()).all()
    return jsonify([r.to_dict() for r in rows])


@app.post("/api/experience")
@require_admin
def experience_create():
    p = request.get_json(silent=True) or {}
    e = Experience(period=p.get("period", ""), role=p.get("role", ""),
                   company=p.get("company", ""),
                   company_meta=p.get("company_meta", ""),
                   order=p.get("order", 0))
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
    b = ExperienceBullet(experience_id=exp_id, text=p.get("text", ""),
                         order=p.get("order", 0))
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


# ---------- bootstrap ----------

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("DB initialized at", app.config["SQLALCHEMY_DATABASE_URI"])


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="127.0.0.1", port=5000)

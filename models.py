from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SiteSetting(db.Model):
    __tablename__ = "site_setting"
    key = db.Column(db.String(80), primary_key=True)
    value = db.Column(db.Text, nullable=False, default="")

    def to_dict(self):
        return {"key": self.key, "value": self.value}


class Stat(db.Model):
    __tablename__ = "stat"
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.String(40), nullable=False)
    label = db.Column(db.String(200), nullable=False)
    color = db.Column(db.String(20), default="")
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, "num": self.num, "label": self.label,
                "color": self.color, "order": self.order}


class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(40), nullable=False)
    label = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(200), nullable=False)
    url = db.Column(db.String(400), default="")
    icon = db.Column(db.String(40), default="mail")
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {"id": self.id, "kind": self.kind, "label": self.label,
                "value": self.value, "url": self.url, "icon": self.icon,
                "order": self.order}


class SkillCluster(db.Model):
    __tablename__ = "skill_cluster"
    id = db.Column(db.Integer, primary_key=True)
    kicker = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    icon = db.Column(db.String(40), default="code-2")
    accent = db.Column(db.String(20), default="")
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship("SkillTag", backref="cluster",
                           cascade="all, delete-orphan",
                           order_by="SkillTag.order")

    def to_dict(self):
        return {"id": self.id, "kicker": self.kicker, "title": self.title,
                "icon": self.icon, "accent": self.accent, "order": self.order,
                "tags": [t.to_dict() for t in self.tags]}


class SkillTag(db.Model):
    __tablename__ = "skill_tag"
    id = db.Column(db.Integer, primary_key=True)
    cluster_id = db.Column(db.Integer,
                           db.ForeignKey("skill_cluster.id", ondelete="CASCADE"),
                           nullable=False)
    name = db.Column(db.String(60), nullable=False)
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {"id": self.id, "cluster_id": self.cluster_id,
                "name": self.name, "order": self.order}


class Project(db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.String(10), default="")
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, default="")
    code_url = db.Column(db.String(400), default="")
    live_url = db.Column(db.String(400), default="")
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tags = db.relationship("ProjectTag", backref="project",
                           cascade="all, delete-orphan",
                           order_by="ProjectTag.order")

    def to_dict(self):
        return {"id": self.id, "num": self.num, "title": self.title,
                "description": self.description, "code_url": self.code_url,
                "live_url": self.live_url, "order": self.order,
                "tags": [t.to_dict() for t in self.tags]}


class ProjectTag(db.Model):
    __tablename__ = "project_tag"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer,
                           db.ForeignKey("project.id", ondelete="CASCADE"),
                           nullable=False)
    name = db.Column(db.String(60), nullable=False)
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {"id": self.id, "project_id": self.project_id,
                "name": self.name, "order": self.order}


class Experience(db.Model):
    __tablename__ = "experience"
    id = db.Column(db.Integer, primary_key=True)
    period = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(120), nullable=False)
    company_meta = db.Column(db.String(200), default="")
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bullets = db.relationship("ExperienceBullet", backref="experience",
                              cascade="all, delete-orphan",
                              order_by="ExperienceBullet.order")

    def to_dict(self):
        return {"id": self.id, "period": self.period, "role": self.role,
                "company": self.company, "company_meta": self.company_meta,
                "order": self.order,
                "bullets": [b.to_dict() for b in self.bullets]}


class ExperienceBullet(db.Model):
    __tablename__ = "experience_bullet"
    id = db.Column(db.Integer, primary_key=True)
    experience_id = db.Column(db.Integer,
                              db.ForeignKey("experience.id", ondelete="CASCADE"),
                              nullable=False)
    text = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {"id": self.id, "experience_id": self.experience_id,
                "text": self.text, "order": self.order}

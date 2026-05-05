"""Populate the DB with the same content the original static index.html had."""
from app import app
from models import (
    Contact, Experience, ExperienceBullet, Project, ProjectTag, SiteSetting,
    SkillCluster, SkillTag, Stat, db,
)


SITE = {
    "hero_badge": "Available for select work · Ashgabat 🇹🇲",
    "hero_title_prefix": "Hi, I'm",
    "hero_name": "Rustem Nuryev",
    "hero_desc_en": "4 years building reliable systems and stress-testing them. "
                    "Backend, networks, infrastructure — and a healthy obsession with security.",
    "hero_desc_ru": "4 года строю надёжные системы и проверяю их на прочность. "
                    "Бэкенд, сети, инфраструктура — и здоровая одержимость безопасностью.",
    "hero_meta_location": "Ashgabat, TM",
    "hero_meta_exp": "4+ yrs",
    "hero_meta_stack": "Python · Node · Linux",
    "about_title_html": "Engineer at the boundary of <span style=\"color:var(--cyan)\">code</span> "
                        "and <span style=\"color:var(--purple)\">security</span>.",
    "about_p1": "I'm <strong>Rustem Nuryev</strong> — a backend & infrastructure engineer from "
                "<span class=\"accent\">Ashgabat, Turkmenistan</span>. For the last four years I've been "
                "building APIs, wiring up networks, automating deployments, and occasionally taking a "
                "flashlight to systems to find what shouldn't be there.",
    "about_p2": "What I love about IT is the <strong>full stack of reality</strong> behind every feature: "
                "the kernel, the packets on the wire, the firewall rules, the database query plan, the CI "
                "pipeline, and the CVE that ruined someone's weekend. I like understanding all of it, "
                "not just the framework on top.",
    "about_p3": "My approach is simple: <strong>security-first, automate everything, write code you can "
                "read at 3 AM</strong>. I prefer boring, observable systems over clever ones. I write a "
                "lot of Bash, sometimes more than I should. I read RFCs for fun and audit my own code "
                "like a stranger wrote it.",
    "about_p4": "Right now I'm <span class=\"accent\">open to interesting work</span> — backend, network "
                "engineering, DevOps, or offensive/defensive security roles. If you have a system that "
                "needs to be built — or one you're worried about — let's talk.",
    "section_about_sub": "A short story of who I am, how I work, and what kinds of problems get me "
                         "out of bed.",
    "section_skills_sub": "Five clusters I rotate through depending on what's on fire that day.",
    "section_projects_sub": "A small slice of what I've shipped — APIs, infra, security tools, side projects.",
    "section_experience_sub": "A reverse-chronological log of where I've spent my keystrokes.",
    "section_contact_sub": "Best for: backend, network or DevOps work, security audits, or just a good "
                           "technical conversation.",
    "footer_copy": "© 2026 Yomarakesha · Rustem Nuryev",
}

STATS = [
    ("4+", "years in IT", ""),
    ("20+", "projects shipped", ""),
    ("15+", "technologies in stack", ""),
    ("∞", "cups of coffee", ""),
    ("0", "production fires this month", "lime"),
]

CONTACTS = [
    ("email", "email", "hello@yomarakesha.dev",
     "mailto:hello@yomarakesha.dev", "mail"),
    ("github", "github", "github.com/yomarakesha",
     "https://github.com/yomarakesha", "github"),
    ("linkedin", "linkedin", "linkedin.com/in/rustem-nuryev",
     "https://www.linkedin.com/in/rustem-nuryev", "linkedin"),
    ("telegram", "telegram", "@yomarakesha",
     "https://t.me/yomarakesha", "send"),
]

CLUSTERS = [
    ("// 01", "Languages & Backend", "code-2", "",
     ["Python", "FastAPI", "Django", "Flask", "Node.js",
      "Express", "NestJS", "Bash", "Shell"]),
    ("// 02", "Network Engineering", "network", "accent-purple",
     ["TCP/IP", "BGP", "OSPF", "VLAN", "VPN", "Cisco", "MikroTik",
      "Juniper", "Firewalls", "Load Balancers", "DNS"]),
    ("// 03", "DevOps & Infrastructure", "server-cog", "accent-lime",
     ["Docker", "Kubernetes", "GitHub Actions", "GitLab CI", "Jenkins",
      "Git", "Linux", "Ubuntu", "Debian", "Arch", "Terraform", "Ansible"]),
    ("// 04", "Cybersecurity & DevSecOps", "shield-check", "accent-purple",
     ["Pentesting", "Burp Suite", "Metasploit", "Nmap", "Splunk", "ELK",
      "Wazuh", "OSINT", "Threat Intel", "Code audit", "DevSecOps"]),
    ("// 05", "Data & Other", "database", "",
     ["PostgreSQL", "MongoDB", "Redis", "REST", "GraphQL",
      "WebSockets", "Linux", "Windows Server"]),
]

PROJECTS = [
    ("// 01", "[PROJECT_1]",
     "Short 2–3 line description: what it does, who it's for, what was hard about it. "
     "Replace this placeholder with a real project.",
     "#", "#",
     ["Python", "FastAPI", "PostgreSQL", "Docker"]),
    ("// 02", "[PROJECT_2]",
     "Short 2–3 line description: what it does, who it's for, what was hard about it. "
     "Replace this placeholder with a real project.",
     "#", "#",
     ["Node.js", "NestJS", "Redis", "Kubernetes"]),
    ("// 03", "[PROJECT_3]",
     "Short 2–3 line description: what it does, who it's for, what was hard about it. "
     "Replace this placeholder with a real project.",
     "#", "#",
     ["Bash", "Ansible", "MikroTik"]),
    ("// 04", "[PROJECT_4]",
     "Short 2–3 line description: what it does, who it's for, what was hard about it. "
     "Replace this placeholder with a real project.",
     "#", "#",
     ["Python", "Burp Suite", "OSINT"]),
    ("// 05", "[PROJECT_5]",
     "Short 2–3 line description: what it does, who it's for, what was hard about it. "
     "Replace this placeholder with a real project.",
     "#", "#",
     ["Terraform", "AWS", "GitHub Actions"]),
    ("// 06", "[PROJECT_6]",
     "Short 2–3 line description: what it does, who it's for, what was hard about it. "
     "Replace this placeholder with a real project.",
     "#", "#",
     ["ELK", "Wazuh", "Linux"]),
]

EXPERIENCE = [
    ("2024 — Present", "[ROLE_1] · [COMPANY_1]", "[COMPANY_1]",
     "Ashgabat · full-time",
     ["Designed and shipped backend services in Python/FastAPI for [DOMAIN].",
      "Set up CI/CD, monitoring, and incident response runbooks from scratch.",
      "Led an internal security audit; closed [N] critical findings."]),
    ("2022 — 2024", "[ROLE_2] · [COMPANY_2]", "[COMPANY_2]",
     "Ashgabat · full-time",
     ["Built and operated network infrastructure for [N] sites: BGP, OSPF, VPN.",
      "Automated provisioning with Ansible and Bash; reduced rollout time by [X]%.",
      "Hardened firewalls and DNS; introduced centralized logging in ELK."]),
    ("2021 — 2022", "[ROLE_3] · [COMPANY_3]", "[COMPANY_3]",
     "Ashgabat · part-time / freelance",
     ["Wrote backend APIs and admin panels for small business clients.",
      "Linux server administration, deploys, backups, basic security hardening.",
      "First exposure to pentesting tooling — Nmap, Burp Suite, simple OSINT."]),
]


def seed():
    with app.app_context():
        db.drop_all()
        db.create_all()

        for k, v in SITE.items():
            db.session.add(SiteSetting(key=k, value=v))

        for i, (num, lbl, color) in enumerate(STATS):
            db.session.add(Stat(num=num, label=lbl, color=color, order=i))

        for i, (kind, lbl, val, url, icon) in enumerate(CONTACTS):
            db.session.add(Contact(kind=kind, label=lbl, value=val,
                                   url=url, icon=icon, order=i))

        for ci, (kicker, title, icon, accent, tags) in enumerate(CLUSTERS):
            cluster = SkillCluster(kicker=kicker, title=title, icon=icon,
                                   accent=accent, order=ci)
            db.session.add(cluster)
            db.session.flush()
            for ti, tag in enumerate(tags):
                db.session.add(SkillTag(cluster_id=cluster.id,
                                        name=tag, order=ti))

        for pi, (num, title, desc, code, live, tags) in enumerate(PROJECTS):
            project = Project(num=num, title=title, description=desc,
                              code_url=code, live_url=live, order=pi)
            db.session.add(project)
            db.session.flush()
            for ti, tag in enumerate(tags):
                db.session.add(ProjectTag(project_id=project.id,
                                          name=tag, order=ti))

        for ei, (period, role, company, meta, bullets) in enumerate(EXPERIENCE):
            exp = Experience(period=period, role=role, company=company,
                             company_meta=meta, order=ei)
            db.session.add(exp)
            db.session.flush()
            for bi, text in enumerate(bullets):
                db.session.add(ExperienceBullet(experience_id=exp.id,
                                                text=text, order=bi))

        db.session.commit()
        print("Seeded.")


if __name__ == "__main__":
    seed()

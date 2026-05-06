"""Populate the DB with content extracted from resume_rustem_nuryev.html."""
from app import app
from models import (
    Contact, Experience, ExperienceBullet, HeroRole, Project, ProjectTag,
    SiteSetting, SkillCluster, SkillTag, Stat, db,
)


SITE = {
    "hero_badge": "Open to work · Ashgabat 🇹🇲 · Remote OK",
    "hero_title_prefix": "Hi, I'm",
    "hero_name": "Rustem Nuryev",
    "hero_desc_en": "4+ years shipping reliable backends and breaking insecure ones. "
                    "I build full-stack systems on FastAPI / Flask / Node, run them on Linux "
                    "infra I maintain myself, and audit them with the same toolkit I use to "
                    "break into other targets.",
    "hero_desc_ru": "4+ года создаю надёжные бэкенды и ломаю уязвимые. "
                    "Строю full-stack системы на FastAPI / Flask / Node, поднимаю их на Linux-"
                    "инфраструктуре, которую сам же поддерживаю, и аудирую тем же инструментарием, "
                    "которым ломаю другие цели.",
    "hero_meta_location": "Ashgabat, TM",
    "hero_meta_exp": "4+ yrs",
    "hero_meta_stack": "Python · Node · Linux",
    "about_title_html": "Engineer at the boundary of <span style=\"color:var(--cyan)\">code</span> "
                        "and <span style=\"color:var(--purple)\">security</span>.",
    "about_p1": "I'm <strong>Rustem Nuryev</strong> (<span class=\"accent\">yomarakesha</span>) — "
                "a backend, network and security engineer from "
                "<span class=\"accent\">Ashgabat, Turkmenistan</span>. I work end-to-end: design "
                "the data model, write the API, wire the deploy, harden the box, and stay around "
                "when something breaks at 3 AM.",
    "about_p2": "I've shipped <strong>25+ projects</strong> — from courier-delivery platforms with "
                "QR/SMS workflows to OSINT investigation tools with LLM agents and graph UIs, plus "
                "a personally-maintained fork of a popular pentesting toolkit (185+ tools, "
                "20 categories).",
    "about_p3": "Fluent across the stack — Python (FastAPI, Flask, SQLAlchemy, Celery), Node "
                "(Nest, Express), front-end (React, Three.js), data (PostgreSQL, MongoDB, Redis, "
                "SQLite), ops (Docker, Linux, MikroTik/Cisco, BGP/OSPF, ELK/Wazuh, Burp Suite).",
    "about_p4": "Right now I'm <span class=\"accent\">open to interesting work</span> — backend, "
                "network engineering, DevOps, or offensive/defensive security roles. If you have "
                "a system that needs to be built — or one you're worried about — let's talk.",
    "section_about_sub": "I work end-to-end: design the data model, write the API, wire the deploy, "
                         "harden the box, and stay around when something breaks at 3 AM.",
    "section_skills_sub": "Seven clusters I rotate through depending on what's on fire that day.",
    "section_projects_sub": "Real systems I've designed, built and maintained — production and prototypes.",
    "section_experience_sub": "A reverse-chronological log of where I've spent my keystrokes.",
    "section_contact_sub": "Best for: backend, network or DevOps work, security audits, or just a "
                           "good technical conversation.",
    "footer_copy": "© 2026 Rustem Nuryev · Yomarakesha",
}

STATS = [
    ("25+", "projects shipped", ""),
    ("185+", "pentest tools maintained", "lime"),
    ("20+", "technologies in active use", "purple"),
    ("4+ yrs", "in production", ""),
]

CONTACTS = [
    ("email", "email", "yomarakesha@gmail.com",
     "mailto:yomarakesha@gmail.com", "mail"),
    ("github", "github", "github.com/yomarakesha",
     "https://github.com/yomarakesha", "github"),
    ("telegram", "telegram", "@yomarakesha",
     "https://t.me/yomarakesha", "send"),
]

CLUSTERS = [
    ("// 01 · backend", "Languages & Frameworks", "Языки и фреймворки", "code-2", "",
     ["Python 3", "FastAPI", "Flask", "SQLAlchemy", "Celery", "Pydantic",
      "Node.js", "NestJS", "Express", "Bash", "PowerShell"]),
    ("// 02 · frontend", "Web & Mobile UI", "Web и мобильный UI", "code-2", "",
     ["React", "Vite", "Three.js", "Cytoscape.js", "Tailwind",
      "Vanilla JS", "HTML/CSS", "React Native"]),
    ("// 03 · data", "Storage & Pipelines", "Хранилища и пайплайны", "database", "",
     ["PostgreSQL", "SQLite", "MongoDB", "Redis", "MySQL",
      "Alembic", "REST", "WebSockets", "SSE"]),
    ("// 04 · devops", "Infra & Deployment", "Инфра и деплой", "server-cog", "accent-lime",
     ["Docker", "docker-compose", "Linux", "Ubuntu/Debian", "Arch",
      "Nginx", "Gitea", "Railway", "GitHub Actions"]),
    ("// 05 · network", "Networking", "Сети", "network", "accent-purple",
     ["TCP/IP", "BGP", "OSPF", "VLAN", "VPN", "MikroTik", "Cisco",
      "DNS", "Firewalls", "WebRTC", "MediaMTX"]),
    ("// 06 · security", "Pentest & DevSecOps", "Пентест и DevSecOps", "shield-check", "accent-purple",
     ["Burp Suite", "Metasploit", "Nmap", "OSINT", "Telethon (MTProto)",
      "Wazuh", "ELK", "Code Audit", "Threat Intel"]),
    ("// 07 · ai", "AI integration", "AI-интеграция", "code-2", "",
     ["Claude API", "OpenAI / GPT", "MediaPipe", "SSE streaming", "Tool-use agents"]),
]

PROJECTS = [
    ("// 01", "Chapar Express", "Chapar Express",
     "Automated inter-city courier delivery platform for Turkmenistan with a two-courier "
     "air-freight workflow. OTP/JWT auth, FCM push, 17-status order lifecycle with QR tracking, "
     "courier balance & payouts, GünDelik flight integration via webhook, admin panel + courier "
     "mobile app.",
     "Автоматизированная платформа межгородской курьерской доставки для Туркменистана с "
     "двух-курьерским авиа-workflow. OTP/JWT-авторизация, FCM push, 17-статусный жизненный цикл "
     "заказа с QR-трекингом, баланс и выплаты курьерам, интеграция с GünDelik через webhook, "
     "админ-панель + мобильное приложение курьера.",
     "", "",
     ["FastAPI", "SQLAlchemy", "PostgreSQL", "JWT/OTP", "FCM", "React Native", "Docker"]),
    ("// 02", "OSINT Investigation Platform", "OSINT-платформа расследований",
     "Local OSINT platform for phone/email/nickname/domain/IP investigations. Single FastAPI "
     "process + SQLite, Cytoscape.js graph of entities & edges, parallel module execution via "
     "asyncio semaphores, custom binary leak-DB importer with hex viewer and entropy/magic "
     "detection, AI agent on Claude with SSE streaming.",
     "Локальная OSINT-платформа для расследований по телефону/email/нику/домену/IP. Один процесс "
     "FastAPI + SQLite, граф сущностей и связей на Cytoscape.js, параллельный запуск модулей через "
     "asyncio-семафоры, кастомный импортёр бинарных leak-БД с hex-вьюером и определением "
     "энтропии/magic, AI-агент на Claude со стримингом по SSE.",
     "", "",
     ["FastAPI", "Telethon", "Claude API", "Cytoscape.js", "SQLite", "SSE", "asyncio"]),
    ("// 03", "HackingTool v2.0 (fork)", "HackingTool v2.0 (форк)",
     "Modernised fork of an all-in-one pentesting toolkit. Migrated from Python 2 to 3.10+, "
     "added OS-aware menus, search/tag filtering across 19 tags, install-status detection, batch "
     "install, smart updater (auto-detects git pull / pip / go install), Docker builds, "
     "one-liner installer, three new categories: AD, cloud and mobile security.",
     "Модернизированный форк all-in-one пентест-тулкита. Миграция с Python 2 на 3.10+, "
     "OS-aware меню, поиск/фильтр по 19 тегам, детект install-статуса, batch-установка, "
     "smart-апдейтер (auto-detect git pull / pip / go install), Docker-сборки, one-liner "
     "установщик, три новые категории: AD, cloud и mobile security.",
     "", "",
     ["Python 3.10+", "Bash", "Docker", "Pentesting", "Linux/macOS"]),
    ("// 04", "DSS — Dahua Surveillance Dashboard", "DSS — дашборд видеонаблюдения Dahua",
     "Web dashboard for Dahua NVR camera feeds via low-latency WebRTC. Configurable grids "
     "(2×2 to 64×64), patrol mode that auto-cycles pages, custom groups and saved layouts, "
     "fullscreen with snapshot capture, full keyboard-driven UX. Stdlib-only Python — no pip "
     "dependencies, just MediaMTX bundled.",
     "Web-дашборд камер Dahua NVR через low-latency WebRTC. Настраиваемые сетки (2×2 до 64×64), "
     "режим патруля с авто-переключением страниц, кастомные группы и сохранённые раскладки, "
     "fullscreen со снапшотами, полностью клавиатурный UX. Только stdlib Python — без pip-"
     "зависимостей, только bundled MediaMTX.",
     "", "",
     ["Python (stdlib)", "WebRTC", "MediaMTX", "RTSP", "JavaScript"]),
    ("// 05", "Yomarakesha Portfolio CMS", "CMS портфолио Yomarakesha",
     "Self-built portfolio with a full admin CMS. Flask + SQLAlchemy backend, JSON API, "
     "drag-and-drop reordering, image uploads, EN/RU localisation, contact form with Telegram "
     "bot notifications, page-view analytics, sitemap/robots, printable CV route. Auth via "
     "password + signed JWT-ish token (itsdangerous).",
     "Самописное портфолио с полноценной админ-CMS. Flask + SQLAlchemy, JSON API, drag-and-drop "
     "сортировка, загрузка изображений, EN/RU-локализация, контакт-форма с уведомлениями в "
     "Telegram-бота, аналитика просмотров, sitemap/robots, печатный CV. Авторизация — пароль + "
     "подписанный JWT-подобный токен (itsdangerous).",
     "", "",
     ["Flask", "SQLAlchemy", "SQLite", "Vanilla JS", "Telegram Bot"]),
    ("// 06", "OSINT Analyser (LLM pipeline)", "OSINT-аналайзер (LLM-пайплайн)",
     "Dockerised collection-and-analysis pipeline for open-source intelligence. Pulls from "
     "Telegram channels, translates non-English content, then routes per-source analysis "
     "requirements (stored in MySQL) into GPT for tailored summaries — different prompts for "
     "e.g. Russia/Ukraine vs Israel/Gaza coverage.",
     "Dockerised пайплайн сбора и анализа OSINT. Тянет из Telegram-каналов, переводит "
     "не-английский контент, затем отправляет per-source требования к анализу (хранятся в MySQL) "
     "в GPT для кастомных сводок — разные промпты, например, для Россия/Украина vs Израиль/Газа.",
     "", "",
     ["Python", "Docker", "OpenAI API", "MySQL", "Telegram"]),
    ("// 07", "Life Tracker (TUI)", "Life Tracker (TUI)",
     "Productivity TUI app inspired by vim/htop. Four modules: TODO with priorities & "
     "deadlines, GYM with weight sparklines and muscle-group stats, HABITS with weekly streak "
     "grid, POMODORO with auto-cycling break timers. Alternate-screen buffer, mouse-free, single "
     "Python file.",
     "TUI-приложение для продуктивности в духе vim/htop. Четыре модуля: TODO с приоритетами и "
     "дедлайнами, GYM со спарклайнами весов и статистикой по мышечным группам, HABITS с недельной "
     "сеткой стриков, POMODORO с авто-переключением break-таймеров. Alternate-screen buffer, без "
     "мыши, один Python-файл.",
     "", "",
     ["Python", "curses", "SQLite", "TUI"]),
    ("// 08", "3D Particle System (gesture-controlled)", "3D-партикл-система (управление жестами)",
     "Real-time visualiser controlled by hand gestures via webcam. MediaPipe recognises open "
     "palm / fist / motion, particles morph between Sphere / Cube / Galaxy / DNA-twist patterns. "
     "Live colour palette, fullscreen, post-processing bloom — pure web, no plugins.",
     "Real-time визуализатор, управляемый жестами руки через вебкамеру. MediaPipe распознаёт "
     "открытую ладонь / кулак / движение, частицы морфятся между паттернами Sphere / Cube / "
     "Galaxy / DNA-twist. Живая палитра, fullscreen, post-processing bloom — чистый веб, без "
     "плагинов.",
     "", "",
     ["React", "Vite", "@react-three/fiber", "MediaPipe", "Three.js"]),
    ("// 09", "QR vCard Admin", "QR vCard Admin",
     "vCard contact manager with on-demand QR generation. Full REST API (CRUD, vCard text, "
     "PNG QR with size/ECL options, preview without saving), Flask + SQLite, deployable to "
     "Railway with one click. Used as a digital business-card backend.",
     "Менеджер vCard-контактов с генерацией QR по запросу. Полноценный REST API (CRUD, vCard-"
     "текст, PNG QR с настройкой размера/ECL, превью без сохранения), Flask + SQLite, деплой в "
     "Railway в один клик. Используется как бэкенд цифровой визитки.",
     "", "",
     ["Flask", "SQLite", "qrcode", "REST API", "Railway"]),
    ("// 10", "Self-hosted Gitea + tooling", "Self-hosted Gitea + тулинг",
     "Personal Git infrastructure on Linux: Gitea binary, custom config, log rotation, backup "
     "scripts, hook-based CI. Used to host all the projects on this page.",
     "Персональная Git-инфраструктура на Linux: бинарник Gitea, кастомный конфиг, ротация логов, "
     "backup-скрипты, hook-based CI. Хостит все проекты с этой страницы.",
     "", "",
     ["Gitea", "Linux", "Bash", "systemd"]),
    ("// 11", "SSL · Tagma — utility services", "SSL · Tagma — утилитарные сервисы",
     "A cluster of small Flask services: SSL/credential vault with Fernet-encrypted storage; "
     "certificate audit dashboard with auto-rendered certificate / dashboard pages; "
     "multi-language API with file uploads and i18n via Babel.",
     "Кластер небольших Flask-сервисов: SSL/credential vault с Fernet-шифрованным хранилищем; "
     "дашборд аудита сертификатов с авто-генерируемыми страницами сертификата/дашборда; "
     "multi-language API с загрузкой файлов и i18n через Babel.",
     "", "",
     ["Flask", "Fernet", "Babel i18n", "Docker"]),
]

HERO_ROLES = [
    ("Backend Developer", "Backend разработчик"),
    ("Network Engineer", "Сетевой инженер"),
    ("DevOps Engineer", "DevOps инженер"),
    ("Cybersecurity Specialist", "Специалист по кибербезопасности"),
]

EXPERIENCE = [
    ("2024 — Present",
     "Backend / DevOps Engineer · Freelance & contract",
     "Backend / DevOps инженер · Фриланс и контракты",
     "Freelance & contract",
     "Ashgabat · remote-friendly",
     "Ашхабад · remote-friendly",
     [("Designed and shipped FastAPI backends (couriers, OSINT, OSS tooling) with "
       "SQLAlchemy/Postgres, Alembic migrations, Celery workers and SSE streaming.",
       "Спроектировал и выпустил FastAPI-бэкенды (курьеры, OSINT, OSS-тулинг) с "
       "SQLAlchemy/Postgres, миграциями Alembic, воркерами Celery и SSE-стримингом."),
      ("Built and maintained Linux infrastructure: self-hosted Gitea, Docker-compose deployments, "
       "MediaMTX-based WebRTC streaming for surveillance.",
       "Поднимал и поддерживал Linux-инфраструктуру: self-hosted Gitea, деплои через docker-"
       "compose, WebRTC-стриминг видеонаблюдения на MediaMTX."),
      ("Integrated Claude and OpenAI as production AI agents with tool-use, streaming responses, "
       "and per-source prompt routing.",
       "Интегрировал Claude и OpenAI как продакшн AI-агентов с tool-use, стримингом ответов и "
       "per-source маршрутизацией промптов."),
      ("Maintained a popular open-source pentesting toolkit (185+ tools, 20 categories) — "
       "Python 3 migration, search/tag filter, install-status detection, Docker.",
       "Поддерживал популярный open-source пентест-тулкит (185+ инструментов, 20 категорий) — "
       "миграция на Python 3, поиск/фильтр по тегам, детект install-статуса, Docker.")]),
    ("2022 — 2024",
     "Network & Backend Engineer",
     "Сетевой и backend инженер",
     "full-time / contract",
     "Ashgabat · full-time / contract",
     "Ашхабад · full-time / контракт",
     [("Built and operated network infrastructure across multiple sites: BGP/OSPF peering, "
       "VLAN segmentation, site-to-site VPN, MikroTik & Cisco config.",
       "Строил и эксплуатировал сетевую инфраструктуру на нескольких площадках: BGP/OSPF-пиринг, "
       "сегментация VLAN, site-to-site VPN, конфигурация MikroTik и Cisco."),
      ("Automated provisioning with Bash and Ansible-style scripts; reduced rollout time by ~35%.",
       "Автоматизировал provisioning Bash- и Ansible-style скриптами; сократил время раскатки "
       "примерно на 35%."),
      ("Hardened firewalls and DNS, introduced centralized logging in ELK and host monitoring "
       "with Wazuh.",
       "Усиливал firewall и DNS, внедрил централизованное логирование в ELK и хост-мониторинг "
       "через Wazuh."),
      ("Wrote backend APIs and admin panels for internal business apps (e-commerce, IT-incident "
       "reporting, courier ops).",
       "Писал backend API и админ-панели для внутренних бизнес-приложений (e-commerce, "
       "IT-incident reporting, курьерские операции).")]),
    ("2021 — 2022",
     "Junior Developer / Sysadmin",
     "Junior разработчик / Системный администратор",
     "part-time / freelance",
     "Ashgabat · part-time / freelance",
     "Ашхабад · part-time / фриланс",
     [("Wrote Flask + SQLite admin panels and REST APIs for small business clients.",
       "Писал админ-панели на Flask + SQLite и REST API для small business клиентов."),
      ("Linux server administration: deploys, backups, basic security hardening, certificate "
       "management.",
       "Администрирование Linux-серверов: деплои, бэкапы, базовый security hardening, "
       "управление сертификатами."),
      ("First exposure to pentest tooling — Nmap, Burp Suite, Metasploit, OSINT workflows.",
       "Первое знакомство с пентест-тулингом — Nmap, Burp Suite, Metasploit, OSINT-воркфлоу.")]),
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

        for ci, (kicker, title, title_ru, icon, accent, tags) in enumerate(CLUSTERS):
            cluster = SkillCluster(kicker=kicker, title=title, title_ru=title_ru,
                                   icon=icon, accent=accent, order=ci)
            db.session.add(cluster)
            db.session.flush()
            for ti, tag in enumerate(tags):
                db.session.add(SkillTag(cluster_id=cluster.id,
                                        name=tag, order=ti))

        for pi, (num, title, title_ru, desc, desc_ru, code, live, tags) in enumerate(PROJECTS):
            project = Project(num=num, title=title, title_ru=title_ru,
                              description=desc, description_ru=desc_ru,
                              code_url=code, live_url=live, order=pi)
            db.session.add(project)
            db.session.flush()
            for ti, tag in enumerate(tags):
                db.session.add(ProjectTag(project_id=project.id,
                                          name=tag, order=ti))

        for ri, (text_en, text_ru) in enumerate(HERO_ROLES):
            db.session.add(HeroRole(text=text_en, text_ru=text_ru, order=ri))

        for ei, (period, role, role_ru, company, meta, meta_ru, bullets) in enumerate(EXPERIENCE):
            exp = Experience(period=period, role=role, role_ru=role_ru,
                             company=company, company_meta=meta,
                             company_meta_ru=meta_ru, order=ei)
            db.session.add(exp)
            db.session.flush()
            for bi, (text_en, text_ru) in enumerate(bullets):
                db.session.add(ExperienceBullet(experience_id=exp.id,
                                                text=text_en, text_ru=text_ru,
                                                order=bi))

        db.session.commit()
        print("Seeded.")


if __name__ == "__main__":
    seed()

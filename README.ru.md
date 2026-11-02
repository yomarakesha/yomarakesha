# Рустем Нурыев

[English](README.md) · **Русский**

**DevOps-инженер с сильным backend-бэкграундом (Golang / FastAPI)**

Пишу бэкенды, разворачиваю их на Linux-серверах, которые сам администрирую, и слежу, чтобы они были наблюдаемыми и защищёнными.
Полевой опыт на крупных объектах физической безопасности: ~1000 IP-камер, СКУД Hikvision, SIEM Wazuh на ~500 хостах.

Открыт к удалённой работе · Ашхабад, Туркменистан (UTC+5)

[![Email](https://img.shields.io/badge/Email-yomarakesha%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:yomarakesha@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-%40yomarakesha-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/yomarakesha)
<!-- TODO: add LinkedIn badge: [![LinkedIn](https://img.shields.io/badge/LinkedIn-profile-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/<handle>) -->

---

## Стек

**Инфраструктура и деплой**
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![Docker](https://img.shields.io/badge/Docker_Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![systemd](https://img.shields.io/badge/systemd-30D475?style=flat-square&logo=linux&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Let's Encrypt](https://img.shields.io/badge/Let's_Encrypt-003A70?style=flat-square&logo=letsencrypt&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white)

**Backend и данные**
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy_+_Alembic-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-C72E49?style=flat-square&logo=minio&logoColor=white)

**Наблюдаемость и безопасность**
![Wazuh](https://img.shields.io/badge/Wazuh_SIEM-3595F9?style=flat-square&logo=wazuh&logoColor=white)
![Sentry](https://img.shields.io/badge/GlitchTip_/_Sentry-362D59?style=flat-square&logo=sentry&logoColor=white)
![Active Directory](https://img.shields.io/badge/Active_Directory_logging-0078D4?style=flat-square&logo=windows&logoColor=white)
![ufw](https://img.shields.io/badge/ufw_/_fail2ban-555555?style=flat-square)

**Сети и физическая безопасность**
![MikroTik](https://img.shields.io/badge/MikroTik-293239?style=flat-square&logo=mikrotik&logoColor=white)
![Cisco](https://img.shields.io/badge/Cisco-1BA0D7?style=flat-square&logo=cisco&logoColor=white)
![VLAN](https://img.shields.io/badge/VLAN_/_VPN-555555?style=flat-square)
![Hikvision](https://img.shields.io/badge/Hikvision_ACS_+_CCTV-E1251B?style=flat-square)
![Dahua](https://img.shields.io/badge/Dahua_NVR-E60012?style=flat-square)
![WebRTC](https://img.shields.io/badge/WebRTC_/_RTSP_/_HLS-333333?style=flat-square&logo=webrtc&logoColor=white)

**Frontend и мобильная разработка** (достаточно, чтобы довести продукт целиком)
![React](https://img.shields.io/badge/React_+_TS-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![Expo](https://img.shields.io/badge/React_Native_/_Expo-000020?style=flat-square&logo=expo&logoColor=white)
![Flutter](https://img.shields.io/badge/Flutter-02569B?style=flat-square&logo=flutter&logoColor=white)


---

## Полевой опыт: физическая безопасность и SIEM

| Направление | Масштаб | Что делал |
|---|---|---|
| **Видеонаблюдение** | ~1000 IP-камер | Централизованный сервер управления (класса Hikvision CMS), интеграция NVR, проектирование сети под видеотрафик. Написал собственную VMS (кейс ниже). |
| **СКУД** | Hikvision | Полный цикл: контроллеры и считыватели, подключение и пусконаладка, карты и пропуска, уровни доступа, графики. |
| **SIEM** | ~500 рабочих станций | Wazuh: сбор логов Active Directory, обнаружение угроз, мониторинг трафика, оповещения. |
| **Сети** | несколько площадок | Настройка MikroTik и Cisco, сегментация VLAN, site-to-site VPN, защита firewall и DNS. |

```mermaid
flowchart LR
    subgraph Endpoints["Источники"]
        PC["~500 рабочих станций Windows<br/>агенты Wazuh"]
        AD["Active Directory<br/>контроллеры домена"]
        NET["Сетевое оборудование<br/>syslog"]
    end
    PC --> WM["Wazuh manager<br/>декодеры + правила"]
    AD --> WM
    NET --> WM
    WM --> IDX["Wazuh indexer"]
    IDX --> DASH["Дашборд + оповещения"]
```

---

## Основные кейсы

### 1. Централизованная система управления видео (VMS)

**Проблема.** NVR Dahua ограничивают число одновременных подключений. Когда смотрят много операторов, NVR отказывают новым зрителям.

**Решение.** VMS держит **одну** RTSP-сессию на канал NVR, сколько бы операторов его ни смотрели. MediaMTX открывает поток при первом зрителе и закрывает после ухода последнего, поэтому неактивные каналы не занимают слоты NVR.

```mermaid
flowchart LR
    OPS["Операторы<br/>браузер / десктоп на Electron"] -->|HTTPS| NGX["nginx"]
    NGX -->|/api| API["FastAPI<br/>авторизация, RBAC, инвентарь"]
    API --> PG[("PostgreSQL")]
    API -->|control API| MTX["MediaMTX"]
    NGX -->|WebRTC WHEP / HLS| MTX
    MTX -->|"1 RTSP-поток на активный канал"| NVR["NVR Dahua"]
```

**Моя роль.** Архитектура, backend, деплой.
**Стек.** FastAPI, async SQLAlchemy, Alembic, PostgreSQL, MediaMTX, WebRTC (WHEP) с откатом на HLS, React, Electron.
**Деплой.** Docker Compose в трёх режимах (bridge, host network, полностью офлайн для изолированных объектов) плюс нативная сборка под Windows. GitHub Actions собирает установщик для Windows и десктоп-клиент.

<details>
<summary>Подробнее</summary>

- Пути каналов backend управляет динамически через control API MediaMTX.
- Сетки операторов от 2×2 до 64×64, режим патруля, сохранённые раскладки, снимки.
- Учётные данные NVR хранятся зашифрованными, пароли хешируются argon2.
- Офлайн-сборка compose для объектов без доступа в интернет.

</details>

### 2. Платформа межгородской авиадоставки посылок

**Проблема.** Логистическая компания доставляет посылки между городами самолётом. На заказ два курьера (от отправителя до аэропорта и из аэропорта до получателя), данные о рейсах приходят из внешней системы.

```mermaid
flowchart LR
    APP["Мобильное приложение курьера<br/>React Native"] -->|HTTPS| NGX["nginx + TLS"]
    ADM["Админ-панель<br/>React + MapLibre"] --> NGX
    NGX --> API["FastAPI<br/>сервис systemd"]
    API --> PG[("PostgreSQL")]
    API --> S3[("MinIO<br/>фото, документы")]
    API --> FCM["Firebase<br/>push-уведомления"]
    EXT["Система рейсов"] -->|webhook| API
    API --> SCH["Задачи APScheduler"]
    API -.->|ошибки, медленные запросы| GT["GlitchTip<br/>self-hosted"]
```

**Моя роль.** Backend, инфраструктура, деплой, мониторинг (578 коммитов).
**Стек.** FastAPI, SQLAlchemy, Alembic, PostgreSQL (asyncpg), MinIO, APScheduler, Firebase Admin, авторизация OTP + JWT.
**Деплой.** Юниты systemd за nginx, Dockerfile и Compose для backend, свой GlitchTip в Docker для отслеживания ошибок.

<details>
<summary>Подробнее</summary>

- Жизненный цикл заказа из 17 статусов с QR-кодами и полной историей.
- Балансы и выплаты курьерам.
- Интеграция с расписанием рейсов через webhook.
- Сбои планировщика и медленные запросы уходят в GlitchTip.

</details>

### 3. Набор инструментов сетевой безопасности с интеграцией Wazuh (open source)

[![CI](https://github.com/yomarakesha/speedtest/actions/workflows/ci.yml/badge.svg)](https://github.com/yomarakesha/speedtest)

**[yomarakesha/speedtest](https://github.com/yomarakesha/speedtest)**: CLI и терминальный дашборд на Go для диагностики сети и аудита безопасности. Вырос в микросервисную систему: Python-оркестратор ставит задачи на обнаружение и аудит, Go-сервисы отправляют находки в Wazuh.

```mermaid
flowchart LR
    CLI["Go CLI / TUI<br/>scan, audit, tlsaudit,<br/>dnssec, cvecheck, sniff"] -->|задачи| ORC["Python-оркестратор<br/>FastAPI"]
    ORC --> AUD["сервис аудита<br/>Go"]
    ORC --> SCN["сервис сканирования<br/>Go"]
    AUD -->|"находки, JSON"| WZ["Wazuh<br/>свои декодеры + правила"]
    SCN --> WZ
    CLI -->|"вывод --wazuh"| WZ
```

**Стек.** Go, Python, FastAPI, Wazuh, Docker Compose, GitHub Actions, GoReleaser (Linux, macOS, Windows; amd64 + arm64).
**Возможности.** Сканирование портов с баннерами и отпечатками сервисов, обнаружение хостов в подсети (MAC, вендор, SNMP), аудит TLS и HTTP-заголовков безопасности с оценкой A–F, проверки DNSSEC/SPF/DMARC, сверка баннеров с CVE, traceroute без root, тест bufferbloat, захват пакетов.

### 4. Видеоаналитика на CPU (open source)

**[yomarakesha/korgoz](https://github.com/yomarakesha/korgoz)**: локальная платформа видеоаналитики. Камеры, затем детекция, трекинг, распознавание лиц, события и аналитика. Работает нативно на systemd, без Docker, на обычных процессорах.

```mermaid
flowchart LR
    CAM["Камеры<br/>RTSP / USB / файл"] --> DET["Детекция<br/>YOLOX, ONNX Runtime"]
    DET --> TRK["Трекинг<br/>ByteTrack + Kalman"]
    TRK --> REC["Распознавание<br/>YuNet + SFace"]
    REC --> QD[("Qdrant<br/>векторы лиц")]
    TRK --> EV["Движок событий"]
    EV --> DB[("PostgreSQL")]
    DB --> API["FastAPI + дашборд на React"]
```

**Стек.** Python, FastAPI, ONNX Runtime, OpenCV, Qdrant, PostgreSQL, SQLAlchemy, Alembic, React, systemd (юниты API и воркера).
**Цифры.** Замеры на Intel Core Ultra 5 125U, только CPU: YOLOX-tiny обрабатывает 4 камеры без потери кадров на ~2,5 ядрах, задержка p95 ~0,15 с.

---

## Другие проекты в продакшене

Код клиентских проектов закрыт. Кратко:

| Проект | Что это | Стек | Деплой |
|---|---|---|---|
| Платформа постаматов | Backend, веб для операторов, мобильное приложение и агент замков на устройстве | FastAPI, PostgreSQL, Flutter, Node | агент systemd на устройстве, контрактные тесты (Schemathesis) |
| Маркетплейс | Витрина, админка и мобильное приложение для национального почтового оператора | FastAPI, MySQL, React, Expo | systemd + nginx |
| Интернет-магазин + CRM | Магазин IT- и охранного оборудования, CRM с RBAC | FastAPI, SQLite, React | systemd + nginx, CI на GitHub Actions |
| Доска вакансий | Серверный рендеринг, работает без JavaScript на медленном мобильном интернете | FastAPI, Next.js | Docker Compose |
| Юридический и HR-комплекс | Договорной документооборот, согласования, HR | Django REST (v1), затем монорепо NestJS + Prisma + tRPC (pnpm, Turborepo), React | Docker Compose + nginx |

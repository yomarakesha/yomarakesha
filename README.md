# Rustem Nuryev

**DevOps Engineer with a strong backend background (Golang / FastAPI)**

I build backends, ship them to Linux servers I run myself, and keep them observable and secure.
Field experience with large physical-security deployments: ~1,000 IP cameras, Hikvision access control, Wazuh SIEM across ~500 hosts.

Open to remote work · Ashgabat, Turkmenistan (UTC+5)

[![Email](https://img.shields.io/badge/Email-yomarakesha%40gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:yomarakesha@gmail.com)
[![Telegram](https://img.shields.io/badge/Telegram-%40yomarakesha-26A5E4?style=flat-square&logo=telegram&logoColor=white)](https://t.me/yomarakesha)
<!-- TODO: add LinkedIn badge: [![LinkedIn](https://img.shields.io/badge/LinkedIn-profile-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/<handle>) -->

---

## Stack

**Infrastructure & deploy**
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black)
![Docker](https://img.shields.io/badge/Docker_Compose-2496ED?style=flat-square&logo=docker&logoColor=white)
![systemd](https://img.shields.io/badge/systemd-30D475?style=flat-square&logo=linux&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white)
![Let's Encrypt](https://img.shields.io/badge/Let's_Encrypt-003A70?style=flat-square&logo=letsencrypt&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=flat-square&logo=gnubash&logoColor=white)

**Backend & data**
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy_+_Alembic-D71F00?style=flat-square&logo=sqlalchemy&logoColor=white)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-C72E49?style=flat-square&logo=minio&logoColor=white)

**Observability & security**
![Wazuh](https://img.shields.io/badge/Wazuh_SIEM-3595F9?style=flat-square&logo=wazuh&logoColor=white)
![Sentry](https://img.shields.io/badge/GlitchTip_/_Sentry-362D59?style=flat-square&logo=sentry&logoColor=white)
![Active Directory](https://img.shields.io/badge/Active_Directory_logging-0078D4?style=flat-square&logo=windows&logoColor=white)
![ufw](https://img.shields.io/badge/ufw_/_fail2ban-555555?style=flat-square)

**Networks & physical security**
![MikroTik](https://img.shields.io/badge/MikroTik-293239?style=flat-square&logo=mikrotik&logoColor=white)
![Cisco](https://img.shields.io/badge/Cisco-1BA0D7?style=flat-square&logo=cisco&logoColor=white)
![VLAN](https://img.shields.io/badge/VLAN_/_VPN-555555?style=flat-square)
![Hikvision](https://img.shields.io/badge/Hikvision_ACS_+_CCTV-E1251B?style=flat-square)
![Dahua](https://img.shields.io/badge/Dahua_NVR-E60012?style=flat-square)
![WebRTC](https://img.shields.io/badge/WebRTC_/_RTSP_/_HLS-333333?style=flat-square&logo=webrtc&logoColor=white)

**Frontend & mobile** (enough to ship the whole product)
![React](https://img.shields.io/badge/React_+_TS-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![Expo](https://img.shields.io/badge/React_Native_/_Expo-000020?style=flat-square&logo=expo&logoColor=white)
![Flutter](https://img.shields.io/badge/Flutter-02569B?style=flat-square&logo=flutter&logoColor=white)

---

## Field experience: physical security and SIEM

| Area | Scale | What I did |
|---|---|---|
| **CCTV** | ~1,000 IP cameras | Centralized management server (Hikvision CMS class), NVR integration, network design for video traffic. Wrote a custom VMS (case study below). |
| **Access control (ACS)** | Hikvision | Full cycle: controllers and readers, connection and commissioning, cards and passes, access levels, time schedules. |
| **SIEM** | ~500 workstations | Wazuh: Active Directory log collection, threat detection, traffic monitoring, alerting. |
| **Networks** | multi-site | MikroTik and Cisco configuration, VLAN segmentation, site-to-site VPN, firewall and DNS hardening. |

```mermaid
flowchart LR
    subgraph Endpoints
        PC["~500 Windows workstations<br/>Wazuh agents"]
        AD["Active Directory<br/>domain controllers"]
        NET["Network devices<br/>syslog"]
    end
    PC --> WM["Wazuh manager<br/>decoders + rules"]
    AD --> WM
    NET --> WM
    WM --> IDX["Wazuh indexer"]
    IDX --> DASH["Dashboard + alerts"]
```

---

## Featured case studies

### 1. Centralized Video Management System

**Problem.** Dahua NVRs cap the number of simultaneous connections. With many operators watching, NVRs refused new viewers.

**Solution.** A VMS that keeps **one** RTSP session per NVR channel, no matter how many operators watch it. MediaMTX opens the pull on the first viewer and closes it after the last one leaves, so idle channels use zero NVR slots.

```mermaid
flowchart LR
    OPS["Operators<br/>browser / Electron desktop"] -->|HTTPS| NGX["nginx"]
    NGX -->|/api| API["FastAPI<br/>auth, RBAC, inventory"]
    API --> PG[("PostgreSQL")]
    API -->|control API| MTX["MediaMTX"]
    NGX -->|WebRTC WHEP / HLS| MTX
    MTX -->|"1 RTSP pull per active channel"| NVR["Dahua NVRs"]
```

**My role.** Architecture, backend, deploy.
**Stack.** FastAPI, async SQLAlchemy, Alembic, PostgreSQL, MediaMTX, WebRTC (WHEP) with HLS fallback, React, Electron.
**Deploy.** Docker Compose in three modes (bridge, host network, fully offline for air-gapped sites), plus a native Windows build. GitHub Actions builds the Windows installer and the desktop client.

<details>
<summary>More details</summary>

- Channel paths are managed dynamically by the backend through the MediaMTX control API.
- Operator grids from 2×2 up to 64×64, patrol mode, saved layouts, snapshots.
- NVR credentials are encrypted at rest; passwords are hashed with argon2.
- Offline compose bundle for sites without internet access.

</details>

### 2. Inter-city air-cargo delivery platform

**Problem.** A logistics company delivers parcels between cities by plane. Two couriers per order (pickup to airport, airport to recipient) and flight data from an external system.

```mermaid
flowchart LR
    APP["Courier mobile app<br/>React Native"] -->|HTTPS| NGX["nginx + TLS"]
    ADM["Admin panel<br/>React + MapLibre"] --> NGX
    NGX --> API["FastAPI<br/>systemd service"]
    API --> PG[("PostgreSQL")]
    API --> S3[("MinIO<br/>photos, documents")]
    API --> FCM["Firebase<br/>push notifications"]
    EXT["Flight system"] -->|webhook| API
    API --> SCH["APScheduler jobs"]
    API -.->|errors, slow requests| GT["GlitchTip<br/>self-hosted"]
```

**My role.** Backend, infrastructure, deploy, monitoring (578 commits).
**Stack.** FastAPI, SQLAlchemy, Alembic, PostgreSQL (asyncpg), MinIO, APScheduler, Firebase Admin, OTP + JWT auth.
**Deploy.** systemd units behind nginx, Dockerfile and Compose for the backend, self-hosted GlitchTip in Docker for error tracking.

<details>
<summary>More details</summary>

- 17-status order lifecycle with QR codes and full history.
- Courier balances and payouts.
- Webhook integration with the flight schedule system.
- Scheduler failures and slow requests are reported to GlitchTip.

</details>

### 3. Network security toolkit with Wazuh integration (open source)

[![CI](https://github.com/yomarakesha/speedtest/actions/workflows/ci.yml/badge.svg)](https://github.com/yomarakesha/speedtest)

**[yomarakesha/speedtest](https://github.com/yomarakesha/speedtest)**: a Go CLI and terminal dashboard for network diagnostics and security audit. It grew into a microservice system: a Python orchestrator schedules discover and audit jobs, and Go services send findings to Wazuh.

```mermaid
flowchart LR
    CLI["Go CLI / TUI<br/>scan, audit, tlsaudit,<br/>dnssec, cvecheck, sniff"] -->|jobs| ORC["Python orchestrator<br/>FastAPI"]
    ORC --> AUD["audit service<br/>Go"]
    ORC --> SCN["scan service<br/>Go"]
    AUD -->|"findings, JSON"| WZ["Wazuh<br/>custom decoders + rules"]
    SCN --> WZ
    CLI -->|"--wazuh output"| WZ
```

**Stack.** Go, Python, FastAPI, Wazuh, Docker Compose, GitHub Actions, GoReleaser (Linux, macOS, Windows; amd64 + arm64).
**Highlights.** Port scan with banners and fingerprints, subnet discovery (MAC, vendor, SNMP), TLS audit and HTTP security headers graded A–F, DNSSEC/SPF/DMARC checks, CVE matching on banners, traceroute without root, bufferbloat test, packet capture.

### 4. CPU-only video analytics (open source)

**[yomarakesha/korgoz](https://github.com/yomarakesha/korgoz)**: a local-first video analytics platform. Cameras, then detection, tracking, face recognition, events, and analytics. Runs natively on systemd, without Docker, on plain CPUs.

```mermaid
flowchart LR
    CAM["Cameras<br/>RTSP / USB / file"] --> DET["Detection<br/>YOLOX, ONNX Runtime"]
    DET --> TRK["Tracking<br/>ByteTrack + Kalman"]
    TRK --> REC["Recognition<br/>YuNet + SFace"]
    REC --> QD[("Qdrant<br/>face vectors")]
    TRK --> EV["Event engine"]
    EV --> DB[("PostgreSQL")]
    DB --> API["FastAPI + React dashboard"]
```

**Stack.** Python, FastAPI, ONNX Runtime, OpenCV, Qdrant, PostgreSQL, SQLAlchemy, Alembic, React, systemd (API and worker units).
**Numbers.** Measured on an Intel Core Ultra 5 125U, CPU only: YOLOX-tiny handles 4 cameras with no frame loss at ~2.5 cores, p95 latency ~0.15 s.

---

## More production work

Client code is private. Short summaries:

| Project | What it is | Stack | Deploy |
|---|---|---|---|
| Parcel-locker platform | Backend, operator web, mobile app and a lock agent on the locker device | FastAPI, PostgreSQL, Flutter, Node | systemd agent on device, contract tests (Schemathesis) |
| Marketplace | Storefront, admin panel and mobile app for a national postal operator | FastAPI, MySQL, React, Expo | systemd + nginx |
| E-shop + CRM | Shop for IT and security hardware, admin CRM with RBAC | FastAPI, SQLite, React | systemd + nginx, GitHub Actions CI |
| Job board | Server-rendered, works without JavaScript on slow mobile networks | FastAPI, Next.js | Docker Compose |
| Legal and HR suite | Contract workflow, approvals, HR | Django REST (v1), then NestJS + Prisma + tRPC monorepo (pnpm, Turborepo), React | Docker Compose + nginx |

---

<sub>English · Русский по запросу</sub>

# Offline Dorm Camera — Project Handbook

**Documentation snapshot:** 2026-11-09  
**Status:** Live 1080p camera stream works through Frigate/go2rtc with Intel VAAPI H.264 encoding. Live video is somewhat delayed/choppy. Person detection with OpenVINO is the next task; its successful deployment has **not been confirmed**. Recording is intentionally disabled until encrypted storage is ready.

> This repository documents a *private, consent-based* indoor camera system. Obtain permission from everyone who may be recorded and comply with dorm/university rules. Do not place cameras in bathrooms or other places where privacy is expected. Disable recording and streaming when consent is absent.

## Project objective

Build an affordable, locally operated, headless indoor security camera that can:

1. Show a live camera feed to an authorized local viewer without cloud dependency.
2. Detect people/motion locally, ideally on the Intel integrated GPU.
3. Record video to a **256 GB high-endurance microSD card** encrypted with LUKS2, targeting approximately **seven days** of retention (to be validated).
4. Run reliably on a CTL Chromebox with Debian, Docker, Frigate and go2rtc.
5. Operate without internet access after provisioning, including a possible direct Ethernet connection to a Windows laptop.
6. Be mounted non-destructively (planned Command-style shelf/mount), with webcam privacy cover available.
7. Remain below an approximately $100 initial compute-device budget; other peripherals/storage affect total cost.

## Documentation map

| File | Purpose |
|---|---|
| `01-hardware-and-environment.md` | Inventory, OS, devices, network, assumptions |
| `02-architecture-and-stack.md` | Pipeline, roles, ports, trust boundaries |
| `03-configurations.md` | Known-good and current candidate config, restore instructions |
| `04-timeline-and-evidence.md` | What happened, commands, logs, performance |
| `05-roadmap.md` | Phased work, acceptance tests, decision gates |
| `06-storage-encryption-and-retention.md` | LUKS2 design, mounting, retention math, recovery |
| `07-security-privacy-and-offline.md` | Threat model, hardening, offline tests, consent |
| `08-operations-and-troubleshooting.md` | Runbook, monitoring, failure diagnosis |
| `09-open-questions-and-handoff.md` | Unknowns, priorities, next-session checklist |

## Current state at a glance

| Component | Status | Evidence / caveat |
|---|---|---|
| Chromebox firmware/OS | Working | Full-ROM UEFI firmware; Debian 13 |
| USB webcam | Working | `/dev/video0`, 1080p MJPEG capture |
| Frigate container | Working | `ghcr.io/blakeblackshear/frigate:stable`, observed 0.18.2 |
| go2rtc RTSP restream | Working | Local RTSP input `rtsp://127.0.0.1:8554/dorm_cam` |
| Intel VAAPI H.264 encoding | **Confirmed** | Successful host and container FFmpeg tests, live encoder process |
| Live viewing | Working with issues | User reports some delay and choppiness |
| 15 FPS output filter | Applied | Did not significantly reduce CPU |
| OpenVINO person detection | **Unverified** | Configuration proposed, no resulting logs yet |
| Continuous/event recording | Disabled | `record.enabled: false` |
| 256 GB microSD | Planned / arrival unconfirmed | Do not assume installed |
| LUKS2 encrypted media | Not implemented | Need threat model, mount and boot behavior |
| Fully disconnected operation | Not proven | LAN setup working; direct Ethernet and no-internet tests pending |
| Camera physical mount | Planned | No confirmation of final mount |

## Non-goals and boundaries

- No cloud NVR, cloud AI, or external remote viewing requirement.
- No facial recognition or identifying particular individuals.
- No covert monitoring. Consent, transparency and access control are requirements.
- No assumption that a webcam's privacy cover is remotely actuated.
- No claim of seven-day retention until bitrate, storage overhead, and actual workload are measured.

## Suggested next action

Check whether OpenVINO changes were actually saved and whether the detector initialized. **Do not assume the previous suggested config was deployed.** Run the diagnostics in `05-roadmap.md`, inspect the current YAML and logs, and make one change at a time with a rollback copy.
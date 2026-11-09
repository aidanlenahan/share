# Open Questions, Evidence Gaps and Handoff

## Highest-priority unknowns

1. **Was OpenVINO config actually applied?** Last user message before documentation request was a plan, not detector logs.
2. Does `/openvino-model/ssdlite_mobilenet_v2.xml` exist in the running image, and is its labelmap correct for this Frigate version?
3. What is the actual camera output FPS and live-view latency? User reports delayed/choppy playback.
4. Does the GPU handle concurrent VAAPI H.264 encode/decode and OpenVINO inference reliably?
5. Is the 256 GB high-endurance microSD purchased/installed, and what is its model and endurance rating?
6. Should recording be continuous or event-only, and what retention/privacy policy is acceptable?
7. Should encrypted media unlock manually (stronger theft protection) or automatically (unattended recovery)?
8. Where will Frigate metadata, snapshots, temporary data and logs reside, and must those be encrypted too?
9. Is the final network an isolated direct Ethernet link or a private router LAN?
10. Who is authorized to view the feed, and what is the consent/physical-disable procedure?

## What must not be assumed

- Person detection is not yet proven working.
- Recording is not yet enabled.
- LUKS2 is not configured.
- Seven-day retention is a target, not an observed result.
- Fully offline operation has not been demonstrated.
- No claim that latency/choppiness is resolved.
- Current YAML content must be inspected on-device; this documentation is a reconstruction.

## Handoff: one-paragraph state

A CTL CBx1-7 Chromebox (i7-8550U, 8 GB RAM, Debian 13) is running Frigate 0.18.2 in Docker with an AOC USB MJPEG webcam at 1920×1080. go2rtc launches a custom FFmpeg `exec:` command that explicitly initializes `/dev/dri/renderD128` VAAPI and encodes H.264 with `h264_vaapi`; the live stream works via Frigate HTTPS at the previously observed LAN IP `192.168.8.223:8971`. Container CPU averages ~101% and memory ~1.02 GiB; output is filtered to 15 FPS but CPU did not significantly improve, and video is somewhat delayed/choppy. Recording remains disabled. The next phase is to validate/enable OpenVINO GPU person detection at 5 FPS, then provision LUKS2 encrypted microSD recording, verify retention and truly offline direct-Ethernet operation. Keep consent/privacy central.

## Commands to run at start of next session

```bash
cd /opt/frigate
printf '\n=== Compose ===\n'; cat compose.yaml
printf '\n=== Frigate config ===\n'; cat config/config.yml
printf '\n=== Services ===\n'; docker compose ps
printf '\n=== Container resources ===\n'; docker stats --no-stream frigate
printf '\n=== Recent logs ===\n'; docker compose logs --tail=120 frigate
printf '\n=== Models ===\n'; docker exec frigate ls -l /openvino-model
printf '\n=== Storage ===\n'; lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
```

Review output for secrets before sharing. If OpenVINO is not yet configured, first create a dated backup and add detector/model sections in a controlled change. If it is configured, diagnose logs and verify actual person boxes before progressing.

## Suggested future additions to this repository

- Sanitized real config exports (`config/compose.yaml`, `config/config.yml`) after confirming exact device state.
- `CHANGELOG.md` for each tested change, including before/after measurements.
- `benchmarks/` with FPS, CPU, RAM, GPU and end-to-end latency data.
- `storage/` with confirmed card identity, LUKS2 UUID, mount strategy and recovery procedure (never keys).
- `network/` with final offline subnet and firewall policy.
- `deployment/` with mount photos, power/thermal checks and consent procedure (avoid publishing private images).
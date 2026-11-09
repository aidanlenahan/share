# Operations and Troubleshooting Runbook

## Start / stop / status

```bash
cd /opt/frigate
docker compose ps
docker compose up -d
docker compose stop frigate
docker compose restart frigate
docker stats --no-stream frigate
docker compose logs --tail=150 frigate
```

`docker compose restart` does **not** apply Compose environment/device/volume changes. Use `docker compose up -d --force-recreate` after those changes.

## Inspect FFmpeg and detection

```bash
docker exec frigate ps -eo pid,pcpu,rss,args | grep '[f]fmpeg'
docker compose logs --since=5m frigate 2>&1 | grep -iE 'error|failed|vaapi|openvino|detector|dorm_cam'
docker exec frigate ls -l /dev/video0 /dev/dri/renderD128
```

A successful custom encoder command should include:

```text
-init_hw_device vaapi=va:/dev/dri/renderD128
-filter_hw_device va
-f v4l2 -input_format mjpeg -video_size 1920x1080
-vf fps=15,format=nv12,hwupload
-c:v h264_vaapi
```

## Diagnostic decision tree

**No live frames:**

1. `docker compose ps`: container up?
2. `docker compose logs`: Frigate config parsing or go2rtc errors?
3. `docker exec frigate ps ...`: custom FFmpeg running?
4. Check `/dev/video0` and GPU render node accessible inside container.
5. Check whether another process owns webcam.
6. Check local RTSP source configuration; 404 may indicate encoder never published.
7. Roll back to last known-good config if needed.

**`A hardware device reference is required to upload frames to`:**

- Known failed path: go2rtc's automatic `#hardware=vaapi` V4L2 pipeline.
- Known successful path: explicit `-init_hw_device vaapi=va:/dev/dri/renderD128` and `-filter_hw_device va` in custom exec.

**High CPU:**

- Compare encoder process vs Frigate decoder/detector processes.
- Hardware H.264 encoding does not eliminate CPU MJPEG decode.
- 15 FPS output filter alone did not lower overall CPU materially.
- Measure with stable workloads over time; don't infer from one snapshot.

**Delayed/choppy video:**

- Known issue, not yet fixed.
- Measure actual delivered FPS and latency, USB input errors, FFmpeg output FPS, RTSP buffering and browser performance.
- Avoid changing resolution/codec until a before/after measurement plan exists.

**OpenVINO errors:**

- Check installed model files and correct path.
- Check Intel GPU availability and OpenVINO device selection.
- Confirm model input shape and pixel format match Frigate version.
- Temporarily disable detector or use CPU fallback to isolate GPU contention.

**Recordings missing:**

- Expected now: recording is disabled.
- Later: confirm LUKS mapper open, mount present, container bind mount correct, writable filesystem, sufficient space and retention policy.

## Useful host commands

```bash
journalctl -u docker --since '1 hour ago' --no-pager
journalctl -k --since '1 hour ago' --no-pager
lsblk -f
findmnt
ip -brief addr
ss -lntp
uptime
free -h
```

## Tested FFmpeg hardware encoder command

With Frigate stopped (to release webcam):

```bash
docker compose run --rm --no-deps \
  --entrypoint /usr/lib/ffmpeg/8.0/bin/ffmpeg \
  frigate \
  -hide_banner \
  -init_hw_device vaapi=va:/dev/dri/renderD128 \
  -filter_hw_device va \
  -f v4l2 -input_format mjpeg \
  -video_size 1920x1080 -framerate 15 \
  -i /dev/video0 \
  -vf 'format=nv12,hwupload' \
  -c:v h264_vaapi -t 10 -f null -
```

This command completed successfully on the Frigate image; webcam negotiated 30 FPS and output approximately 15 FPS in the test. Start Frigate again afterward: `docker compose up -d`.

## Backup / rollback

- Prior Compose backup: `/opt/frigate/compose.yaml.backup`.
- Prior software config backup: `/opt/frigate/config/config.yml.backup`.
- Proposed pre-OpenVINO backup: `/opt/frigate/config/config.yml.pre-openvino` (existence unconfirmed).
- Preserve a dated copy of the **current working VAAPI exec config** before any changes.
- Validate Compose with `docker compose config -q`; Frigate-specific validation requires application startup/log review.

## Maintenance cadence

- After changes: check stream, logs, CPU, memory and access control.
- Weekly: check storage free space, card errors, unexpected restarts, detection events.
- Monthly: review logs, firmware/software update policy and encryption backup procedures.
- Before extended offline operation: prefetch updates, export config and verify cold-boot recovery.
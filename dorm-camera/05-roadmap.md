# Implementation Roadmap and Acceptance Tests

## Phase 0 — Preserve known-good state (immediate)

- [ ] Confirm current files: `cat /opt/frigate/compose.yaml` and `cat /opt/frigate/config/config.yml`.
- [ ] Back up both with dated filenames and ideally store a copy off-device, excluding secrets.
- [ ] Verify camera stream, dashboard access, logs, and resource baseline.
- [ ] Record Frigate image digest/version, Debian version, kernel, and Docker versions.
- [ ] Ensure `record.enabled: false` remains in effect.

**Exit criterion:** Known-good rollback exists and feed works after restart.

## Phase 1 — Local OpenVINO person detection (next)

- [ ] Check whether proposed OpenVINO YAML has actually been applied.
- [ ] Verify bundled model paths in container (`/openvino-model/...`) and available GPU device.
- [ ] Confirm detector config matches installed Frigate version.
- [ ] Enable OpenVINO detector on GPU; track `person` only; keep recording off.
- [ ] Restart and inspect startup logs for successful detector initialization.
- [ ] Verify person boxes in Debug view and sensible inference times.
- [ ] Measure CPU/RAM/GPU load with and without a person present.
- [ ] If GPU inference conflicts with video encode/decode, compare CPU OpenVINO inference as a fallback; do not assume it is better.
- [ ] Evaluate false positives/negatives in actual lighting conditions, including night/low light.

**Exit criterion:** Person detection demonstrably works locally without cloud, with manageable resource use and no unacceptable new feed failures.

Suggested checks:

```bash
cd /opt/frigate
docker compose ps
docker compose logs --since=5m frigate | grep -iE 'openvino|detector|inference|error|failed'
docker stats --no-stream frigate
docker exec frigate ps -eo pid,pcpu,rss,args | grep -E '[f]fmpeg|[o]penvino'
docker exec frigate ls -l /openvino-model
```

## Phase 2 — Video quality / latency (deferred by user)

- [ ] Measure actual input, encoded output, detection, and displayed FPS separately.
- [ ] Determine end-to-end live-view latency with a visible clock/timer test.
- [ ] Check whether USB bandwidth, malformed MJPEG, software decode, RTSP buffering or browser decoding is limiting.
- [ ] Consider lower-resolution detection path while keeping higher-resolution viewing/recording.
- [ ] Optionally test YUYV 1280×720 at 10 FPS and compare CPU, latency, detail.
- [ ] Compare hardware-encode output bitrates and GOP sizes; optimize only if benefit is measurable.

**Exit criterion:** Define acceptable latency and visual smoothness; do not claim resolved until tested.

## Phase 3 — Encrypted microSD storage

- [ ] Confirm card model, endurance rating, actual capacity, block device identity and health.
- [ ] Back up anything on card; partitioning and LUKS formatting **erase data**.
- [ ] Decide manual unlock vs auto-unlock; document theft and reboot tradeoffs.
- [ ] Create LUKS2 volume, filesystem and stable mount point (details in storage document).
- [ ] Map **only** intended recording data to encrypted mount, avoiding silent fallback to internal SSD.
- [ ] Configure service startup ordering so recording never writes unencrypted when card is locked/unmounted.
- [ ] Configure Frigate retention and reserve space; validate with real recorded bitrate.
- [ ] Test unclean shutdown, reboot, card removal, full disk, and recovery.

**Exit criterion:** Video files are written to the encrypted card, inaccessible without unlock, and no recordings leak to unencrypted fallback.

## Phase 4 — Motion/person-triggered and/or continuous recording

- [ ] Decide continuous vs event-only recording (affects retention and privacy).
- [ ] Enable recording only after encrypted mount is verified.
- [ ] Tune retention, snapshots, event settings, and minimum free space.
- [ ] Verify file creation, playback, deletion, and oldest-first retention behavior.
- [ ] Benchmark at day/night and during movement; calculate real storage use.

**Exit criterion:** Desired capture policy works and measured retention is close to target.

## Phase 5 — Fully offline local network

- [ ] Choose dedicated private subnet for direct laptop-to-Chromebox Ethernet (example `192.168.50.0/24`; not yet configured).
- [ ] Set static IPs or local DHCP; avoid conflicting subnets.
- [ ] Test dashboard, SSH, RTSP internally if needed, and detection without WAN.
- [ ] Ensure all required images/models are cached; no DNS/cloud dependency.
- [ ] Check clocks/timestamps after prolonged power-off.
- [ ] Restrict UI and SSH access to authorized endpoint(s).

**Exit criterion:** All required functions work with WAN physically disconnected and no outside routes.

## Phase 6 — Physical deployment and reliability

- [ ] Confirm informed consent and dorm policy compliance.
- [ ] Install secure non-drilling mount and cable strain relief.
- [ ] Place camera away from private areas; provide obvious disable/privacy procedure.
- [ ] Configure safe power recovery, thermals, and startup behavior.
- [ ] Test 24–72 hour uptime, logs, storage write rate and reboot recovery.
- [ ] Document maintenance and emergency shutdown instructions.

**Exit criterion:** Reliable, consent-based operation with an owner-maintainable runbook.

## Priority order

1. Verify/enable OpenVINO detection.
2. Implement encryption and safe mount behavior.
3. Enable/validate recording and retention.
4. Prove no-internet/direct-Ethernet operation.
5. Return to latency and video optimization if needed.
6. Physical installation and burn-in.
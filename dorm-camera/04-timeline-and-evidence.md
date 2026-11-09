# Chronological Work Log and Evidence

## Initial design and provisioning

1. Defined objective: offline indoor camera for girlfriend's dorm, private local viewing, person/motion detection, encrypted microSD, no drilling, low cost.
2. Selected CTL CBx1-7 Chromebox (~$93), AOC 4K USB webcam, intended 256 GB high-endurance microSD.
3. Disabled firmware write protection; used MrChromebox firmware to install UEFI Full ROM.
4. Installed Debian 13, configured Ethernet, SSH, Docker and Docker Compose.
5. Exposed `/dev/video0` and `/dev/dri/renderD128` to Frigate container.
6. Confirmed Frigate UI responsive and camera ingest functioning with software H.264 encoding.

## Original software encoding baseline

- go2rtc source: `ffmpeg:device?video=0&video_size=1920x1080#video=h264`.
- Container CPU: **133.25%**.
- Container memory: **1.122 GiB / 7.656 GiB**.
- `libx264` FFmpeg encoder process: approximately 99.9% CPU.
- Frigate RTSP decoding pipeline used VAAPI, roughly 9% CPU.
- Stream frame delivery appeared limited (earlier observation around 10 FPS; not a controlled measurement).

## Failed go2rtc automatic VAAPI attempt

Source changed to:

```text
ffmpeg:device?video=0&video_size=1920x1080&framerate=15#video=h264#hardware=vaapi
```

Generated FFmpeg command lacked an initialized hardware device for its `hwupload` filter. Relevant errors:

```text
[hwupload] A hardware device reference is required to upload frames to.
[AVFilterGraph] Error initializing filters
Error opening output files: Invalid argument
ioctl(VIDIOC_QBUF): Bad file descriptor
```

No frames reached Frigate; subsequent RTSP 404/watchdog errors were downstream symptoms.

## Successful host VAAPI test

Frigate stopped to release webcam, then host command:

```bash
ffmpeg -hide_banner \
  -init_hw_device vaapi=va:/dev/dri/renderD128 \
  -filter_hw_device va \
  -f v4l2 -input_format mjpeg \
  -video_size 1920x1080 -framerate 15 \
  -i /dev/video0 \
  -vf 'format=nv12,hwupload' \
  -c:v h264_vaapi -t 10 -y /tmp/vaapi-test.mp4
```

Result: **151 frames**, ~10 seconds, ~9.7 MiB file, **8.124 Mbps** average, **0.989x** speed. Driver changed capture request from 15 to 30 FPS. MJPEG APP field warnings occurred but output completed.

## Successful container VAAPI test

```bash
docker compose run --rm --no-deps \
  --entrypoint /usr/lib/ffmpeg/8.0/bin/ffmpeg frigate \
  -hide_banner \
  -init_hw_device vaapi=va:/dev/dri/renderD128 \
  -filter_hw_device va \
  -f v4l2 -input_format mjpeg \
  -video_size 1920x1080 -framerate 15 \
  -i /dev/video0 \
  -vf 'format=nv12,hwupload' \
  -c:v h264_vaapi -t 10 -f null -
```

Result: **151 frames**, 9.93 seconds, ~0.982x speed, no fatal hardware error. Warnings: `overread 8`, `EOI missing, emulating`; FFmpeg output identified `h264_vaapi`.

## Successful go2rtc custom exec deployment

- Added `GO2RTC_ALLOW_ARBITRARY_EXEC: "true"` to Compose.
- Added explicit `exec:/usr/lib/ffmpeg/8.0/bin/ffmpeg` stream with `-init_hw_device`, `-filter_hw_device`, V4L2 MJPEG and `h264_vaapi`.
- `docker compose config -q` succeeded; container recreated.
- User confirmed: **"its working again"**.
- Process listing confirmed encoder running with VAAPI and publishing RTSP.
- Container CPU samples: **102.40%, 103.98%**.
- Memory samples: **888 MiB, 1.036 GiB** (startup variability).
- Encoder process: **~69–72% CPU**; Frigate decoder ~8% CPU.

## 15 FPS output filter experiment

Changed:

```text
-vf format=nv12,hwupload
```

to:

```text
-vf fps=15,format=nv12,hwupload
```

Restarted container; process listing confirmed the new filter was active. Encoder process ~73.9% CPU; container CPU ~101.95% and 105.48% in initial samples. Therefore reducing output frame rate **did not materially reduce CPU**. The MJPEG input still arrives at 30 FPS.

## Repeated steady-state resource samples

19 CPU readings (% of one logical CPU core):

```text
105.48 100.92 105.46 95.16 91.44 102.37 100.16
101.61 103.85 102.68 103.74 97.46 102.93 107.70
97.34 103.62 89.58 100.42 99.30
```

- Arithmetic mean: approximately **100.7%**.
- Minimum/maximum: **89.58% / 107.70%**.
- Memory stabilized around **1.015–1.022 GiB**, approximately 13.3% of reported limit.
- No obvious progressive memory growth across these snapshots; this is **not** proof of long-term stability.

## Current UX and next phase

User reported the feed is **"a bit delayed and choppy"**, and chose to defer further video optimization.

OpenVINO person detection was then proposed with `device: GPU`, bundled SSD Lite MobileNet model, person-only tracking, 5 FPS detect, recording disabled. **There is no user-provided confirmation of successful deployment or logs from this phase.**

## Interpretations and limits

- Docker CPU 100% corresponds approximately to one logical CPU, not the entire 8-thread processor.
- CPU percentages for processes are snapshots; do not sum them across different measurement windows as if they were exact.
- VAAPI hardware encoding is confirmed; CPU MJPEG decode remains a likely cost but has not been profiled rigorously.
- The reported choppiness may be related to capture, processing, RTSP buffering, browser playback or network. Cause unknown.
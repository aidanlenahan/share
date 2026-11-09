# Configuration Reference and Rollback

> **Snapshot caveat:** These are configurations reconstructed from commands and process listings shared in chat, **not a fresh read of files currently on the device**. Verify with `cat` before treating them as authoritative. The OpenVINO configuration below was suggested but its application is unconfirmed.

## Directory structure

```text
/opt/frigate/
├── compose.yaml
├── compose.yaml.backup              # user created
├── config/
│   ├── config.yml
│   ├── config.yml.backup            # earlier software-encoder backup
│   └── config.yml.pre-openvino      # proposed backup; existence unverified
└── media/                           # temporary/current media volume
```

## Docker Compose — last known shape

```yaml
services:
  frigate:
    container_name: frigate
    image: ghcr.io/blakeblackshear/frigate:stable
    restart: unless-stopped
    shm_size: "256mb"
    environment:
      GO2RTC_ALLOW_ARBITRARY_EXEC: "true"
    devices:
      - /dev/video0:/dev/video0
      - /dev/dri/renderD128:/dev/dri/renderD128
    ports:
      - "8971:8971"
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ./config:/config
      - ./media:/media/frigate
      - type: tmpfs
        target: /tmp/cache
        tmpfs:
          size: 268435456
```

`environment` was added by user and a working custom FFmpeg process confirms the feature was enabled. Exact YAML placement/whitespace should still be verified.

## Camera configuration — last verified working stream, detection OFF

```yaml
mqtt:
  enabled: false

go2rtc:
  streams:
    dorm_cam:
      - >-
        exec:/usr/lib/ffmpeg/8.0/bin/ffmpeg
        -hide_banner -loglevel warning
        -init_hw_device vaapi=va:/dev/dri/renderD128
        -filter_hw_device va
        -f v4l2
        -input_format mjpeg
        -video_size 1920x1080
        -framerate 30
        -i /dev/video0
        -vf fps=15,format=nv12,hwupload
        -c:v h264_vaapi
        -b:v 3000k
        -maxrate 4000k
        -bufsize 8000k
        -g 30
        -an
        -rtsp_transport tcp
        -f rtsp
        {{output}}

cameras:
  dorm_cam:
    enabled: true
    ffmpeg:
      inputs:
        - path: rtsp://127.0.0.1:8554/dorm_cam
          input_args: preset-rtsp-restream
          roles:
            - detect
    detect:
      enabled: false
      width: 1920
      height: 1080
    record:
      enabled: false
```

**Why this is the baseline:** The user confirmed video was working after custom VAAPI configuration, and process listings subsequently confirmed `-vf fps=15,format=nv12,hwupload`. The feed was reported somewhat delayed/choppy.

## OpenVINO proposal — NOT YET VERIFIED

The following was suggested as an addition to the same config, not proven to have been deployed:

```yaml
detectors:
  ov:
    type: openvino
    device: GPU

model:
  width: 300
  height: 300
  input_tensor: nhwc
  input_pixel_format: bgr
  path: /openvino-model/ssdlite_mobilenet_v2.xml
  labelmap_path: /openvino-model/coco_91cl_bkgr.txt
```

Camera changes proposed:

```yaml
cameras:
  dorm_cam:
    # Retain the EXISTING ffmpeg input and other camera fields
    detect:
      enabled: true
      width: 1920
      height: 1080
      fps: 5
    objects:
      track:
        - person
    record:
      enabled: false
```

**Do not paste the partial `cameras:` example over the entire existing camera block.** It omits the FFmpeg input intentionally. Validate the selected model's exact path and label map against the installed Frigate image before starting. Frigate releases can change defaults and bundled assets.

## Previous software-encoding fallback

```yaml
go2rtc:
  streams:
    dorm_cam:
      - "ffmpeg:device?video=0&video_size=1920x1080#video=h264"
```

This worked but consumed approximately 133% total container CPU, with a `libx264` process near 100%. The backup file `config/config.yml.backup` was created before a failed VAAPI attempt; verify its contents before restoring.

## Failed automatic go2rtc VAAPI setting

```yaml
go2rtc:
  streams:
    dorm_cam:
      - "ffmpeg:device?video=0&video_size=1920x1080&framerate=15#video=h264#hardware=vaapi"
```

This **failed** with `A hardware device reference is required to upload frames to`, followed by RTSP DESCRIBE 404 and Frigate camera watchdog errors. Do not revert to it.

## Safe edit / validate / rollback

```bash
cd /opt/frigate
cp compose.yaml "compose.yaml.$(date +%Y%m%d-%H%M%S).bak"
cp config/config.yml "config/config.yml.$(date +%Y%m%d-%H%M%S).bak"
nano config/config.yml
docker compose config -q  # validates Compose only, NOT Frigate's YAML schema
# Frigate application config is validated on container startup; inspect logs
docker compose up -d --force-recreate
docker compose logs --tail=150 frigate
```

If a change breaks the feed, restore the most recent verified YAML backup and restart. Keep a copy of the working `exec:` configuration before enabling detection or encrypted media.
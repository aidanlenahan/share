# Architecture and Software Stack

## Data flow

```text
AOC USB webcam (/dev/video0; MJPEG 1920x1080 @ 30 fps)
        |
        v
FFmpeg process launched by go2rtc (inside Frigate container)
  - V4L2 MJPEG input
  - CPU MJPEG decode / pixel format conversion
  - fps=15 filter (current candidate)
  - upload NV12 frames to Intel GPU (/dev/dri/renderD128)
  - H.264 hardware encode with h264_vaapi
        |
        v
Local RTSP publish to go2rtc (127.0.0.1:8554)
        |
        +----> Frigate FFmpeg camera input
        |        - RTSP restream
        |        - VAAPI-assisted decode
        |        - detection pipeline at 5 fps
        |        - OpenVINO inference: PLANNED / UNVERIFIED
        |        - recording: DISABLED
        |
        +----> Local authenticated live view (Frigate web UI)
```

## Why these components

| Layer | Technology | Purpose |
|---|---|---|
| Host OS | Debian 13 | Headless Linux, device and storage control |
| Container runtime | Docker Engine + Compose | Reproducible deployment and restart policy |
| NVR / UI | Frigate (`stable`, observed 0.18.2) | Camera ingest, detection orchestration, live UI, future recording |
| Stream broker | go2rtc (observed 1.9.14) | Convert USB V4L2 webcam into RTSP stream |
| Video conversion | FFmpeg 8.0 bundled in Frigate | Decode MJPEG, convert format, encode H.264 |
| Hardware codec | Intel VAAPI | GPU-assisted H.264 encode and decode |
| Object detector | OpenVINO (proposed) | Local person inference on Intel GPU |
| Encrypted media | LUKS2 + ext4 (proposed) | Encrypt recorded media at rest |
| Connectivity | Ethernet | Local-only management/viewing |

## Important technical nuance

`h264_vaapi` confirms **hardware H.264 encoding**, not an entirely GPU-driven pipeline. USB webcam MJPEG frames are still software decoded, pixel-converted and uploaded. In process listings, the live encoder used roughly 69–74% of a logical CPU. Overall container CPU hovered around 100% even after reducing output FPS. Some latency/choppiness remains; the exact cause has not been isolated.

## Ports and trust boundaries

- **8971/TCP**: Frigate HTTPS UI; published in Compose.
- **8554/TCP**: go2rtc RTSP inside container, used via loopback by Frigate. Not published in the known Compose config.
- Other Frigate/go2rtc internal ports may exist; **do not publish them without a specific reason**.
- `GO2RTC_ALLOW_ARBITRARY_EXEC=true` is required for the custom `exec:` stream; this increases risk if an attacker can edit the go2rtc configuration or access its administrative interface. Keep configuration writable only by trusted administrators, and limit network exposure.
- Docker container maps host webcam and GPU render node, so access to Docker and the container should be considered privileged.

## Desired final architecture

```text
[Webcam] -> [Chromebox: Frigate + go2rtc + VAAPI + OpenVINO]
                     |                      |
                     |                      +-> local event metadata
                     +-> LUKS2 encrypted microSD: recordings
                     |
                     +-> Ethernet-only local viewing/administration
                              |
                              +-> authorized laptop/browser
```

**Boot design question:** If encrypted media is unlocked manually, unattended restart cannot automatically resume recording until someone supplies the passphrase. Auto-unlock can improve availability but may weaken protection against theft if the key is stored on the same device. This must be decided explicitly.

## Dependency considerations

- Container image and model assets must be cached before disconnecting the internet.
- Local time should remain correct for event timestamps; choose RTC/manual time setup or trusted local time source.
- Browser may warn on self-signed HTTPS certificate; verify endpoint identity before accepting.
- Verify that OpenVINO GPU and VAAPI can coexist under sustained load.
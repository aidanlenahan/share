# Hardware and Environment

## Compute device

- **Model:** CTL CBx1-7 Chromebox, platform WUKONG/FIZZ (Kaby Lake family).
- **Processor:** Intel Core i7-8550U, 4 physical cores / 8 threads, nominal base clock 1.8 GHz.
- **GPU:** Intel UHD Graphics 620; VAAPI H.264 encode/decode capabilities observed.
- **Memory:** 8 GB RAM (Docker reports approximately 7.656 GiB available as container limit).
- **Internal storage:** 128 GB SSD (capacity stated; actual partitions/free space not yet documented).
- **Removable storage:** microSD slot, intended 256 GB high-endurance card, **not confirmed installed**.
- **Acquisition price:** approximately $93 for Chromebox (reported).

## Firmware / operating system history

- Original ChromeOS firmware family: `Google_Fizz.10139.202.0`, dated 2024-01-12.
- Firmware write protection disabled (`WP 0`).
- MrChromebox process: RW_LEGACY used earlier, then UEFI Full ROM firmware.
- Current operating system: **Debian 13 (trixie)**, headless, managed through SSH.
- Host prompt: `root@debcam:/opt/frigate#`.
- Missing firmware warning previously noted: `intel/avs/hda-8086280b-tplg.bin` (audio-related; no evidence it prevents camera function).

## Camera

- **Product:** AOC 4K USB webcam, white, approximately 80° field of view, physical privacy cover.
- **Reported identifier:** XIFT AC310, USB ID `5843:e819`.
- **Device nodes:** `/dev/video0`, `/dev/video1` (the actual capture device used is `/dev/video0`).
- **Capture format:** MJPEG up to 3840×2160 at 30 FPS, 1920×1080 at 30 FPS.
- **Alternative format:** YUYV supported at lower frame rates/resolutions; prior discussion suggests 1280×720 at 10 FPS, **not yet validated by a successful encoding test**.
- **Observed behavior:** `-framerate 15` request at 1080p MJPEG is renegotiated by driver to **30 FPS**.
- **Observed malformed JPEG warnings:** `unable to decode APP fields`, `overread`, `EOI missing`; tests still encoded video. Assess actual visual artifacts.

## GPU and video devices

- Render node: `/dev/dri/renderD128`.
- Host verification: `vainfo --display drm --device /dev/dri/renderD128` indicated H.264 encode/decode support.
- Device exposed to container in Compose.
- Host FFmpeg and Frigate-bundled FFmpeg have both successfully used `h264_vaapi`.

## Network

- Ethernet interface: `eno0`.
- DHCP LAN address observed: `192.168.8.223/24`; gateway `192.168.8.1`.
- UI used: `https://192.168.8.223:8971`.
- This address is **not permanent** unless DHCP reservation or static IP configured.
- Planned final topology may be a direct wired connection to a Windows laptop, with static addresses and no internet route.
- **Important distinction:** Access on a private LAN is not the same as proven offline operation.

## Physical installation

- Intended location: indoor dorm room.
- Mount: non-drilling Command shelf or equivalent, pending load and adhesive suitability review.
- Ensure webcam does not fall, block ventilation, or capture private areas.
- Cable strain relief and placement of the Chromebox/power adapter still need to be documented.

## Useful discovery commands

```bash
cat /etc/os-release
uname -a
lscpu
free -h
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,MODEL
lsusb
ls -l /dev/video* /dev/dri/*
ip -brief addr
ip route
v4l2-ctl --device /dev/video0 --list-formats-ext
vainfo --display drm --device /dev/dri/renderD128
```

Do not paste credentials, session tokens, or encryption keys into issue trackers or AI chats.
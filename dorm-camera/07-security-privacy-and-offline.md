# Security, Privacy and Offline Operation

## Privacy requirement

This is a dorm-room camera. All people whose private space might be captured should know about it and consent to its operation. Obtain any university/dorm permissions required. Use the physical privacy cover or power disconnect when the camera is not needed. Avoid recording roommates, visitors or intimate activity without explicit consent; do not install hidden or covertly.

## Threat model

| Threat | Mitigation / remaining issue |
|---|---|
| Internet/cloud disclosure | No cloud components; prove WAN disconnected; block outbound traffic |
| Unauthorized local viewer | Authenticated Frigate UI, firewall restrictions, strong credentials |
| Stolen microSD | LUKS2 encryption and strong passphrase |
| Stolen whole device | Manual unlock is stronger than key stored on internal SSD |
| Someone edits go2rtc config | Protect files and admin UI; custom exec permits arbitrary commands |
| Sensitive metadata on SSD | Audit Frigate DB, thumbnails, logs, swap, temporary files |
| Physical tampering | Visible installation, locked/controlled access, tamper awareness |
| Camera accidentally stays active | Privacy cover, obvious power switch, documented shutdown |
| Compromised SSH account | Key-based auth, limited access, security updates before offline deployment |

## Custom go2rtc exec security

`GO2RTC_ALLOW_ARBITRARY_EXEC: "true"` is currently needed to launch the explicit FFmpeg command that initializes VAAPI correctly. This is a security-sensitive capability: someone able to change go2rtc streams may be able to run commands inside the container. Restrict configuration file ownership, management access, exposed ports, and users with Docker privileges. Do not expose go2rtc's administrative API to untrusted networks.

## Network hardening checklist

- [ ] Change default passwords; use unique strong credentials.
- [ ] Restrict SSH to authorized laptop and consider public-key-only authentication.
- [ ] Restrict Frigate HTTPS to local subnet or a single host.
- [ ] Do not publish RTSP/go2rtc admin ports unless necessary.
- [ ] Confirm no router port forwarding, UPnP exposure, or public tunnels.
- [ ] Confirm container and host do not require WAN to boot and operate.
- [ ] Install/update images and packages before permanent offline deployment.
- [ ] Consider a host firewall, with a tested recovery path before enabling it.
- [ ] Keep time reasonably accurate for timestamps and certificate behavior.
- [ ] Store backup configurations without passwords or keys.

## How to prove offline operation

1. Verify Docker image, OpenVINO model and required dependencies already exist locally.
2. Disconnect WAN physically (not just close a browser tab).
3. Check host routes and DNS; ensure no path to public internet.
4. From authorized laptop, access Frigate UI and SSH over the intended private link.
5. Confirm live video, detection and recording continue.
6. Restart both devices while WAN remains absent and repeat.
7. Confirm timestamps are correct enough for operational use.
8. Optionally monitor outbound packets during testing to detect attempted cloud connections.

## Direct Ethernet design (not yet implemented)

Example isolated addresses:

- Windows laptop: `192.168.50.1/24`
- Chromebox `eno0`: `192.168.50.2/24`
- No default gateway or DNS needed for direct-IP access.

These are **illustrative**, not current settings. If Windows shares its internet connection or bridges adapters, the link may no longer be isolated. Use explicit firewall rules if isolation is required.

## HTTPS considerations

Frigate HTTPS on port 8971 may use a certificate not trusted by the browser. Avoid casually ignoring certificate warnings on a shared network; confirm the correct device endpoint. Local certificates or a pinned trust workflow can improve confidence without cloud dependency.

## Retention and deletion policy

Decide whether to keep continuous footage, events only, or no recording when occupants are present. Minimize retention to the actual purpose, set a clear deletion schedule, and restrict access to recordings and snapshots. Encrypting data does not replace access control or consent.
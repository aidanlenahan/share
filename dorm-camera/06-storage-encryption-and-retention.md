# Encrypted Storage and Retention Design

**Status:** Planning only. The 256 GB microSD has not been confirmed installed; no LUKS volume has been created, and recording is disabled.

## Storage objective

Keep recorded video encrypted at rest on a high-endurance microSD, ideally retaining about seven days. The internal 128 GB SSD should hold OS, containers and configuration, not unencrypted video. Temporary caches and metadata need separate review; encryption of the microSD alone does **not** automatically encrypt thumbnails, database entries, logs, swap or other artifacts on the system SSD.

## LUKS2 design choices

- Device: **identify via `lsblk` each time**; never hardcode `/dev/mmcblk0` or `/dev/sdb` without confirmation.
- Encryption: LUKS2 with a strong unique passphrase.
- Filesystem: ext4 is a reasonable default for Linux removable media.
- Mount point: e.g. `/srv/frigate-encrypted`.
- Docker bind mount: map encrypted media to `/media/frigate` after confirming Frigate's expected directory layout and cache paths.
- Startup protection: container must not start recording when mount is absent; an empty host mount directory must not silently receive recordings on SSD.
- Consider `RequiresMountsFor=` or a systemd service that validates `findmnt` before `docker compose up`.
- Backup LUKS header securely and separately; loss of header or passphrase can mean permanent data loss.

## Data-erasing procedure — template, not commands to run blindly

1. Insert card and list block devices with `lsblk -o NAME,SIZE,MODEL,TRAN,FSTYPE,MOUNTPOINTS`.
2. Identify **exact** card device by size/model; verify it is not root disk.
3. Unmount existing partitions and back up anything valuable.
4. Create a new partition table/partition if desired.
5. `cryptsetup luksFormat` on the **confirmed** target partition (DESTRUCTIVE).
6. `cryptsetup open` to create a mapper device.
7. `mkfs.ext4` on the **mapper**, not the raw card.
8. Mount, set ownership/permissions, and verify with `findmnt` and `df -h`.
9. Adjust Docker volume mapping and startup dependencies.
10. Test reboot, manual unlock, shutdown, and recovery **before** enabling recording.

Do not execute destructive formatting until the exact device is verified interactively.

## Capacity planning

Assume a nominal 256 GB card, which is approximately **238 GiB** before formatting/reserved space. Actual usable capacity will be lower after filesystem overhead and a safety margin.

For constant bitrate video, approximate storage:

`GB/day ≈ bitrate_Mbps × 10.8` (decimal gigabytes)

| Average video bitrate | GB/day | 7-day storage (decimal GB) | Approx. days in 220 GB usable |
|---:|---:|---:|---:|
| 1 Mbps | 10.8 | 75.6 | 20.4 |
| 2 Mbps | 21.6 | 151.2 | 10.2 |
| 3 Mbps | 32.4 | 226.8 | 6.8 |
| 4 Mbps | 43.2 | 302.4 | 5.1 |
| 8 Mbps | 86.4 | 604.8 | 2.5 |

These are estimates for **continuous video**; audio, metadata, segment overhead, filesystem reserve, and variable bitrate can change results. The current encoder uses `-b:v 3000k -maxrate 4000k`, but actual average bitrate has **not** been measured during normal live use. Event-only recording could extend retention dramatically depending on activity.

## Durability and endurance

- High-endurance microSD is preferable to ordinary consumer cards for continuous writes.
- At 3 Mbps continuous recording, approximately 32.4 GB/day is written (~11.8 TB/year), before write amplification and other activity.
- Monitor card health where supported; not all SD readers expose SMART data.
- Minimize unnecessary writes, ensure adequate free space and avoid aggressive swap onto SD.
- A single microSD is not a backup; encrypted video can be lost to card failure.

## Security tradeoff: auto-unlock

**Manual unlock:** Better protection if device and card are stolen together, but recordings will not resume automatically after unattended reboot until unlocked.  
**Key stored on internal SSD:** Better automatic recovery, but theft of entire Chromebox may reveal both encrypted card and key, undermining theft protection.  
**External key / trusted unlock workflow:** More complex and may conflict with fully offline operation.

Select one explicitly and document what attack it protects against.

## Verification tests

- With encrypted media locked: `cryptsetup status <mapper>` shows inactive; raw card contains no readable video filesystem.
- With media unlocked: `findmnt /srv/frigate-encrypted` reports mapper filesystem; Frigate recordings land there.
- Without card: service must refuse recording or stay stopped, not write to `/opt/frigate/media` on SSD.
- After forced power loss: volume and filesystem recover cleanly; no unexpected plaintext copies.
- Check Frigate database, thumbnails, cache, logs, swap and backup locations for sensitive remnants.
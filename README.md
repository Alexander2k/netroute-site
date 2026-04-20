# NetRoute Pro

**Smart Route Generation for Network Engineers**

Chrome extension that discovers domains on any webpage, resolves IPs via racing DNS queries, and generates optimized routing commands for 8 platforms.

**🌐 Live site:** [alexander2k.github.io/netroute-site](https://alexander2k.github.io/netroute-site/)
**🧩 Chrome Web Store:** [NetRoute Pro](https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla)

![NetRoute Pro Banner](screenshots/promo-large.png)

## Features

- **Network Sniffer** — captures dynamic background requests (AJAX, CDN, API) in real-time via Service Worker
- **DNS Racing** — queries Cloudflare, Google, AdGuard simultaneously via `Promise.any` — first response wins
- **CIDR Aggregation** — merges individual IPs into optimized subnets (IPv4 bitmask + IPv6 BigInt)
- **RIPE BGP Optimization** — fetches real BGP prefixes from RIPE Stat API to replace /32s with announced routes
- **ASN Lookup** — batch IP-to-ASN resolution (e.g. `AS13335 (Cloudflare)`)
- **Bulk Scan** — paste a list of URLs, generate aggregated routes for all hostnames at once
- **Domain Blacklist** — exclude analytics/trackers, syncs across devices via Chrome Cloud Sync
- **Pro Export** — download as `.bat`, `.sh`, or `.rsc` with proper headers and verification commands

## Supported Platforms

| Platform | IPv4 | IPv6 |
|----------|------|------|
| **Windows** | `route add {net} mask {mask} {gw}` | `netsh interface ipv6 add route` |
| **Linux** | `ip route add {net}/{cidr} via {gw}` | `ip -6 route add` |
| **macOS** | `route add -net {net}/{cidr} {gw}` | `route add -inet6` |
| **MikroTik** | `/ip route add dst-address=` | `/ipv6 route add` |
| **Cisco** | `ip route {net} {mask} {gw}` | `ipv6 route` |
| **Juniper** | `set routing-options static route` | `set rib inet6.0 static route` |
| **WireGuard** | `AllowedIPs = {net}/{cidr}` | `AllowedIPs = {addr}` |
| **OpenVPN** | `route {net} {mask}` | `route-ipv6` |

## Screenshots

### Routes Generation
![Routes Tab](screenshots/popup-dark-routes.png)

### Domain Discovery
![Domains Tab](screenshots/popup-dark-domains.png)

### Extension in Browser
![Extension View](screenshots/screenshot-ext-dark-routes.png)

## How It Works

1. **Install & Navigate** — add the extension from Chrome Web Store, navigate to any site
2. **Configure & Scan** — choose target OS, merge mask, gateway, domain filter, click Analyze Website
3. **Copy or Export** — grab generated routes, copy to clipboard or export as script file

## Step-by-Step Guides

Detailed instructions for applying generated routes on each platform:

- [Keenetic](https://alexander2k.github.io/netroute-site/guides/keenetic.html) — `.bat` file upload with VPN interface binding
- [MikroTik](https://alexander2k.github.io/netroute-site/guides/mikrotik.html) — `.rsc` script import via `/import`
- [WireGuard](https://alexander2k.github.io/netroute-site/guides/wireguard.html) — AllowedIPs on any client (Linux/Windows/macOS/mobile)
- [Linux](https://alexander2k.github.io/netroute-site/guides/linux.html) — `.sh` script with systemd-networkd / NetworkManager persistence
- [OpenVPN](https://alexander2k.github.io/netroute-site/guides/openvpn.html) — client config `route` directives for split tunneling

Each guide links to official vendor documentation and covers common pitfalls.

## Available Languages

The site is available in **4 languages**:
- 🇬🇧 [English](https://alexander2k.github.io/netroute-site/)
- 🇷🇺 [Русский](https://alexander2k.github.io/netroute-site/ru/)
- 🇪🇸 [Español](https://alexander2k.github.io/netroute-site/es/)
- 🇨🇳 [中文](https://alexander2k.github.io/netroute-site/zh/)

## Tech Stack

- Chrome Extension (Manifest V3)
- Service Worker for network sniffing
- DoH (DNS over HTTPS) with racing resolution
- RIPE Stat API for BGP prefix lookups
- 5 interface languages

## Support the Project

<a href="https://dalink.to/netrouter">
  <img src="https://img.shields.io/badge/%E2%9D%A4%EF%B8%8F_Support_the_Project-orange?style=for-the-badge" alt="Support the Project">
</a>

## License

All rights reserved.

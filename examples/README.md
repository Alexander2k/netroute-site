# NetRoute — Example Config Files

Ready-to-edit configuration templates for each platform supported by [NetRoute](https://alexander2k.github.io/netroute-site/).

| File | Platform | Format |
|---|---|---|
| [`keenetic-routes.bat`](keenetic-routes.bat) | Keenetic | Windows `route ADD` syntax (uploaded via web UI) |
| [`mikrotik-routes.rsc`](mikrotik-routes.rsc) | MikroTik RouterOS | `/import` script |
| [`wireguard-split-tunnel.conf`](wireguard-split-tunnel.conf) | WireGuard | Peer config with `AllowedIPs` |
| [`linux-routes.sh`](linux-routes.sh) | Linux | Bash + `ip route` |
| [`openvpn-routes.ovpn`](openvpn-routes.ovpn) | OpenVPN | Client config snippet |
| [`singbox-rules.json`](singbox-rules.json) | sing-box / Hiddify | Rule-set, source format (`domain_suffix`, `ip_cidr`) |
| [`clash-rules.yaml`](clash-rules.yaml) | Clash / mihomo | Rule-provider, `behavior: classical` |
| [`xray-routing.json`](xray-routing.json) | Xray-core / 3X-UI | `routing.rules` fragment |
| [`v2rayn-rules.json`](v2rayn-rules.json) | v2rayN | Rule list for "Import Rules From Clipboard / File" |
| [`happ-routing.json`](happ-routing.json) | Happ | Routing profile (base64 → `happ://routing/onadd/…`) |
| [`shadowrocket-rules.list`](shadowrocket-rules.list) | Shadowrocket / Surge / Loon | Rule set lines |
| [`proxy.pac`](proxy.pac) | Browser / system proxy | PAC file |
| [`amnezia-sites.json`](amnezia-sites.json) | AmneziaVPN | Site list for import (hosts with addresses, subnets) |
| [`openwrt-routes.sh`](openwrt-routes.sh) | OpenWrt | Persistent routes via `uci` |

The rule-format examples are rendered by the extension's own `RuleFormats` module from a fixed sample scan (a github.com page), so they match the 4.1.3 output exactly; JSON formats carry no comments.

Each file contains inline comments explaining the syntax and how to apply it. Replace the example IPs/CIDRs with output from the [NetRoute Chrome extension](https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla) for your target sites.

See full step-by-step guides at [alexander2k.github.io/netroute-site/guides/](https://alexander2k.github.io/netroute-site/guides/).

# NetRoute Pro — Example Config Files

Ready-to-edit configuration templates for each platform supported by [NetRoute Pro](https://alexander2k.github.io/netroute-site/).

| File | Platform | Format |
|---|---|---|
| [`keenetic-routes.bat`](keenetic-routes.bat) | Keenetic | Windows `route ADD` syntax (uploaded via web UI) |
| [`mikrotik-routes.rsc`](mikrotik-routes.rsc) | MikroTik RouterOS | `/import` script |
| [`wireguard-split-tunnel.conf`](wireguard-split-tunnel.conf) | WireGuard | Peer config with `AllowedIPs` |
| [`linux-routes.sh`](linux-routes.sh) | Linux | Bash + `ip route` |
| [`openvpn-routes.ovpn`](openvpn-routes.ovpn) | OpenVPN | Client config snippet |

Each file contains inline comments explaining the syntax and how to apply it. Replace the example IPs/CIDRs with output from the [NetRoute Pro Chrome extension](https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla) for your target sites.

See full step-by-step guides at [alexander2k.github.io/netroute-site/guides/](https://alexander2k.github.io/netroute-site/guides/).

# Shared UI strings of the generated guide pages (English). HTML allowed.
# Extension labels quoted in the guides come from _locales/en/messages.json: "Target OS", "Gateway IP",
# "Device (Optional)", "ANALYZE WEBSITE", tabs "Routes" / "Domains", "Download", "Route Mode",
# "Route Optimization", "URL list", groups "Proxy clients" / "VPN clients".
UI = {
    'home': 'Home',
    'guides': 'Guides',
    'back': '&larr; Back to Home',
    'examples_h2': 'Example Configuration File',
    'examples_p': 'Ready-to-edit template. Replace the example domains and networks with output from NetRoute for your target sites.',
    'comments_hint': '<strong>Hint:</strong> the text formats download with a comment header. Untick <strong>“Include comments in exported files”</strong> in the NetRoute options to get the rules alone; the JSON formats never carry comments.',
    'all_examples': 'All example configs on GitHub &rarr;',
    'official_docs': 'Official Documentation',
    'related': 'Related Guides',
    'cta_h3': 'Ready to try?',
    'cta_p': 'NetRoute — a free Chrome extension to generate routes from any website.',
    'cta_btn': 'Install Extension',
    'shot_alt_default': 'NetRoute popup after scanning github.com: the selected format and the result on the Routes tab',
    'shot_caption_default': 'What the result looks like in NetRoute: the format is selected under “Target OS”, the output is on the Routes tab. Scan data: a github.com page.',
    'classic_names': {
        'keenetic': 'Keenetic', 'mikrotik': 'MikroTik', 'wireguard': 'WireGuard', 'linux': 'Linux', 'openvpn': 'OpenVPN',
    },
    'classic_related': {
        'keenetic': 'routes from a <code>.bat</code> upload',
        'mikrotik': '<code>.rsc</code> script import into RouterOS',
        'wireguard': 'split tunneling via <code>AllowedIPs</code>',
        'linux': '<code>ip route</code> shell script',
        'openvpn': '<code>route</code> directives in the client config',
    },
}

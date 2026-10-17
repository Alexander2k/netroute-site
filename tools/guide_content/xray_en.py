# Guide: Xray routing rules — Xray-core, 3X-UI, v2rayN, Streisand. English.
# Same facts and sources as xray_ru.py (verified 2026-10-17); extension labels from _locales/en.
PAGE = {
    'title': 'Xray routing rules for Xray-core, 3X-UI and v2rayN — guide | NetRoute',
    'description': 'How to get Xray routing.rules with a website’s domains and networks in NetRoute and apply them in Xray-core, 3X-UI’s Xray Settings or by importing into v2rayN.',
    'keywords': 'xray routing rules, xray domain: outboundTag, xray split tunneling, 3x-ui routing rules, 3x-ui xray settings routing, v2rayn import rules, v2rayn routing setting, v2rayn custom routing rules, xray json routing',
    'og_title': 'Xray routing rules from any website',
    'og_description': 'NetRoute turns the domains and networks of a website into Xray routing.rules — for an Xray-core config, the 3X-UI panel and rule import in v2rayN.',
    'breadcrumb': 'Xray',
    'h1': 'Xray routing rules from any website: Xray-core, 3X-UI, v2rayN',
    'lead': 'Xray directs connections by <code>routing.rules</code>: lists of domains and addresses plus the tag of an outbound. NetRoute builds such rules from a website in two variants: a fragment of an Xray-core config &mdash; which also fits the 3X-UI panel, where the Xray config is edited as JSON &mdash; and a file for importing rules into v2rayN.',
    'howto': {
        'name': 'How to apply Xray routing rules from NetRoute',
        'description': 'Generate rules in the Xray or v2rayN format with the NetRoute extension and paste them into routing.rules of an Xray-core config, into the Xray settings of the 3X-UI panel, or import them into v2rayN from the clipboard.',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Generate the rules in NetRoute', 'text': 'Open the website in Chrome, start NetRoute, pick “Xray / 3X-UI / Streisand” or “v2rayN (rules import)” under “Target OS”, put the tag of your outbound into the “Device” field (proxy by default), click “Analyze website” and download the file.'},
            {'name': 'Insert the rules', 'text': 'Xray-core and 3X-UI: add the objects from rules to the beginning of routing.rules in your config. v2rayN: Routing → Routing Setting → Import Rules From Clipboard, answer “yes” to the append question to keep the existing rules.'},
            {'name': 'Check', 'text': 'Restart Xray (the 3X-UI panel reloads it by itself) and open the site — it should go through the outbound with the given tag.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'What is inside the file',
            'html': '''    <p><strong>The “Xray / 3X-UI / Streisand” format</strong> is a fragment of an Xray-core config with a <code>routing</code> section. Domains and networks are two rules, each with its own list and a shared <code>outboundTag</code>:</p>
    <pre><code>{
  "routing": {
    "domainStrategy": "IPIfNonMatch",
    "rules": [
      { "type": "field", "outboundTag": "proxy", "domain": ["domain:github.com", "domain:githubusercontent.com"] },
      { "type": "field", "outboundTag": "proxy", "ip": ["140.82.112.0/20", "185.199.108.0/22", "2606:50c0::/32"] }
    ]
  }
}</code></pre>
    <ul>
        <li><code>domain:name</code> &mdash; per the Xray documentation the domain itself and its subdomains. The list is folded: when <code>api.github.com</code> and <code>github.com</code> are found, only <code>github.com</code> stays; <code>www.</code> is dropped. Every domain of the scan is included, also those that did not resolve to an IP.</li>
        <li><code>ip</code> &mdash; addresses in CIDR form; the same aggregated networks NetRoute emits as router routes, IPv4 and IPv6.</li>
        <li><code>outboundTag</code> &mdash; the tag of the outbound from the <strong>Device</strong> field in NetRoute; <code>proxy</code> by default.</li>
        <li><code>domainStrategy: IPIfNonMatch</code> &mdash; per the Xray documentation a domain is resolved to an address only when no rule matched by name; Xray’s own default is <code>AsIs</code>, no resolving.</li>
    </ul>
    <p><strong>The “v2rayN (rules import)” format</strong> is an array of rules in the shape v2rayN imports from the clipboard or a file (as in the <code>v2rayCustomRoutingList</code> repository of the v2rayN author):</p>
    <pre><code>[
  { "port": "", "outboundTag": "proxy", "domain": ["domain:github.com", "domain:githubusercontent.com"], "enabled": true, "remarks": "NetRoute github.com domains" },
  { "port": "", "outboundTag": "proxy", "ip": ["140.82.112.0/20", "185.199.108.0/22", "2606:50c0::/32"], "enabled": true, "remarks": "NetRoute github.com networks" }
]</code></pre>''',
        },
        {
            'h2': 'What you need',
            'html': '''    <ul>
        <li>Xray-core with a configured outbound and a known tag &mdash; on a computer, a server or in the <a href="https://github.com/MHSanaei/3x-ui" target="_blank" rel="noopener">3X-UI</a> panel</li>
        <li>or <a href="https://github.com/2dust/v2rayN" target="_blank" rel="noopener">v2rayN</a> for Windows, Linux or macOS &mdash; a client with the Xray and sing-box cores</li>
        <li>The <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> extension in Chrome</li>
    </ul>''',
        },
        {
            'h2': 'Step 1. Generate the rules in NetRoute',
            'html': '''    <ol>
        <li>Open the website in Chrome and reload the page so the extension’s sniffer sees the background requests</li>
        <li>Start <strong>NetRoute</strong></li>
        <li>Under <strong>Target OS</strong>, “Proxy clients” group, pick <strong>Xray / 3X-UI / Streisand</strong> for an Xray-core config or <strong>v2rayN (rules import)</strong> for importing into v2rayN</li>
        <li>In the <strong>Device</strong> field enter the tag of your outbound &mdash; the placeholder shows the default <code>proxy</code>. The <strong>Gateway IP</strong> field does not affect these formats</li>
        <li>Click <strong>Analyze website</strong></li>
        <li>On the <strong>Domains</strong> tab untick what you do not need &mdash; the rules update at once</li>
        <li>Click <strong>Download</strong>: the file is named after the site, for example <code>github_com_rules.json</code></li>
    </ol>''',
        },
        {
            'h2': 'Step 2a. Xray-core: insert the rules into the config',
            'html': '''    <p>Open Xray’s <code>config.json</code> and add both objects from <code>rules</code> to the <code>routing.rules</code> array <strong>above</strong> the general rules. Per the Xray documentation rules are checked top to bottom and the first match wins; a connection that matched no rule leaves through the first outbound of the config. Make sure <code>outboundTag</code> equals the tag of your proxy outbound and that <code>domainStrategy</code> is set once in the <code>routing</code> section.</p>
    <p>Restart Xray.</p>''',
        },
        {
            'h2': 'Step 2b. 3X-UI: rules in the Xray settings',
            'html': '''    <p>3X-UI is a web panel for Xray-core servers. Per its documentation the routing rules are Xray rules with the <code>domain</code>, <code>ip</code>, <code>port</code>, <code>network</code>, <code>protocol</code>, <code>inboundTag</code>, <code>sourceIP</code> matchers and an <code>outboundTag</code> or <code>balancerTag</code> target; there is no separate per-rule editor &mdash; you edit the JSON of the config under <strong>Xray Settings</strong>, and the panel reloads Xray by itself.</p>
    <ol>
        <li>Open <strong>Xray Settings</strong> in the panel</li>
        <li>Find the <code>routing.rules</code> array in the JSON and insert both objects from the NetRoute file at its beginning</li>
        <li>Put the tag of the wanted outbound into <code>outboundTag</code> &mdash; for example a WARP connection or another server, if these sites should go that way</li>
        <li>Save &mdash; the panel reloads Xray</li>
    </ol>
    <p>On a server the rule means: the clients’ traffic to these domains and networks is sent by the server to the given outbound, the rest as configured further down the rule list.</p>''',
        },
        {
            'h2': 'Step 2c. v2rayN: importing the rules',
            'html': '''    <p>For v2rayN pick the <strong>v2rayN (rules import)</strong> format in NetRoute. The v2rayN interface strings to follow:</p>
    <ol>
        <li>Open the downloaded file and copy its contents to the clipboard</li>
        <li>In v2rayN open <strong>Routing</strong> &rarr; <strong>Routing Setting</strong></li>
        <li>Choose <strong>Import Rules From Clipboard</strong> (there are also <strong>Import Rules From File</strong> and <strong>Import Rules From Subscription URL</strong>)</li>
        <li>To the question <em>“Do you want to append rules? Choose yes to append, no to replace.”</em> answer <strong>Yes</strong> to add the rules to the existing ones</li>
        <li>Check that the rule set they landed in is marked active (<strong>Set as active rule</strong>)</li>
    </ol>
    <p>In v2rayN’s rule editor the same lists appear in the <strong>Domain</strong> and <strong>IP or IP CIDR</strong> fields; the entry syntax is Xray’s, and the v2rayN wiki points to the Xray documentation for it.</p>''',
        },
        {
            'h2': 'Step 3. Check',
            'html': '''    <p>Open the site &mdash; it should go through the outbound with the tag from the rule, other sites as before. If the site does not open or bypasses the proxy, go through the common problems.</p>''',
        },
        {
            'h2': 'Common problems',
            'html': '''    <h3>The rule does not fire</h3>
    <p>Rules are checked top to bottom and the first match wins &mdash; if a rule above already takes this traffic (for example a general <code>geosite</code> rule), the NetRoute rule is never reached. Move the NetRoute rules up.</p>

    <h3>Xray does not start after the edit</h3>
    <p>Check the JSON: a stray comma or a second <code>routing</code> section breaks the config. Only the objects from the <code>rules</code> array go in, not the whole file.</p>

    <h3>Tag not found</h3>
    <p><code>outboundTag</code> has to equal the tag of an existing outbound literally. In NetRoute the tag is set in the <strong>Device</strong> field before the scan.</p>

    <h3>Streisand</h3>
    <p>Streisand is a client for iOS, macOS and visionOS with rule-based proxy setup (“Rule-based Proxy Setup” in its App Store description). How to add your own rules to it is described in the app’s documentation; the domain and network lists from the NetRoute file fit that purpose.</p>

    <h3>Several sites in one file</h3>
    <p>Click <strong>URL list</strong> next to the analyze button and paste the list of sites &mdash; NetRoute builds one set of rules for all of them, the file is named <code>bulk_N_rules.json</code>.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS and leaks',
        'html': '''    <p>A domain rule in Xray is matched against the destination name; how and where names are resolved is decided by <code>domainStrategy</code> and the <code>dns</code> section of your config &mdash; the NetRoute rules do not change them. The browser’s queries go wherever its own DNS is configured: in Chrome turn off “Use secure DNS” or point it at a resolver you trust, otherwise Chrome resolves names past the client.</p>
    <p>Check: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> with the client on should not show the ISP’s resolver.</p>''',
    },
    'official_docs': [
        {'url': 'https://xtls.github.io/config/routing.html', 'label': 'Xray: Routing &mdash; domainStrategy, rule order, the domain and ip forms (zh)'},
        {'url': 'https://github.com/MHSanaei/3x-ui', 'label': '3X-UI &mdash; README and the panel documentation'},
        {'url': 'https://github.com/MHSanaei/3x-ui/blob/main/docs/content/docs/en/operations/outbounds-routing.mdx', 'label': '3X-UI: Outbounds &amp; Routing'},
        {'url': 'https://github.com/2dust/v2rayN/wiki/Description-of-custom-routing-rules', 'label': 'v2rayN: description of custom routing rules (zh)'},
        {'url': 'https://github.com/2dust/v2rayCustomRoutingList', 'label': 'v2rayN: the format of the rule lists for import'},
    ],
    'shot_format': 'xray',
    'shot_caption': 'The NetRoute popup with the “Xray / 3X-UI / Streisand” format: the Device field holds the proxy tag, the Routes tab a routing.rules fragment. Scan data: a github.com page.',
    'example_file': 'xray-routing.json',
    'example_desc': 'a fragment of an Xray-core config with a <code>routing</code> section; next to it <code>v2rayn-rules.json</code> for importing into v2rayN',
    'card': {
        'badge': 'proxy',
        'badge_label': 'Proxy client',
        'title': 'Xray / 3X-UI / v2rayN',
        'text': 'routing.rules with the domains and networks of a site: into an Xray-core config, the Xray settings of the 3X-UI panel, or rule import in v2rayN.',
    },
    'related_desc': 'routing.rules for Xray-core, 3X-UI and v2rayN',
    'date_published': '2026-10-17',
}

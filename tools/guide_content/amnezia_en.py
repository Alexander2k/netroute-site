# Guide: AmneziaVPN site list for split tunneling. English.
# Same facts and sources as amnezia_ru.py (verified 2026-10-17); extension labels from _locales/en; the
# AmneziaVPN screen names follow docs.amnezia.org/documentation/instructions/vpn-split-tunneling (English).
PAGE = {
    'title': 'AmneziaVPN site list for split tunneling — guide | NetRoute',
    'description': 'How to get an AmneziaVPN import file with a website’s addresses and subnets in NetRoute and turn on split tunneling for sites: modes, ⋮ import, IPv4 only.',
    'keywords': 'amnezia split tunneling, amneziavpn split tunneling sites, amnezia site list, amnezia import ip-list.json, amnezia only the sites listed here, amneziawg split tunneling sites, amnezia service subnets',
    'og_title': 'AmneziaVPN site list from any website',
    'og_description': 'NetRoute turns the addresses and subnets of a website into a file for import into AmneziaVPN — split tunneling for sites in three steps.',
    'breadcrumb': 'AmneziaVPN',
    'h1': 'AmneziaVPN site list from any website',
    'lead': 'AmneziaVPN can send only the addresses from a list through the VPN &mdash; split tunneling for sites. The list consists of IPv4 addresses and subnets, and building it by hand for a site with dozens of domains takes long. NetRoute does it from the page: open the site, click “Analyze website”, download the file for import.',
    'howto': {
        'name': 'How to import a NetRoute site list into AmneziaVPN',
        'description': 'Generate an AmneziaVPN list with the NetRoute extension, import the file in the split tunneling settings for sites via the ⋮ menu and turn on the mode “Only the sites listed here will be accessed through the VPN”.',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Generate the list in NetRoute', 'text': 'Open the website in Chrome, start NetRoute, pick “AmneziaVPN (site list)” under “Target OS”, click “Analyze website” and download <site>_rules.json.'},
            {'name': 'Import the file into AmneziaVPN', 'text': 'Open the split tunneling settings for sites, choose the import in the ⋮ menu — replace the list or add to the existing one — and pick the file.'},
            {'name': 'Turn on the mode and connect', 'text': 'Choose the mode “Only the sites listed here will be accessed through the VPN”, enable split tunneling and connect to the VPN.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'What is inside the file',
            'html': '''    <p>The file is a JSON array of entries in the shape AmneziaVPN itself exports its list: each entry has a <code>hostname</code>, the list of addresses <code>ips</code> and the first of them in <code>ip</code> &mdash; for older versions of the app.</p>
    <pre><code>[
  { "hostname": "api.github.com", "ips": ["140.82.112.4"], "ip": "140.82.112.4" },
  { "hostname": "github.com", "ips": ["140.82.112.3"], "ip": "140.82.112.3" },
  { "hostname": "140.82.112.0/20", "ips": [], "ip": "" },
  { "hostname": "185.199.108.0/22", "ips": [], "ip": "" }
]</code></pre>
    <ul>
        <li><strong>Hosts with addresses.</strong> Per the client’s source code AmneziaVPN does not resolve names on import &mdash; the entries are stored as given, and resolving happens only when a site is added by hand. So NetRoute writes every host with the IPv4 addresses found during the scan; hosts without IPv4 addresses are left out. Names are not folded: <code>www.ozon.ru</code> and <code>ozon.ru</code> are separate entries with their own addresses.</li>
        <li><strong>Subnets.</strong> After the hosts come the aggregated IPv4 networks &mdash; the same ones NetRoute emits as router routes; with <strong>Route Optimization &rarr; BGP Prefix</strong> these are the provider’s announced prefixes rather than single addresses.</li>
        <li><strong>IPv4 only.</strong> Per the AmneziaVPN documentation IPv6 is not supported; IPv6 addresses are not written to the file.</li>
    </ul>''',
        },
        {
            'h2': 'What you need',
            'html': '''    <ul>
        <li>The <a href="https://amnezia.org/" target="_blank" rel="noopener">AmneziaVPN</a> app with a configured connection. Per the documentation split tunneling by addresses is not available in Amnezia Free</li>
        <li>A platform with tunneling by addresses: per the documentation iOS, macOS and Linux support only that, Windows and Android both by addresses and by apps</li>
        <li>The <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> extension in Chrome</li>
    </ul>''',
        },
        {
            'h2': 'Step 1. Generate the list in NetRoute',
            'html': '''    <ol>
        <li>Open the website in Chrome and reload the page so the extension’s sniffer sees the background requests</li>
        <li>Start <strong>NetRoute</strong></li>
        <li>Under <strong>Target OS</strong> pick <strong>AmneziaVPN (site list)</strong> &mdash; the “VPN clients” group</li>
        <li>The <strong>Gateway IP</strong> and <strong>Device</strong> fields do not affect this format</li>
        <li>Click <strong>Analyze website</strong></li>
        <li>On the <strong>Domains</strong> tab untick what you do not need &mdash; counters, ad networks, third-party CDNs; the list updates at once</li>
        <li>Click <strong>Download</strong>: the file is named after the site, for example <code>github_com_rules.json</code></li>
    </ol>
    <div class="callout">
        <strong>About changing addresses.</strong> The AmneziaVPN documentation warns that an address obtained from a domain is not updated automatically, and that large services need whole subnets. So before scanning enable <strong>Route Optimization &rarr; BGP Prefix</strong> in the NetRoute options &mdash; the file then carries the announced subnets, which survive address rotation at CDNs.
    </div>''',
        },
        {
            'h2': 'Step 2. Import the file into AmneziaVPN',
            'html': '''    <p>Per the AmneziaVPN documentation the list is imported from the split tunneling settings for sites:</p>
    <ol>
        <li>Open <strong>Split tunneling</strong> and go to the split tunneling settings for sites</li>
        <li>Tap the <strong>⋮</strong> icon and choose the import: replace the list &mdash; when starting from scratch, or add the imported sites to the existing ones &mdash; when extending</li>
        <li>Pick the downloaded file; the entries appear in the list</li>
    </ol>''',
        },
        {
            'h2': 'Step 3. Turn on the mode and connect',
            'html': '''    <ol>
        <li>Choose the mode <strong>Only the sites listed here will be accessed through the VPN</strong> &mdash; only the sites from the file go through the tunnel, the rest of the traffic goes direct. The second mode, <strong>Addresses from the list should not be accessed via VPN</strong>, does the opposite: it excludes the list from the tunnel</li>
        <li>Enable split tunneling for sites</li>
        <li>Connect to the VPN</li>
    </ol>''',
        },
        {
            'h2': 'Step 4. Check',
            'html': '''    <p>Open the site the list was built for: it should open through the VPN, sites outside the list direct. If the site opens only partly &mdash; some of its domains are missing from the list: check the <strong>Domains</strong> tab in NetRoute, walk through the site before scanning (sign in, open a video) so the sniffer sees the deferred requests, and import the file again, replacing the list.</p>''',
        },
        {
            'h2': 'Common problems',
            'html': '''    <h3>The file does not import</h3>
    <p>Per the client’s source code the file must be a JSON array of objects; a plain array of strings is rejected. The NetRoute file already has the right shape &mdash; check that it was downloaded completely and not edited in a text editor that replaces quotes.</p>

    <h3>The site worked, then stopped</h3>
    <p>The site’s addresses changed. Rebuild the file in NetRoute &mdash; with <strong>BGP Prefix</strong> enabled it carries subnets instead of single addresses &mdash; and import it replacing the list.</p>

    <h3>Unrelated traffic went through the VPN</h3>
    <p>The AmneziaVPN documentation warns that the wide subnets of large services can capture unrelated traffic. Untick third-party CDNs on the <strong>Domains</strong> tab in NetRoute or turn the BGP optimization off for such sites.</p>

    <h3>The connection to your own server was lost</h3>
    <p>Per the documentation, when the address of your VPN server falls inside one of the added subnets the connection breaks &mdash; remove that subnet from the list.</p>

    <h3>Several sites in one list</h3>
    <p>Click <strong>URL list</strong> next to the analyze button and paste the list of sites &mdash; NetRoute builds one file for all of them, named <code>bulk_N_rules.json</code>.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS and leaks',
        'html': '''    <p>AmneziaVPN’s split tunneling works by addresses: traffic to the addresses from the list enters the tunnel, while the browser’s DNS queries go wherever its resolver is configured. When that is the ISP’s resolver, it sees the names of the sites even while the traffic itself goes through the VPN. In Chrome turn off “Use secure DNS” or point it at a resolver you trust; the DNS settings of AmneziaVPN itself are described in its documentation.</p>
    <p>Check: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> with the VPN connected shows whose resolver answers your queries.</p>''',
    },
    'official_docs': [
        {'url': 'https://docs.amnezia.org/documentation/instructions/vpn-split-tunneling', 'label': 'AmneziaVPN: split tunneling &mdash; modes, import, limits'},
        {'url': 'https://github.com/amnezia-vpn/amnezia-client', 'label': 'AmneziaVPN: client source code &mdash; the import format in ipSplitTunnelingController'},
        {'url': 'https://amnezia.org/blog/what-is-split-tunneling-and-why-you-need-it', 'label': 'Amnezia: what split tunneling is'},
    ],
    'shot_format': 'amnezia',
    'shot_caption': 'The NetRoute popup with the “AmneziaVPN (site list)” format: the Routes tab holds the list for import, hosts with addresses and subnets. Scan data: a github.com page.',
    'example_file': 'amnezia-sites.json',
    'example_desc': 'a list for import into AmneziaVPN: hosts with addresses and subnets',
    'card': {
        'badge': 'vpn',
        'badge_label': 'VPN client',
        'title': 'AmneziaVPN',
        'text': 'A site list for split tunneling: hosts with IPv4 addresses and subnets, import via the ⋮ menu.',
    },
    'related_desc': 'site list for split tunneling',
    'date_published': '2026-10-17',
}

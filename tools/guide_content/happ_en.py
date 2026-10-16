# Guide: Happ routing profile. English.
# Same facts and sources as happ_ru.py (verified 2026-10-17); extension labels from _locales/en.
PAGE = {
    'title': 'Happ routing profile from any website: domains and networks through the proxy — guide | NetRoute',
    'description': 'How to get a Happ routing profile with the domains and networks of a website in NetRoute and add it with a happ://routing/onadd link: base64 encoding, import from the clipboard or a QR code, checking.',
    'keywords': 'happ routing, happ routing profile, happ routing onadd, happ json routing profile, happ proxysites, happ split tunneling, happ rules for a website, happ xray routing',
    'og_title': 'Happ routing profile from any website',
    'og_description': 'NetRoute turns the domains and networks of a website into a Happ routing profile. Encode it in base64, add it with a happ://routing/onadd link — only these sites go through the proxy.',
    'breadcrumb': 'Happ',
    'h1': 'Happ routing profile from any website',
    'lead': 'Happ is a cross-platform client on the Xray core for Windows, macOS, Linux, iOS, Android and TV platforms. What goes through the proxy is decided by a <strong>routing profile</strong>: lists of domains and addresses. NetRoute builds such a profile from a website as JSON, and it enters the app as a <code>happ://routing/onadd/…</code> link.',
    'howto': {
        'name': 'How to add a NetRoute routing profile to Happ',
        'description': 'Generate a Happ profile with the NetRoute extension, encode the JSON in base64, build the happ://routing/onadd/{base64} link and add it to Happ from the clipboard, by QR code or as a deeplink.',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Generate the profile in NetRoute', 'text': 'Open the website in Chrome, start NetRoute, pick “Happ” under “Target OS”, click “Analyze website” and download <site>_rules.json.'},
            {'name': 'Build the link', 'text': 'Encode the file contents in base64 and prepend happ://routing/onadd/ — the resulting link adds the profile and activates it at once.'},
            {'name': 'Add the link to Happ', 'text': 'Copy the link to the clipboard, open Happ and add it with the “+” button (from the clipboard, by QR code or as a deeplink). Reconnect after changing the profile.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'What is inside the file',
            'html': '''    <p>A Happ routing profile is a JSON document with DNS and geo-file settings and six lists: what goes through the proxy, what goes direct and what is blocked &mdash; separately for domains and for addresses. NetRoute fills the proxy lists and leaves the rest at values Happ accepts by default:</p>
    <pre><code>{
  "Name": "NetRoute github.com",
  "GlobalProxy": "false",
  "RemoteDNSType": "DoH",
  "RemoteDNSDomain": "https://1.1.1.1/dns-query",
  "RemoteDNSIP": "1.1.1.1",
  "DomesticDNSType": "DoH",
  "DomesticDNSDomain": "https://77.88.8.8/dns-query",
  "DomesticDNSIP": "77.88.8.8",
  "Geoipurl": "",
  "Geositeurl": "",
  "LastUpdated": "1760572800",
  "DnsHosts": {},
  "RouteOrder": "block-proxy-direct",
  "DirectSites": [],
  "DirectIp": ["geoip:private"],
  "ProxySites": ["domain:github.com", "domain:githubusercontent.com"],
  "ProxyIp": ["140.82.112.0/20", "185.199.108.0/22", "2606:50c0::/32"],
  "BlockSites": [],
  "BlockIp": [],
  "DomainStrategy": "IPIfNonMatch",
  "FakeDNS": "false"
}</code></pre>
    <p>What the fields mean, per the Happ documentation:</p>
    <ul>
        <li><code>GlobalProxy</code> &mdash; with <code>true</code> all traffic goes through the proxy by default, with <code>false</code> it goes direct; the same value sets the exit for everything that matched no rule. NetRoute sets <code>false</code>: only the listed sites go through the proxy.</li>
        <li><code>ProxySites</code> / <code>ProxyIp</code> &mdash; domains and addresses that go through the proxy. Domains are written as <code>domain:name</code> &mdash; per the Xray documentation that is the domain and all its subdomains; the list is folded, <code>www.</code> dropped. The addresses are the same aggregated networks NetRoute emits as router routes, IPv4 and IPv6.</li>
        <li><code>DirectSites</code> / <code>DirectIp</code> and <code>BlockSites</code> / <code>BlockIp</code> &mdash; direct and blocked; NetRoute leaves only private addresses direct (<code>geoip:private</code>).</li>
        <li><code>RouteOrder</code> &mdash; the order in which the rules are checked: block first, then proxy, then direct.</li>
        <li><code>DomainStrategy</code> &mdash; the Xray strategy: <code>IPIfNonMatch</code> resolves a domain to an address only when no rule matched by name.</li>
        <li><code>RemoteDNS*</code> / <code>DomesticDNS*</code> &mdash; DNS for the sites behind the proxy and for the rest; <code>DoH</code> is DNS-over-HTTPS. Change the values in the file before importing if you want other resolvers.</li>
        <li><code>Geoipurl</code> / <code>Geositeurl</code> &mdash; links to geoip.dat and geosite.dat; Happ fills empty values from its default profile.</li>
        <li><code>LastUpdated</code> &mdash; a Unix date; the profile is updated when it is higher than the previous one. NetRoute writes the generation time.</li>
        <li><code>DnsHosts</code> &mdash; manual “domain: IP” mappings, like a hosts file; empty in NetRoute’s profile.</li>
    </ul>''',
        },
        {
            'h2': 'What you need',
            'html': '''    <ul>
        <li>The <a href="https://www.happ.su/main" target="_blank" rel="noopener">Happ</a> app with a server added (Windows, macOS, Linux, iOS, Android, Android TV or Apple TV)</li>
        <li>The <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> extension in Chrome</li>
        <li>A way to base64-encode a file &mdash; every system has a command for it, examples below</li>
    </ul>''',
        },
        {
            'h2': 'Step 1. Generate the profile in NetRoute',
            'html': '''    <ol>
        <li>Open the website in Chrome and reload the page so the extension’s sniffer sees the background requests</li>
        <li>Start <strong>NetRoute</strong></li>
        <li>Under <strong>Target OS</strong> pick <strong>Happ</strong> &mdash; the “Proxy clients” group</li>
        <li>The <strong>Gateway IP</strong> and <strong>Device</strong> fields do not affect this format</li>
        <li>Click <strong>Analyze website</strong></li>
        <li>On the <strong>Domains</strong> tab untick what you do not need &mdash; counters, ad networks, third-party CDNs; the profile updates at once</li>
        <li>Click <strong>Download</strong>: the file is named after the site, for example <code>github_com_rules.json</code></li>
    </ol>''',
        },
        {
            'h2': 'Step 2. Build the happ://routing/… link',
            'html': '''    <p>Per the Happ documentation a profile is added with a link in which <code>{base64}</code> is the JSON profile converted to base64 text:</p>
    <ul>
        <li><code>happ://routing/add/{base64}</code> &mdash; adds the profile to the list;</li>
        <li><code>happ://routing/onadd/{base64}</code> &mdash; adds and activates it at once, even when another profile is active.</li>
    </ul>
    <p>Encode the downloaded file:</p>
    <pre><code># Windows, PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("github_com_rules.json"))

# macOS
base64 -i github_com_rules.json

# Linux
base64 -w0 github_com_rules.json</code></pre>
    <p>Prepend <code>happ://routing/onadd/</code> to the result &mdash; one line, no spaces or line breaks. The link gets long; that is normal.</p>
    <div class="callout">
        Encode the file locally &mdash; an online encoder would see your list of sites. A built-in “Copy as a Happ link” button in NetRoute is planned.
    </div>''',
        },
        {
            'h2': 'Step 3. Add the link to Happ',
            'html': '''    <p>Per the Happ documentation links are accepted in three ways &mdash; copied from the clipboard, scanned from a QR code and as a deeplink:</p>
    <ol>
        <li>Copy the built link to the clipboard</li>
        <li>Open Happ and tap <strong>+</strong> in the upper-right corner of the main screen</li>
        <li>Add the link from the clipboard. To a phone the link is easiest to pass as a QR code or to open as a deeplink &mdash; the system offers to open it in Happ</li>
        <li>With <code>onadd</code> the profile is already active; with <code>add</code> select it in the list of routing profiles</li>
        <li>Reconnect: per the documentation profile changes apply after <strong>Reconnect</strong></li>
    </ol>''',
        },
        {
            'h2': 'Step 4. Check',
            'html': '''    <p>Open the site the profile was built for &mdash; it should open through the proxy, while other sites go direct (<code>GlobalProxy: false</code>). If it is the other way round, check which routing profile is active in Happ and that you reconnected after the import.</p>''',
        },
        {
            'h2': 'Common problems',
            'html': '''    <h3>The link is not accepted</h3>
    <p>Check that the base64 is a single line without breaks (on Linux that needs the <code>-w0</code> switch) and that it is preceded by exactly <code>happ://routing/onadd/</code> or <code>happ://routing/add/</code>.</p>

    <h3>The profile was added but nothing changed</h3>
    <p>Happ applies a changed profile on reconnect. With an <code>add</code> link the profile also has to be selected as active.</p>

    <h3>The site pulls data from other domains</h3>
    <p>They should be visible on the <strong>Domains</strong> tab in NetRoute &mdash; the extension collects domains from the page and from its background requests. Walk through the site before scanning (sign in, open a video) so the deferred requests end up in the profile too. Several sites in one profile &mdash; the <strong>URL list</strong> button next to the analyze button: the file is named <code>bulk_N_rules.json</code>.</p>

    <h3>A profile in a subscription</h3>
    <p>Per the Happ documentation a JSON subscription may carry strictly 0 or 1 routing profile, and a profile link can be passed in the <code>routing</code> header or right in the subscription body &mdash; handy when you hand out settings to several devices.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS and leaks',
        'html': '''    <p>The profile sets two DNS servers: <code>RemoteDNS</code> for the sites behind the proxy and <code>DomesticDNS</code> for the rest &mdash; both over DNS-over-HTTPS (Cloudflare and Yandex in NetRoute’s file). Change them in the JSON before encoding if you need other resolvers. The browser’s queries still go wherever its own DNS is configured: in Chrome turn off “Use secure DNS” or point it at a resolver you trust, otherwise Chrome resolves names past the client.</p>
    <p>Check: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> with Happ on should show the resolver from the profile, not the ISP’s.</p>''',
    },
    'official_docs': [
        {'url': 'https://www.happ.su/main/dev-docs/routing.md', 'label': 'Happ: Routing &mdash; the add and onadd links, profile fields'},
        {'url': 'https://www.happ.su/main/faq/adding-configuration-subscription.md', 'label': 'Happ: Adding Configuration/Subscription &mdash; clipboard, QR code, deeplink'},
        {'url': 'https://www.happ.su/main/dev-docs/examples-of-links-and-parameters.md', 'label': 'Happ: Examples of links and parameters'},
        {'url': 'https://xtls.github.io/config/routing.html', 'label': 'Xray: Routing &mdash; the domain: form and domain strategies (zh)'},
    ],
    'shot_format': 'happ',
    'shot_caption': 'The NetRoute popup with the “Happ” format: the Routes tab holds the routing profile that remains to be encoded into a link. Scan data: a github.com page.',
    'example_file': 'happ-routing.json',
    'example_desc': 'a Happ routing profile with the <code>ProxySites</code> and <code>ProxyIp</code> lists',
    'card': {
        'badge': 'proxy',
        'badge_label': 'Proxy client',
        'title': 'Happ',
        'text': 'A routing profile with the domains and networks of a site: base64 → happ://routing/onadd link → import from the clipboard or a QR code.',
    },
    'related_desc': 'routing profile as a happ://routing link',
    'date_published': '2026-10-17',
}

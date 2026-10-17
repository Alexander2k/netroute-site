# Guide: sing-box rule-set (sing-box, Hiddify and other sing-box based clients). English.
# Same facts and sources as singbox_ru.py (verified 2026-10-16); extension labels from _locales/en.
PAGE = {
    'title': 'sing-box rule-set from any website for Hiddify — guide | NetRoute',
    'description': 'How to get a sing-box rule-set with a website’s domains and networks in NetRoute and wire it into sing-box or Hiddify: route.rule_set, action route, .srs, DNS.',
    'keywords': 'sing-box rule-set, sing-box rule_set source, sing-box domain_suffix ip_cidr, hiddify sing-box config, sing-box srs compile, split tunneling sing-box, sing-box rules for a website, sing-box route by domain',
    'og_title': 'sing-box rule-set from any website: domains and networks for Hiddify and sing-box',
    'og_description': 'NetRoute turns the domains and networks of a website into a sing-box rule-set. Wire it into route.rule_set with an action route rule, or compile it to .srs.',
    'breadcrumb': 'sing-box',
    'h1': 'sing-box rule-set from any website: domains and networks for Hiddify and sing-box',
    'lead': 'sing-box and the clients built on it &mdash; the official sing-box apps, Hiddify, NekoBox &mdash; decide what goes through the proxy by <strong>rules</strong>: lists of domains and networks, packaged since version 1.8.0 as rule-sets. NetRoute builds such a rule-set straight from a website: open the site, click “Analyze website”, download the <code>.json</code>.',
    'howto': {
        'name': 'How to wire a NetRoute rule-set into sing-box',
        'description': 'Generate a rule-set in the sing-box format with the NetRoute extension, describe the file in route.rule_set and add a route.rules entry with action route and the outbound of your proxy.',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Generate the rule-set in NetRoute', 'text': 'Open the website in Chrome, start NetRoute, pick “sing-box / Hiddify / NekoBox” under “Target OS”, click “Analyze website” and download <site>_rules.json.'},
            {'name': 'Describe the file in the sing-box config', 'text': 'Add a route.rule_set entry of type local with format source and the path to the file (or type remote with a url when the file is published), and a route.rules entry with rule_set, action route and the outbound of your proxy.'},
            {'name': 'Check the config', 'text': 'Run sing-box check -c config.json, start sing-box and open the site.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'What is inside the file',
            'html': '''    <p>A rule-set in the source format (<code>source</code>) is a JSON document with <code>version</code> and <code>rules</code>. NetRoute writes the domains and the networks as <strong>two separate rules</strong>: per the sing-box documentation the conditions inside one rule are combined with a logical AND, so a single rule with both domains and networks would match only when both agree.</p>
    <pre><code>{
  "version": 1,
  "rules": [
    { "domain_suffix": ["github.com", "githubusercontent.com"] },
    { "ip_cidr": ["140.82.112.0/20", "185.199.108.0/22", "2606:50c0::/32"] }
  ]
}</code></pre>
    <ul>
        <li><code>domain_suffix</code> &mdash; a domain suffix match: the domain itself and all its subdomains. NetRoute folds the list: when the page uses <code>api.github.com</code> and <code>github.com</code>, only <code>github.com</code> stays; a <code>www.</code> prefix is dropped. Every domain of the scan is listed, including those that did not resolve to an IP.</li>
        <li><code>ip_cidr</code> &mdash; a network match. These are the same aggregated networks NetRoute would emit as routes for a router, IPv4 and IPv6 together; the rule is present when at least one domain resolved to an address.</li>
        <li><code>version: 1</code> &mdash; the first version of the format, introduced in sing-box 1.8.0.</li>
    </ul>''',
        },
        {
            'h2': 'What you need',
            'html': '''    <ul>
        <li>sing-box 1.8.0 or newer: the <code>sing-box</code> binary on a computer, server or router, or the official apps <em>sing-box for Android</em>, <em>sing-box for Apple platforms</em>, <em>sing-box for Desktop</em></li>
        <li>or <a href="https://github.com/hiddify/hiddify-app" target="_blank" rel="noopener">Hiddify</a> &mdash; a client built on the sing-box core which, per its README, accepts configurations in the sing-box format (Android, iOS, Windows, macOS, Linux)</li>
        <li>A working proxy outbound in the config &mdash; any protocol</li>
        <li>The <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> extension in Chrome</li>
    </ul>
    <div class="callout">
        <strong>NekoBox for Android</strong> runs on the sing-box core too, but per its README it takes only the nodes from a subscription and ignores routing rules. A rule-set can reach it only inside a full sing-box configuration.
    </div>''',
        },
        {
            'h2': 'Step 1. Generate the rule-set in NetRoute',
            'html': '''    <ol>
        <li>Open the website in Chrome and reload the page so the extension’s sniffer sees the background requests</li>
        <li>Start <strong>NetRoute</strong></li>
        <li>Under <strong>Target OS</strong> pick <strong>sing-box / Hiddify / NekoBox</strong> &mdash; the “Proxy clients” group</li>
        <li>The <strong>Gateway IP</strong> and <strong>Device</strong> fields do not affect this format</li>
        <li>Click <strong>Analyze website</strong></li>
        <li>On the <strong>Domains</strong> tab untick what you do not need &mdash; counters, ad networks, third-party CDNs; the rules update at once</li>
        <li>Click <strong>Download</strong>: the file is named after the site, for example <code>github_com_rules.json</code></li>
    </ol>
    <div class="callout">
        <strong>About the networks.</strong> The <code>ip_cidr</code> rule is always in the file when there are resolved addresses, and it does not get in the way of the domain rule. Want domains only &mdash; delete the second rule from the file. Want fewer networks &mdash; choose <strong>IPv4 Only</strong> under <strong>Route Mode</strong>: the rule keeps no IPv6 prefixes.
    </div>''',
        },
        {
            'h2': 'Step 2. Describe the file in the sing-box config',
            'html': '''    <p>A local file next to the config. <code>format</code> may be omitted when the path ends in <code>.json</code> or <code>.srs</code>; since 1.10.0 sing-box reloads the file by itself when it changes.</p>
    <pre><code>{
  "route": {
    "rule_set": [
      {
        "type": "local",
        "tag": "netroute",
        "format": "source",
        "path": "github_com_rules.json"
      }
    ],
    "rules": [
      { "rule_set": "netroute", "action": "route", "outbound": "proxy" }
    ],
    "final": "direct"
  }
}</code></pre>
    <ul>
        <li><code>outbound</code> &mdash; the tag of your proxy outbound. <code>"action": "route"</code> is required from sing-box 1.11.0 on: the old <code>outbound</code> field directly in the rule is deprecated there.</li>
        <li><code>final</code> &mdash; the default outbound for everything that matched no rule; <code>direct</code> gives classic split tunneling.</li>
    </ul>
    <p>A file by URL. Put the <code>.json</code> into a GitHub repository or on your own server and give the direct link to the raw file; by default sing-box refreshes it once a day (<code>update_interval</code> = <code>1d</code>):</p>
    <pre><code>{
  "type": "remote",
  "tag": "netroute",
  "format": "source",
  "url": "https://raw.githubusercontent.com/you/rules/main/github_com_rules.json",
  "update_interval": "1d"
}</code></pre>
    <p>If the link has to be downloaded through the proxy: up to sing-box 1.13 the <code>download_detour</code> field with an outbound tag did that; 1.14.0 deprecated it in favour of <code>http_client</code>, and 1.16.0 removed it.</p>
    <div class="callout">
        <strong>Hiddify.</strong> The app accepts configurations in the sing-box format &mdash; add the <code>route</code> block above together with your outbound to such a config and import it as a profile. How exactly a profile is imported in your version of Hiddify is described in the app’s documentation.
    </div>''',
        },
        {
            'h2': 'Step 3. Check',
            'html': '''    <p>The syntax of the config together with the rule-set:</p>
    <pre><code>sing-box check -c config.json</code></pre>
    <p>Then start sing-box and open the site. If it opens through the proxy while other sites go direct &mdash; the rule works. If not, go through the common problems below.</p>''',
        },
        {
            'h2': 'Compiled rule-set (.srs)',
            'html': '''    <p>For big lists sing-box offers a binary format. Compile the NetRoute file with the command from the documentation:</p>
    <pre><code>sing-box rule-set compile github_com_rules.json
# → github_com_rules.srs</code></pre>
    <p>In the config set <code>"format": "binary"</code> and the path to the <code>.srs</code>. For a dozen sites this is not necessary.</p>''',
        },
        {
            'h2': 'Common problems',
            'html': '''    <h3>sing-box rejects the file</h3>
    <p>Rule-sets appeared in sing-box 1.8.0; older versions and clients built on them do not know the format. NetRoute writes the minimal <code>version: 1</code> &mdash; every later version reads it.</p>

    <h3>The rule does not match a subdomain</h3>
    <p><code>domain_suffix</code> covers the subdomains of the domains in the list only. If the site pulls data from another domain, it should be visible on the <strong>Domains</strong> tab in NetRoute. Walk through the site before scanning &mdash; sign in, open a video &mdash; so the extension’s sniffer sees the deferred requests too.</p>

    <h3>Connections by IP bypass the proxy</h3>
    <p>A domain rule needs sing-box to know the destination name. That is what sniffing is for: it takes the name from the HTTP Host field and from the Server Name in TLS and QUIC. From sing-box 1.11.0 sniffing is enabled by a rule with <code>"action": "sniff"</code> in <code>route.rules</code> (the old inbound <code>sniff</code> field is deprecated and was removed in 1.13.0). Connections without a name are matched by the <code>ip_cidr</code> rule &mdash; for services whose addresses change, enable <strong>Route Optimization &rarr; BGP Prefix</strong> in the NetRoute options: the networks become the announced prefixes instead of single addresses.</p>

    <h3>One rule-set for several sites</h3>
    <p>Click <strong>URL list</strong> next to the analyze button and paste the list of sites &mdash; NetRoute builds one rule-set for all of them, the file is named <code>bulk_N_rules.json</code>.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS and leaks',
        'html': '''    <p>A domain rule does not change how the browser resolves names: the DNS query for <code>github.com</code> still goes to the resolver configured in the system or in the browser itself, and when that is the ISP’s resolver, the ISP sees the names of the sites.</p>
    <ul>
        <li>In sing-box the DNS rules can reference the same rule-set: a <code>dns.rules</code> entry with <code>"rule_set": "netroute"</code>, <code>"action": "route"</code> and <code>server</code> sends the queries for these domains to the chosen DNS server. To make the server itself go through the proxy, give it a <code>detour</code> with the outbound tag &mdash; a field of the shared Dial Fields; servers in the new format (<code>"type": "https"</code> and others) appeared in sing-box 1.12.0.</li>
        <li>In Chrome turn off “Use secure DNS” or point it at a resolver you trust: the browser’s own DNS-over-HTTPS works past the system resolver &mdash; see the <a href="https://github.com/Alexander2k/netroute-site" target="_blank" rel="noopener">Troubleshooting section</a> of the project.</li>
    </ul>
    <p>Check: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> with the client on should show the proxy’s resolver, not the ISP’s.</p>''',
    },
    'official_docs': [
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/', 'label': 'sing-box: Rule Set &mdash; local and remote fields'},
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/source-format/', 'label': 'sing-box: Source Format &mdash; version, the compile command'},
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/headless-rule/', 'label': 'sing-box: Headless Rule &mdash; domain_suffix, ip_cidr'},
        {'url': 'https://sing-box.sagernet.org/configuration/route/rule_action/', 'label': 'sing-box: Rule Action &mdash; route, sniff'},
        {'url': 'https://sing-box.sagernet.org/configuration/dns/rule/', 'label': 'sing-box: DNS Rule'},
        {'url': 'https://github.com/hiddify/hiddify-app', 'label': 'Hiddify &mdash; README: supported configuration formats'},
    ],
    'shot_format': 'singbox',
    'shot_caption': 'The NetRoute popup with the “sing-box / Hiddify / NekoBox” format: the Routes tab holds the finished rule-set, the counter shows the number of rules. Scan data: a github.com page.',
    'example_file': 'singbox-rules.json',
    'example_desc': 'a rule-set in the source format with <code>domain_suffix</code> and <code>ip_cidr</code> rules',
    'card': {
        'badge': 'proxy',
        'badge_label': 'Proxy client',
        'title': 'sing-box / Hiddify',
        'text': 'A rule-set with the domains and networks of a site: local file or URL in route.rule_set, compiling to .srs.',
    },
    'related_desc': 'rule-set for sing-box and Hiddify',
    'date_published': '2026-10-16',
}

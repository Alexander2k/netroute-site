# 指南：Happ 路由配置文件（routing profile）。简体中文。
# 事实与来源同 happ_ru.py（2026-10-17 核对）；扩展界面文案来自 _locales/zh_CN。
PAGE = {
    'title': '从任意网站生成 Happ 路由配置文件：让域名和网段走代理 — 指南 | NetRoute',
    'description': '如何在 NetRoute 中获取包含网站域名和网段的 Happ 路由配置文件，并通过 happ://routing/onadd 链接添加：base64 编码、从剪贴板或二维码导入、检查。',
    'keywords': 'happ routing, happ 路由配置文件, happ routing onadd, happ json routing profile, happ proxysites, happ 分流, happ 网站规则, happ xray 路由',
    'og_title': '从任意网站生成 Happ 路由配置文件',
    'og_description': 'NetRoute 将网站的域名和网段整理为 Happ 路由配置文件。以 base64 编码后通过 happ://routing/onadd 链接添加 — 只有这些网站走代理。',
    'breadcrumb': 'Happ',
    'h1': '从任意网站生成 Happ 路由配置文件',
    'lead': 'Happ 是基于 Xray 内核的跨平台客户端，支持 Windows、macOS、Linux、iOS、Android 和 TV 平台。哪些流量走代理由<strong>路由配置文件</strong>（routing profile）决定：即域名和地址的列表。NetRoute 可从网站生成这样的 JSON 配置文件，它以 <code>happ://routing/onadd/…</code> 链接的形式进入应用。',
    'howto': {
        'name': '如何将 NetRoute 的路由配置文件添加到 Happ',
        'description': '使用 NetRoute 扩展生成 Happ 配置文件，将 JSON 编码为 base64，构造 happ://routing/onadd/{base64} 链接，然后从剪贴板、通过二维码或作为 deeplink 添加到 Happ。',
        'total_time': 'PT5M',
        'steps': [
            {'name': '在 NetRoute 中生成配置文件', 'text': '在 Chrome 中打开目标网站，启动 NetRoute，在「目标系统」中选择「Happ」，点击「分析网站」并下载 <网站>_rules.json。'},
            {'name': '构造链接', 'text': '将文件内容编码为 base64，并在前面加上 happ://routing/onadd/ — 得到的链接会添加配置文件并立即激活它。'},
            {'name': '将链接添加到 Happ', 'text': '将链接复制到剪贴板，打开 Happ 并用「+」按钮添加（从剪贴板、通过二维码或作为 deeplink）。更改配置文件后请重新连接。'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': '文件内容',
            'html': '''    <p>Happ 路由配置文件是一个 JSON 文档，包含 DNS 和 geo 文件设置以及六个列表：哪些走代理、哪些直连、哪些被屏蔽 &mdash; 域名和地址各自分开。NetRoute 填写代理列表，其余保持 Happ 默认接受的值：</p>
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
    <p>各字段的含义，按 Happ 文档：</p>
    <ul>
        <li><code>GlobalProxy</code> &mdash; 为 <code>true</code> 时所有流量默认走代理，为 <code>false</code> 时直连；同一个值也决定了所有未匹配任何规则的流量的出口。NetRoute 设为 <code>false</code>：只有列出的网站走代理。</li>
        <li><code>ProxySites</code> / <code>ProxyIp</code> &mdash; 走代理的域名和地址。域名写成 <code>domain:name</code> 形式 &mdash; 按 Xray 文档，这表示该域名及其所有子域名；列表已折叠，<code>www.</code> 已去掉。地址是 NetRoute 为路由器输出路由时所用的同一批聚合网段，IPv4 和 IPv6。</li>
        <li><code>DirectSites</code> / <code>DirectIp</code> 和 <code>BlockSites</code> / <code>BlockIp</code> &mdash; 直连和屏蔽；NetRoute 只把私有地址留为直连（<code>geoip:private</code>）。</li>
        <li><code>RouteOrder</code> &mdash; 规则的检查顺序：先屏蔽，再代理，最后直连。</li>
        <li><code>DomainStrategy</code> &mdash; Xray 策略：<code>IPIfNonMatch</code> 只在没有规则按名称匹配时才把域名解析为地址。</li>
        <li><code>RemoteDNS*</code> / <code>DomesticDNS*</code> &mdash; 分别用于走代理的网站和其余网站的 DNS；<code>DoH</code> 即 DNS-over-HTTPS。如需其他解析器，请在导入前修改文件中的值。</li>
        <li><code>Geoipurl</code> / <code>Geositeurl</code> &mdash; geoip.dat 和 geosite.dat 的链接；空值由 Happ 从其默认配置文件填充。</li>
        <li><code>LastUpdated</code> &mdash; Unix 格式的日期；当它大于之前的值时配置文件才会更新。NetRoute 写入生成时间。</li>
        <li><code>DnsHosts</code> &mdash; 手动的「域名: IP」映射，类似 hosts 文件；NetRoute 的配置文件中为空。</li>
    </ul>''',
        },
        {
            'h2': '准备工作',
            'html': '''    <ul>
        <li>已添加服务器的 <a href="https://www.happ.su/main" target="_blank" rel="noopener">Happ</a> 应用（Windows、macOS、Linux、iOS、Android、Android TV 或 Apple TV）</li>
        <li>Chrome 中已安装 <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> 扩展</li>
        <li>一种对文件进行 base64 编码的方法 &mdash; 每个系统都有相应的命令，示例见下文</li>
    </ul>''',
        },
        {
            'h2': '步骤 1. 在 NetRoute 中生成配置文件',
            'html': '''    <ol>
        <li>在 Chrome 中打开目标网站并刷新页面，让扩展的嗅探器看到后台请求</li>
        <li>启动 <strong>NetRoute</strong></li>
        <li>在 <strong>「目标系统」</strong> 中选择 <strong>Happ</strong> &mdash; 位于「代理客户端」分组</li>
        <li><strong>「网关 IP」</strong> 和 <strong>「网络设备」</strong> 字段不影响此格式</li>
        <li>点击 <strong>「分析网站」</strong></li>
        <li>在 <strong>「域名列表」</strong> 标签页中取消勾选不需要的项 &mdash; 统计计数器、广告网络、第三方 CDN；配置文件会立即更新</li>
        <li>点击 <strong>「下载」</strong>：文件以网站命名，例如 <code>github_com_rules.json</code></li>
    </ol>''',
        },
        {
            'h2': '步骤 2. 构造 happ://routing/… 链接',
            'html': '''    <p>按 Happ 文档，配置文件通过链接添加，其中 <code>{base64}</code> 是转换为 base64 文本的 JSON 配置文件：</p>
    <ul>
        <li><code>happ://routing/add/{base64}</code> &mdash; 将配置文件添加到列表；</li>
        <li><code>happ://routing/onadd/{base64}</code> &mdash; 添加并立即激活，即使当前有另一个配置文件处于激活状态。</li>
    </ul>
    <p>对下载的文件进行编码：</p>
    <pre><code># Windows, PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("github_com_rules.json"))

# macOS
base64 -i github_com_rules.json

# Linux
base64 -w0 github_com_rules.json</code></pre>
    <p>在结果前面加上 <code>happ://routing/onadd/</code> &mdash; 一整行，不含空格或换行。链接会很长；这是正常的。</p>
    <div class="callout">
        请在本地编码文件 &mdash; 在线编码器会看到你的网站列表。NetRoute 计划内置「复制为 Happ 链接」按钮。
    </div>''',
        },
        {
            'h2': '步骤 3. 将链接添加到 Happ',
            'html': '''    <p>按 Happ 文档，链接可通过三种方式接收 &mdash; 从剪贴板复制、扫描二维码以及作为 deeplink：</p>
    <ol>
        <li>将构造好的链接复制到剪贴板</li>
        <li>打开 Happ，点击主屏幕右上角的 <strong>+</strong></li>
        <li>从剪贴板添加链接。传到手机上最简单的方式是以二维码传递或作为 deeplink 打开 &mdash; 系统会提示在 Happ 中打开</li>
        <li>使用 <code>onadd</code> 时配置文件已处于激活状态；使用 <code>add</code> 时请在路由配置文件列表中选择它</li>
        <li>重新连接：按文档说明，配置文件的更改在 <strong>Reconnect</strong>（重新连接）后生效</li>
    </ol>''',
        },
        {
            'h2': '步骤 4. 检查',
            'html': '''    <p>打开为其生成配置文件的网站 &mdash; 它应通过代理打开，而其他网站直连（<code>GlobalProxy: false</code>）。如果情况相反，请检查 Happ 中激活的是哪个路由配置文件，以及导入后是否已重新连接。</p>''',
        },
        {
            'h2': '常见问题',
            'html': '''    <h3>链接不被接受</h3>
    <p>检查 base64 是否为不含换行的单行（在 Linux 上需要 <code>-w0</code> 参数），以及前面是否正好是 <code>happ://routing/onadd/</code> 或 <code>happ://routing/add/</code>。</p>

    <h3>配置文件已添加但没有任何变化</h3>
    <p>Happ 在重新连接时应用更改后的配置文件。使用 <code>add</code> 链接时，还必须将该配置文件选为激活状态。</p>

    <h3>网站从其他域名拉取数据</h3>
    <p>它们应该出现在 NetRoute 的 <strong>「域名列表」</strong> 标签页中 &mdash; 扩展会从页面及其后台请求中收集域名。扫描前先在网站上浏览一遍（登录、打开一个视频），让延迟发出的请求也进入配置文件。多个网站放进一个配置文件 &mdash; 使用分析按钮旁的 <strong>「URL 列表」</strong> 按钮：文件名为 <code>bulk_N_rules.json</code>。</p>

    <h3>订阅中的配置文件</h3>
    <p>按 Happ 文档，JSON 订阅中严格只能包含 0 或 1 个路由配置文件，而配置文件链接可以放在 <code>routing</code> 头部或直接放在订阅正文中 &mdash; 向多台设备分发设置时很方便。</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS 与泄漏',
        'html': '''    <p>配置文件设置了两个 DNS 服务器：<code>RemoteDNS</code> 用于走代理的网站，<code>DomesticDNS</code> 用于其余网站 &mdash; 两者都通过 DNS-over-HTTPS（NetRoute 的文件中为 Cloudflare 和 Yandex）。如需其他解析器，请在编码前在 JSON 中修改。浏览器的查询仍然发往其自身配置的 DNS：在 Chrome 中关闭「使用安全 DNS」或将其指向你信任的解析器，否则 Chrome 会绕过客户端解析名称。</p>
    <p>检查：开启 Happ 后，<a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> 应显示配置文件中的解析器，而不是运营商的。</p>''',
    },
    'official_docs': [
        {'url': 'https://www.happ.su/main/dev-docs/routing.md', 'label': 'Happ：Routing &mdash; add 和 onadd 链接、配置文件字段'},
        {'url': 'https://www.happ.su/main/faq/adding-configuration-subscription.md', 'label': 'Happ：Adding Configuration/Subscription &mdash; 剪贴板、二维码、deeplink'},
        {'url': 'https://www.happ.su/main/dev-docs/examples-of-links-and-parameters.md', 'label': 'Happ：Examples of links and parameters'},
        {'url': 'https://xtls.github.io/config/routing.html', 'label': 'Xray：Routing &mdash; domain: 形式与域名策略 (zh)'},
    ],
    'shot_format': 'happ',
    'shot_caption': '选择「Happ」格式的 NetRoute 弹窗：「路由」标签页中是路由配置文件，接下来只需将其编码为链接。扫描数据：github.com 页面。',
    'example_file': 'happ-routing.json',
    'example_desc': '包含 <code>ProxySites</code> 和 <code>ProxyIp</code> 列表的 Happ 路由配置文件',
    'card': {
        'badge': 'proxy',
        'badge_label': '代理客户端',
        'title': 'Happ',
        'text': '包含网站域名和网段的路由配置文件：base64 → happ://routing/onadd 链接 → 从剪贴板或二维码导入。',
    },
    'related_desc': '以 happ://routing 链接形式提供的路由配置文件',
    'date_published': '2026-10-17',
}

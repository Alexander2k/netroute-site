# 指南：sing-box rule-set（sing-box、Hiddify 及其他基于 sing-box 内核的客户端）。简体中文。
# 事实与来源同 singbox_ru.py（2026-10-16 核对）；扩展界面文案来自 _locales/zh_CN。
PAGE = {
    'title': '从任意网站生成 sing-box rule-set：Hiddify 与 sing-box 的域名和网段 — 指南 | NetRoute',
    'description': '如何在 NetRoute 中获取包含网站域名和网段的 sing-box rule-set，并将其接入 sing-box 或 Hiddify 配置：route.rule_set、带 action route 的规则、编译为 .srs、DNS。',
    'keywords': 'sing-box rule-set, sing-box rule_set source, sing-box domain_suffix ip_cidr, hiddify sing-box 配置, sing-box srs 编译, sing-box 分流, sing-box 网站规则, sing-box 按域名路由',
    'og_title': '从任意网站生成 sing-box rule-set：Hiddify 与 sing-box 的域名和网段',
    'og_description': 'NetRoute 将网站的域名和网段整理为 sing-box rule-set。通过带 action route 的规则接入 route.rule_set，或编译为 .srs。',
    'breadcrumb': 'sing-box',
    'h1': '从任意网站生成 sing-box rule-set：Hiddify 与 sing-box 的域名和网段',
    'lead': 'sing-box 及基于它构建的客户端 &mdash; 官方 sing-box 应用、Hiddify、NekoBox &mdash; 依靠<strong>规则</strong>决定哪些流量走代理：规则是域名和网段的列表，自 1.8.0 版起打包为 rule-set。NetRoute 可直接从网站生成这样的 rule-set：打开网站，点击「分析网站」，下载 <code>.json</code> 即可。',
    'howto': {
        'name': '如何将 NetRoute 的 rule-set 接入 sing-box',
        'description': '使用 NetRoute 扩展生成 sing-box 格式的 rule-set，在 route.rule_set 中描述该文件，并在 route.rules 中添加一条带 action route 和代理 outbound 的规则。',
        'total_time': 'PT5M',
        'steps': [
            {'name': '在 NetRoute 中生成 rule-set', 'text': '在 Chrome 中打开目标网站，启动 NetRoute，在「目标系统」中选择「sing-box / Hiddify / NekoBox」，点击「分析网站」并下载 <网站>_rules.json。'},
            {'name': '在 sing-box 配置中描述该文件', 'text': '在 route.rule_set 中添加一条 type local、format source 并带有文件 path 的记录（文件已发布时则用 type remote 加 url），并在 route.rules 中添加一条带 rule_set、action route 和代理 outbound 的规则。'},
            {'name': '检查配置', 'text': '运行 sing-box check -c config.json，启动 sing-box 并打开网站。'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': '文件内容',
            'html': '''    <p>源格式（<code>source</code>）的 rule-set 是一个带有 <code>version</code> 和 <code>rules</code> 的 JSON 文档。NetRoute 将域名和网段写成<strong>两条独立的规则</strong>：按照 sing-box 文档，同一条规则内的条件以逻辑「与」组合，若把域名和网段放在同一条规则中，则只有两者同时匹配时才会命中。</p>
    <pre><code>{
  "version": 1,
  "rules": [
    { "domain_suffix": ["github.com", "githubusercontent.com"] },
    { "ip_cidr": ["140.82.112.0/20", "185.199.108.0/22", "2606:50c0::/32"] }
  ]
}</code></pre>
    <ul>
        <li><code>domain_suffix</code> &mdash; 域名后缀匹配：域名本身及其所有子域名。NetRoute 会折叠列表：当页面同时使用 <code>api.github.com</code> 和 <code>github.com</code> 时，只保留 <code>github.com</code>；<code>www.</code> 前缀会被去掉。扫描到的所有域名都会列出，包括未能解析出 IP 的域名。</li>
        <li><code>ip_cidr</code> &mdash; 网段匹配。这些就是 NetRoute 为路由器输出路由时所用的同一批聚合网段，IPv4 和 IPv6 一起；只要至少有一个域名解析出了地址，这条规则就会存在。</li>
        <li><code>version: 1</code> &mdash; 该格式的第一个版本，自 sing-box 1.8.0 引入。</li>
    </ul>''',
        },
        {
            'h2': '准备工作',
            'html': '''    <ul>
        <li>sing-box 1.8.0 或更新版本：电脑、服务器或路由器上的 <code>sing-box</code> 二进制程序，或官方应用 <em>sing-box for Android</em>、<em>sing-box for Apple platforms</em>、<em>sing-box for Desktop</em></li>
        <li>或 <a href="https://github.com/hiddify/hiddify-app" target="_blank" rel="noopener">Hiddify</a> &mdash; 基于 sing-box 内核的客户端，按其 README 的说明接受 sing-box 格式的配置（Android、iOS、Windows、macOS、Linux）</li>
        <li>配置中有一个可用的代理 outbound &mdash; 协议不限</li>
        <li>Chrome 中已安装 <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> 扩展</li>
    </ul>
    <div class="callout">
        <strong>NekoBox for Android</strong> 同样运行在 sing-box 内核上，但按其 README 的说明，它只从订阅中获取节点，忽略路由规则。rule-set 只有包含在完整的 sing-box 配置中才能进入该应用。
    </div>''',
        },
        {
            'h2': '步骤 1. 在 NetRoute 中生成 rule-set',
            'html': '''    <ol>
        <li>在 Chrome 中打开目标网站并刷新页面，让扩展的嗅探器看到后台请求</li>
        <li>启动 <strong>NetRoute</strong></li>
        <li>在 <strong>「目标系统」</strong> 中选择 <strong>sing-box / Hiddify / NekoBox</strong> &mdash; 位于「代理客户端」分组</li>
        <li><strong>「网关 IP」</strong> 和 <strong>「网络设备」</strong> 字段不影响此格式</li>
        <li>点击 <strong>「分析网站」</strong></li>
        <li>在 <strong>「域名列表」</strong> 标签页中取消勾选不需要的项 &mdash; 统计计数器、广告网络、第三方 CDN；规则会立即更新</li>
        <li>点击 <strong>「下载」</strong>：文件以网站命名，例如 <code>github_com_rules.json</code></li>
    </ol>
    <div class="callout">
        <strong>关于网段。</strong>只要有已解析的地址，<code>ip_cidr</code> 规则就总会出现在文件中，它不会妨碍域名规则。只想要域名 &mdash; 从文件中删除第二条规则。想要更少的网段 &mdash; 在 <strong>「路由模式」</strong> 中选择 <strong>IPv4 Only</strong>：规则中将不再包含 IPv6 前缀。
    </div>''',
        },
        {
            'h2': '步骤 2. 在 sing-box 配置中描述该文件',
            'html': '''    <p>与配置放在一起的本地文件。当路径以 <code>.json</code> 或 <code>.srs</code> 结尾时可以省略 <code>format</code>；自 1.10.0 起，文件变化时 sing-box 会自行重新加载。</p>
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
        <li><code>outbound</code> &mdash; 你的代理 outbound 的 tag。自 sing-box 1.11.0 起必须写 <code>"action": "route"</code>：直接写在规则中的旧 <code>outbound</code> 字段在该版本已被弃用。</li>
        <li><code>final</code> &mdash; 所有未匹配任何规则的流量的默认 outbound；<code>direct</code> 即经典的分流。</li>
    </ul>
    <p>通过 URL 引用的文件。将 <code>.json</code> 放到 GitHub 仓库或自己的服务器上，并给出原始文件的直接链接；默认情况下 sing-box 每天刷新一次（<code>update_interval</code> = <code>1d</code>）：</p>
    <pre><code>{
  "type": "remote",
  "tag": "netroute",
  "format": "source",
  "url": "https://raw.githubusercontent.com/you/rules/main/github_com_rules.json",
  "update_interval": "1d"
}</code></pre>
    <p>如果该链接必须通过代理下载：在 sing-box 1.13 及之前由带 outbound tag 的 <code>download_detour</code> 字段完成；1.14.0 将其弃用并改用 <code>http_client</code>，1.16.0 将其移除。</p>
    <div class="callout">
        <strong>Hiddify。</strong>该应用接受 sing-box 格式的配置 &mdash; 把上面的 <code>route</code> 块连同你的 outbound 一起加入这样的配置，并将其作为配置文件（profile）导入。你所用 Hiddify 版本中具体如何导入配置文件，请参阅应用的文档。
    </div>''',
        },
        {
            'h2': '步骤 3. 检查',
            'html': '''    <p>检查配置连同 rule-set 的语法：</p>
    <pre><code>sing-box check -c config.json</code></pre>
    <p>然后启动 sing-box 并打开网站。如果该网站通过代理打开，而其他网站直连 &mdash; 规则生效。如果没有，请查看下面的常见问题。</p>''',
        },
        {
            'h2': '编译后的 rule-set（.srs）',
            'html': '''    <p>对于大型列表，sing-box 提供二进制格式。使用文档中的命令编译 NetRoute 文件：</p>
    <pre><code>sing-box rule-set compile github_com_rules.json
# → github_com_rules.srs</code></pre>
    <p>在配置中设置 <code>"format": "binary"</code> 和 <code>.srs</code> 的路径。对于十几个网站来说没有必要这样做。</p>''',
        },
        {
            'h2': '常见问题',
            'html': '''    <h3>sing-box 拒绝该文件</h3>
    <p>rule-set 在 sing-box 1.8.0 中出现；更早的版本以及基于它们构建的客户端不认识这种格式。NetRoute 写入最低的 <code>version: 1</code> &mdash; 之后的每个版本都能读取。</p>

    <h3>规则没有匹配到子域名</h3>
    <p><code>domain_suffix</code> 只覆盖列表中域名的子域名。如果网站从另一个域名拉取数据，它应该出现在 NetRoute 的 <strong>「域名列表」</strong> 标签页中。扫描前先在网站上浏览一遍 &mdash; 登录、打开一个视频 &mdash; 让扩展的嗅探器也能看到延迟发出的请求。</p>

    <h3>按 IP 发起的连接绕过了代理</h3>
    <p>域名规则需要 sing-box 知道目标名称。这正是嗅探的用途：它从 HTTP 的 Host 字段以及 TLS 和 QUIC 的 Server Name 中获取名称。自 sing-box 1.11.0 起，嗅探通过 <code>route.rules</code> 中带 <code>"action": "sniff"</code> 的规则启用（inbound 上旧的 <code>sniff</code> 字段已弃用，并在 1.13.0 中移除）。没有名称的连接由 <code>ip_cidr</code> 规则匹配 &mdash; 对于地址经常变化的服务，请在 NetRoute 选项中启用 <strong>「路由优化 &rarr; BGP 前缀」</strong>：网段将变为公告的前缀而不是单个地址。</p>

    <h3>一个 rule-set 包含多个网站</h3>
    <p>点击分析按钮旁的 <strong>「URL 列表」</strong> 并粘贴网站列表 &mdash; NetRoute 会为所有网站生成一个 rule-set，文件名为 <code>bulk_N_rules.json</code>。</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS 与泄漏',
        'html': '''    <p>域名规则不会改变浏览器解析名称的方式：对 <code>github.com</code> 的 DNS 查询仍然发往系统或浏览器自身配置的解析器，若那是运营商的解析器，运营商就能看到网站的名称。</p>
    <ul>
        <li>在 sing-box 中，DNS 规则可以引用同一个 rule-set：一条带 <code>"rule_set": "netroute"</code>、<code>"action": "route"</code> 和 <code>server</code> 的 <code>dns.rules</code> 记录会把这些域名的查询发送到所选的 DNS 服务器。要让该服务器本身走代理，给它设置带 outbound tag 的 <code>detour</code> &mdash; 这是共享 Dial Fields 中的一个字段；新格式的服务器（<code>"type": "https"</code> 等）在 sing-box 1.12.0 中出现。</li>
        <li>在 Chrome 中关闭「使用安全 DNS」或将其指向你信任的解析器：浏览器自己的 DNS-over-HTTPS 会绕过系统解析器 &mdash; 参见项目的 <a href="https://github.com/Alexander2k/netroute-site" target="_blank" rel="noopener">Troubleshooting 部分</a>。</li>
    </ul>
    <p>检查：开启客户端后，<a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> 应显示代理的解析器，而不是运营商的。</p>''',
    },
    'official_docs': [
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/', 'label': 'sing-box：Rule Set &mdash; local 与 remote 字段'},
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/source-format/', 'label': 'sing-box：Source Format &mdash; version、compile 命令'},
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/headless-rule/', 'label': 'sing-box：Headless Rule &mdash; domain_suffix、ip_cidr'},
        {'url': 'https://sing-box.sagernet.org/configuration/route/rule_action/', 'label': 'sing-box：Rule Action &mdash; route、sniff'},
        {'url': 'https://sing-box.sagernet.org/configuration/dns/rule/', 'label': 'sing-box：DNS Rule'},
        {'url': 'https://github.com/hiddify/hiddify-app', 'label': 'Hiddify &mdash; README：支持的配置格式'},
    ],
    'shot_format': 'singbox',
    'shot_caption': '选择「sing-box / Hiddify / NekoBox」格式的 NetRoute 弹窗：「路由」标签页中是生成好的 rule-set，计数器显示规则数量。扫描数据：github.com 页面。',
    'example_file': 'singbox-rules.json',
    'example_desc': '源格式的 rule-set，包含 <code>domain_suffix</code> 和 <code>ip_cidr</code> 规则',
    'card': {
        'badge': 'proxy',
        'badge_label': '代理客户端',
        'title': 'sing-box / Hiddify',
        'text': '包含网站域名和网段的 rule-set：route.rule_set 中的本地文件或 URL，编译为 .srs。',
    },
    'related_desc': '用于 sing-box 和 Hiddify 的 rule-set',
    'date_published': '2026-10-16',
}

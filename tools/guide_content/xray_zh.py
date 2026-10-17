# 指南：Xray 路由规则 — Xray-core、3X-UI、v2rayN、Streisand。简体中文。
# 事实与来源同 xray_ru.py（2026-10-17 核对）；扩展界面文案来自 _locales/zh_CN。
PAGE = {
    'title': '从任意网站生成 Xray 路由规则：适用于 Xray-core、3X-UI 和 v2rayN — 指南 | NetRoute',
    'description': '如何在 NetRoute 中获取包含网站域名和网段的 Xray routing.rules，并将其应用于 Xray-core 配置、3X-UI 面板的 Xray 设置，或通过规则导入功能导入 v2rayN。',
    'keywords': 'xray routing rules, xray 路由规则, xray domain: outboundTag, xray 分流, 3x-ui 路由规则, 3x-ui xray settings routing, v2rayn 导入规则, v2rayn routing setting, v2rayn 自定义路由规则, xray json routing',
    'og_title': '从任意网站生成 Xray 路由规则',
    'og_description': 'NetRoute 将网站的域名和网段整理为 Xray routing.rules — 用于 Xray-core 配置、3X-UI 面板以及 v2rayN 的规则导入。',
    'breadcrumb': 'Xray',
    'h1': '从任意网站生成 Xray 路由规则：Xray-core、3X-UI、v2rayN',
    'lead': 'Xray 依据 <code>routing.rules</code> 转发连接：域名和地址的列表加上一个 outbound 的 tag。NetRoute 可从网站生成两种变体的此类规则：一段 Xray-core 配置片段 &mdash; 同样适用于以 JSON 形式编辑 Xray 配置的 3X-UI 面板 &mdash; 以及一个用于向 v2rayN 导入规则的文件。',
    'howto': {
        'name': '如何应用 NetRoute 生成的 Xray 路由规则',
        'description': '使用 NetRoute 扩展生成 Xray 或 v2rayN 格式的规则，将其粘贴到 Xray-core 配置的 routing.rules 中、3X-UI 面板的 Xray 设置中，或从剪贴板导入 v2rayN。',
        'total_time': 'PT5M',
        'steps': [
            {'name': '在 NetRoute 中生成规则', 'text': '在 Chrome 中打开目标网站，启动 NetRoute，在「目标系统」中选择「Xray / 3X-UI / Streisand」或「v2rayN (rules import)」，在「网络设备」字段中填入你的 outbound 的 tag（默认为 proxy），点击「分析网站」并下载文件。'},
            {'name': '插入规则', 'text': 'Xray-core 和 3X-UI：将 rules 中的对象添加到配置中 routing.rules 的开头。v2rayN：Routing → Routing Setting → Import Rules From Clipboard，在询问是否追加时回答「yes」以保留现有规则。'},
            {'name': '检查', 'text': '重启 Xray（3X-UI 面板会自行重新加载）并打开网站 — 它应通过带有指定 tag 的 outbound 出站。'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': '文件内容',
            'html': '''    <p><strong>「Xray / 3X-UI / Streisand」格式</strong>是带有 <code>routing</code> 部分的 Xray-core 配置片段。域名和网段是两条规则，各有自己的列表，共用一个 <code>outboundTag</code>：</p>
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
        <li><code>domain:name</code> &mdash; 按 Xray 文档，表示该域名本身及其子域名。列表已折叠：当同时找到 <code>api.github.com</code> 和 <code>github.com</code> 时，只保留 <code>github.com</code>；<code>www.</code> 已去掉。扫描到的所有域名都包含在内，包括未能解析出 IP 的域名。</li>
        <li><code>ip</code> &mdash; CIDR 形式的地址；即 NetRoute 为路由器输出路由时所用的同一批聚合网段，IPv4 和 IPv6。</li>
        <li><code>outboundTag</code> &mdash; 来自 NetRoute 中 <strong>「网络设备」</strong> 字段的 outbound 的 tag；默认为 <code>proxy</code>。</li>
        <li><code>domainStrategy: IPIfNonMatch</code> &mdash; 按 Xray 文档，只有在没有规则按名称匹配时才把域名解析为地址；Xray 自身的默认值是 <code>AsIs</code>，不做解析。</li>
    </ul>
    <p><strong>「v2rayN (rules import)」格式</strong>是一个规则数组，形式与 v2rayN 从剪贴板或文件导入时的一致（同 v2rayN 作者的 <code>v2rayCustomRoutingList</code> 仓库）：</p>
    <pre><code>[
  { "port": "", "outboundTag": "proxy", "domain": ["domain:github.com", "domain:githubusercontent.com"], "enabled": true, "remarks": "NetRoute github.com domains" },
  { "port": "", "outboundTag": "proxy", "ip": ["140.82.112.0/20", "185.199.108.0/22", "2606:50c0::/32"], "enabled": true, "remarks": "NetRoute github.com networks" }
]</code></pre>''',
        },
        {
            'h2': '准备工作',
            'html': '''    <ul>
        <li>已配置 outbound 且知道其 tag 的 Xray-core &mdash; 在电脑、服务器上或 <a href="https://github.com/MHSanaei/3x-ui" target="_blank" rel="noopener">3X-UI</a> 面板中</li>
        <li>或适用于 Windows、Linux 或 macOS 的 <a href="https://github.com/2dust/v2rayN" target="_blank" rel="noopener">v2rayN</a> &mdash; 带有 Xray 和 sing-box 内核的客户端</li>
        <li>Chrome 中已安装 <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> 扩展</li>
    </ul>''',
        },
        {
            'h2': '步骤 1. 在 NetRoute 中生成规则',
            'html': '''    <ol>
        <li>在 Chrome 中打开目标网站并刷新页面，让扩展的嗅探器看到后台请求</li>
        <li>启动 <strong>NetRoute</strong></li>
        <li>在 <strong>「目标系统」</strong> 的「代理客户端」分组中，为 Xray-core 配置选择 <strong>Xray / 3X-UI / Streisand</strong>，或为导入 v2rayN 选择 <strong>v2rayN (rules import)</strong></li>
        <li>在 <strong>「网络设备」</strong> 字段中输入你的 outbound 的 tag &mdash; 占位提示显示默认值 <code>proxy</code>。<strong>「网关 IP」</strong> 字段不影响这些格式</li>
        <li>点击 <strong>「分析网站」</strong></li>
        <li>在 <strong>「域名列表」</strong> 标签页中取消勾选不需要的项 &mdash; 规则会立即更新</li>
        <li>点击 <strong>「下载」</strong>：文件以网站命名，例如 <code>github_com_rules.json</code></li>
    </ol>''',
        },
        {
            'h2': '步骤 2a. Xray-core：将规则插入配置',
            'html': '''    <p>打开 Xray 的 <code>config.json</code>，将 <code>rules</code> 中的两个对象添加到 <code>routing.rules</code> 数组中、通用规则的<strong>上方</strong>。按 Xray 文档，规则自上而下检查，第一个匹配的生效；未匹配任何规则的连接从配置中的第一个 outbound 出站。确认 <code>outboundTag</code> 与你的代理 outbound 的 tag 一致，且 <code>domainStrategy</code> 在 <code>routing</code> 部分只设置一次。</p>
    <p>重启 Xray。</p>''',
        },
        {
            'h2': '步骤 2b. 3X-UI：Xray 设置中的规则',
            'html': '''    <p>3X-UI 是面向 Xray-core 服务器的 Web 面板。按其文档，路由规则就是 Xray 规则，带有 <code>domain</code>、<code>ip</code>、<code>port</code>、<code>network</code>、<code>protocol</code>、<code>inboundTag</code>、<code>sourceIP</code> 匹配条件以及 <code>outboundTag</code> 或 <code>balancerTag</code> 目标；没有单独的逐条规则编辑器 &mdash; 你在 <strong>Xray Settings</strong>（Xray 设置）中编辑配置的 JSON，面板会自行重新加载 Xray。</p>
    <ol>
        <li>在面板中打开 <strong>Xray Settings</strong></li>
        <li>在 JSON 中找到 <code>routing.rules</code> 数组，并把 NetRoute 文件中的两个对象插入其开头</li>
        <li>将所需 outbound 的 tag 填入 <code>outboundTag</code> &mdash; 例如 WARP 连接或另一台服务器，如果这些网站应走那条路径</li>
        <li>保存 &mdash; 面板会重新加载 Xray</li>
    </ol>
    <p>在服务器上，这条规则的含义是：客户端发往这些域名和网段的流量由服务器发送到指定的 outbound，其余流量按规则列表后面的配置处理。</p>''',
        },
        {
            'h2': '步骤 2c. v2rayN：导入规则',
            'html': '''    <p>对于 v2rayN，在 NetRoute 中选择 <strong>v2rayN (rules import)</strong> 格式。需要参照的 v2rayN 界面文字如下：</p>
    <ol>
        <li>打开下载的文件，将其内容复制到剪贴板</li>
        <li>在 v2rayN 中打开 <strong>Routing</strong> &rarr; <strong>Routing Setting</strong></li>
        <li>选择 <strong>Import Rules From Clipboard</strong>（还有 <strong>Import Rules From File</strong> 和 <strong>Import Rules From Subscription URL</strong>）</li>
        <li>对于提问 <em>“Do you want to append rules? Choose yes to append, no to replace.”</em>（是否追加规则？选 yes 追加，选 no 替换），回答 <strong>Yes</strong> 以将规则添加到现有规则中</li>
        <li>检查这些规则所在的规则集已被标记为激活（<strong>Set as active rule</strong>）</li>
    </ol>
    <p>在 v2rayN 的规则编辑器中，同样的列表出现在 <strong>Domain</strong> 和 <strong>IP or IP CIDR</strong> 字段中；条目语法与 Xray 相同，v2rayN 的 wiki 也为此指向 Xray 文档。</p>''',
        },
        {
            'h2': '步骤 3. 检查',
            'html': '''    <p>打开网站 &mdash; 它应通过规则中 tag 对应的 outbound 出站，其他网站与之前一样。如果网站打不开或绕过了代理，请查看常见问题。</p>''',
        },
        {
            'h2': '常见问题',
            'html': '''    <h3>规则不生效</h3>
    <p>规则自上而下检查，第一个匹配的生效 &mdash; 如果上方的某条规则已经接管了这部分流量（例如通用的 <code>geosite</code> 规则），NetRoute 的规则就永远轮不到。请把 NetRoute 的规则上移。</p>

    <h3>编辑后 Xray 无法启动</h3>
    <p>检查 JSON：多余的逗号或第二个 <code>routing</code> 部分都会破坏配置。只需插入 <code>rules</code> 数组中的对象，而不是整个文件。</p>

    <h3>找不到 tag</h3>
    <p><code>outboundTag</code> 必须与某个现有 outbound 的 tag 逐字一致。在 NetRoute 中，tag 在扫描前于 <strong>「网络设备」</strong> 字段中设置。</p>

    <h3>Streisand</h3>
    <p>Streisand 是适用于 iOS、macOS 和 visionOS 的客户端，支持基于规则的代理设置（其 App Store 描述中的“Rule-based Proxy Setup”）。如何向其中添加自己的规则，请参阅应用的文档；NetRoute 文件中的域名和网段列表适合此用途。</p>

    <h3>一个文件包含多个网站</h3>
    <p>点击分析按钮旁的 <strong>「URL 列表」</strong> 并粘贴网站列表 &mdash; NetRoute 会为所有网站生成一组规则，文件名为 <code>bulk_N_rules.json</code>。</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS 与泄漏',
        'html': '''    <p>Xray 中的域名规则与目标名称进行匹配；名称如何解析、在哪里解析由你配置中的 <code>domainStrategy</code> 和 <code>dns</code> 部分决定 &mdash; NetRoute 的规则不会改变它们。浏览器的查询发往其自身配置的 DNS：在 Chrome 中关闭「使用安全 DNS」或将其指向你信任的解析器，否则 Chrome 会绕过客户端解析名称。</p>
    <p>检查：开启客户端后，<a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> 不应显示运营商的解析器。</p>''',
    },
    'official_docs': [
        {'url': 'https://xtls.github.io/config/routing.html', 'label': 'Xray：Routing &mdash; domainStrategy、规则顺序、domain 和 ip 的形式 (zh)'},
        {'url': 'https://github.com/MHSanaei/3x-ui', 'label': '3X-UI &mdash; README 与面板文档'},
        {'url': 'https://github.com/MHSanaei/3x-ui/blob/main/docs/content/docs/en/operations/outbounds-routing.mdx', 'label': '3X-UI：Outbounds &amp; Routing'},
        {'url': 'https://github.com/2dust/v2rayN/wiki/Description-of-custom-routing-rules', 'label': 'v2rayN：自定义路由规则说明 (zh)'},
        {'url': 'https://github.com/2dust/v2rayCustomRoutingList', 'label': 'v2rayN：用于导入的规则列表格式'},
    ],
    'shot_format': 'xray',
    'shot_caption': '选择「Xray / 3X-UI / Streisand」格式的 NetRoute 弹窗：「网络设备」字段中是 proxy tag，「路由」标签页中是 routing.rules 片段。扫描数据：github.com 页面。',
    'example_file': 'xray-routing.json',
    'example_desc': '带有 <code>routing</code> 部分的 Xray-core 配置片段；旁边的 <code>v2rayn-rules.json</code> 用于导入 v2rayN',
    'card': {
        'badge': 'proxy',
        'badge_label': '代理客户端',
        'title': 'Xray / 3X-UI / v2rayN',
        'text': '包含网站域名和网段的 routing.rules：用于 Xray-core 配置、3X-UI 面板的 Xray 设置，或 v2rayN 的规则导入。',
    },
    'related_desc': '用于 Xray-core、3X-UI 和 v2rayN 的 routing.rules',
    'date_published': '2026-10-17',
}

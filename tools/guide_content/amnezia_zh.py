# 指南：用于分流的 AmneziaVPN 网站列表。简体中文。
# 事实与来源同 amnezia_ru.py（2026-10-17 核对）；扩展界面文案来自 _locales/zh_CN；
# AmneziaVPN 的界面名称沿用 docs.amnezia.org/documentation/instructions/vpn-split-tunneling（英文）。
PAGE = {
    'title': '从任意网站生成 AmneziaVPN 网站列表：按地址分流 — 指南 | NetRoute',
    'description': '如何在 NetRoute 中获取包含网站地址和子网、可导入 AmneziaVPN 的文件，并为网站开启分流：模式、通过 ⋮ 菜单导入、IPv4 和 Amnezia Free 的限制。',
    'keywords': 'amnezia split tunneling, amneziavpn 分流 网站, amnezia 网站列表, amnezia 导入 ip-list.json, amnezia only the sites listed here, amneziawg 分流 网站, amnezia 服务子网',
    'og_title': '从任意网站生成 AmneziaVPN 网站列表',
    'og_description': 'NetRoute 将网站的地址和子网整理为可导入 AmneziaVPN 的文件 — 三步完成网站分流。',
    'breadcrumb': 'AmneziaVPN',
    'h1': '从任意网站生成 AmneziaVPN 网站列表',
    'lead': 'AmneziaVPN 可以只让列表中的地址通过 VPN &mdash; 即网站分流。列表由 IPv4 地址和子网组成，为一个拥有几十个域名的网站手工整理列表很费时间。NetRoute 直接从页面完成这件事：打开网站，点击「分析网站」，下载用于导入的文件。',
    'howto': {
        'name': '如何将 NetRoute 的网站列表导入 AmneziaVPN',
        'description': '使用 NetRoute 扩展生成 AmneziaVPN 列表，在网站分流设置中通过 ⋮ 菜单导入文件，并开启「Only the sites listed here will be accessed through the VPN」模式。',
        'total_time': 'PT5M',
        'steps': [
            {'name': '在 NetRoute 中生成列表', 'text': '在 Chrome 中打开目标网站，启动 NetRoute，在「目标系统」中选择「AmneziaVPN (site list)」，点击「分析网站」并下载 <网站>_rules.json。'},
            {'name': '将文件导入 AmneziaVPN', 'text': '打开网站分流设置，在 ⋮ 菜单中选择导入 — 替换列表或添加到现有列表 — 然后选择文件。'},
            {'name': '开启模式并连接', 'text': '选择「Only the sites listed here will be accessed through the VPN」模式，启用分流并连接 VPN。'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': '文件内容',
            'html': '''    <p>该文件是一个 JSON 数组，条目形式与 AmneziaVPN 自身导出列表时一致：每个条目有 <code>hostname</code>、地址列表 <code>ips</code>，以及其中第一个地址 <code>ip</code> &mdash; 供旧版本应用使用。</p>
    <pre><code>[
  { "hostname": "api.github.com", "ips": ["140.82.112.4"], "ip": "140.82.112.4" },
  { "hostname": "github.com", "ips": ["140.82.112.3"], "ip": "140.82.112.3" },
  { "hostname": "140.82.112.0/20", "ips": [], "ip": "" },
  { "hostname": "185.199.108.0/22", "ips": [], "ip": "" }
]</code></pre>
    <ul>
        <li><strong>带地址的主机。</strong>按客户端源代码，AmneziaVPN 在导入时不解析名称 &mdash; 条目按原样保存，只有手动添加网站时才会解析。因此 NetRoute 为每个主机写入扫描期间找到的 IPv4 地址；没有 IPv4 地址的主机不会写入。名称不折叠：<code>www.ozon.ru</code> 和 <code>ozon.ru</code> 是各自带有自己地址的独立条目。</li>
        <li><strong>子网。</strong>主机之后是聚合的 IPv4 子网 &mdash; 即 NetRoute 为路由器输出路由时所用的同一批；启用 <strong>「路由优化 &rarr; BGP 前缀」</strong> 后，这些是提供商公告的前缀而不是单个地址。</li>
        <li><strong>仅 IPv4。</strong>按 AmneziaVPN 文档，不支持 IPv6；IPv6 地址不会写入文件。</li>
    </ul>''',
        },
        {
            'h2': '准备工作',
            'html': '''    <ul>
        <li>已配置连接的 <a href="https://amnezia.org/" target="_blank" rel="noopener">AmneziaVPN</a> 应用。按文档说明，按地址分流在 Amnezia Free 中不可用</li>
        <li>支持按地址分流的平台：按文档说明，iOS、macOS 和 Linux 只支持按地址分流，Windows 和 Android 则同时支持按地址和按应用分流</li>
        <li>Chrome 中已安装 <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> 扩展</li>
    </ul>''',
        },
        {
            'h2': '步骤 1. 在 NetRoute 中生成列表',
            'html': '''    <ol>
        <li>在 Chrome 中打开目标网站并刷新页面，让扩展的嗅探器看到后台请求</li>
        <li>启动 <strong>NetRoute</strong></li>
        <li>在 <strong>「目标系统」</strong> 中选择 <strong>AmneziaVPN (site list)</strong> &mdash; 位于「VPN 客户端」分组</li>
        <li><strong>「网关 IP」</strong> 和 <strong>「网络设备」</strong> 字段不影响此格式</li>
        <li>点击 <strong>「分析网站」</strong></li>
        <li>在 <strong>「域名列表」</strong> 标签页中取消勾选不需要的项 &mdash; 统计计数器、广告网络、第三方 CDN；列表会立即更新</li>
        <li>点击 <strong>「下载」</strong>：文件以网站命名，例如 <code>github_com_rules.json</code></li>
    </ol>
    <div class="callout">
        <strong>关于变化的地址。</strong>AmneziaVPN 文档提醒：从域名获得的地址不会自动更新，而大型服务需要整个子网。因此在扫描前请在 NetRoute 选项中启用 <strong>「路由优化 &rarr; BGP 前缀」</strong> &mdash; 文件中将包含公告的子网，它们能经受住 CDN 的地址轮换。
    </div>''',
        },
        {
            'h2': '步骤 2. 将文件导入 AmneziaVPN',
            'html': '''    <p>按 AmneziaVPN 文档，列表从网站分流设置中导入：</p>
    <ol>
        <li>打开 <strong>Split tunneling</strong>（分流）并进入网站分流设置</li>
        <li>点击 <strong>⋮</strong> 图标并选择导入：替换列表 &mdash; 从头开始时；或将导入的网站添加到现有网站 &mdash; 扩充列表时</li>
        <li>选择下载的文件；条目会出现在列表中</li>
    </ol>''',
        },
        {
            'h2': '步骤 3. 开启模式并连接',
            'html': '''    <ol>
        <li>选择 <strong>Only the sites listed here will be accessed through the VPN</strong>（仅此处列出的网站通过 VPN 访问）模式 &mdash; 只有文件中的网站走隧道，其余流量直连。另一种模式 <strong>Addresses from the list should not be accessed via VPN</strong>（列表中的地址不通过 VPN 访问）则相反：把列表排除在隧道之外</li>
        <li>启用网站分流</li>
        <li>连接 VPN</li>
    </ol>''',
        },
        {
            'h2': '步骤 4. 检查',
            'html': '''    <p>打开为其生成列表的网站：它应通过 VPN 打开，列表之外的网站直连。如果网站只能部分打开 &mdash; 说明它的一部分域名不在列表中：检查 NetRoute 的 <strong>「域名列表」</strong> 标签页，扫描前先在网站上浏览一遍（登录、打开一个视频），让嗅探器看到延迟发出的请求，然后以替换列表的方式重新导入文件。</p>''',
        },
        {
            'h2': '常见问题',
            'html': '''    <h3>文件无法导入</h3>
    <p>按客户端源代码，文件必须是由对象组成的 JSON 数组；纯字符串数组会被拒绝。NetRoute 文件已经是正确的形式 &mdash; 请检查它是否完整下载，且没有在会替换引号的文本编辑器中编辑过。</p>

    <h3>网站起初可用，后来不行了</h3>
    <p>网站的地址变了。在 NetRoute 中重新生成文件 &mdash; 启用 <strong>「BGP 前缀」</strong> 后，文件包含子网而不是单个地址 &mdash; 然后以替换列表的方式导入。</p>

    <h3>无关流量走了 VPN</h3>
    <p>AmneziaVPN 文档提醒：大型服务的宽泛子网可能捕获无关流量。在 NetRoute 的 <strong>「域名列表」</strong> 标签页中取消勾选第三方 CDN，或对这类网站关闭 BGP 优化。</p>

    <h3>与自己服务器的连接断开</h3>
    <p>按文档说明，当你的 VPN 服务器地址落入某个已添加的子网时，连接会中断 &mdash; 请从列表中删除该子网。</p>

    <h3>一个列表包含多个网站</h3>
    <p>点击分析按钮旁的 <strong>「URL 列表」</strong> 并粘贴网站列表 &mdash; NetRoute 会为所有网站生成一个文件，名为 <code>bulk_N_rules.json</code>。</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS 与泄漏',
        'html': '''    <p>AmneziaVPN 的分流按地址工作：发往列表中地址的流量进入隧道，而浏览器的 DNS 查询发往其解析器所配置的地方。若那是运营商的解析器，即使流量本身通过 VPN，它也能看到网站的名称。在 Chrome 中关闭「使用安全 DNS」或将其指向你信任的解析器；AmneziaVPN 自身的 DNS 设置请参阅其文档。</p>
    <p>检查：连接 VPN 后，<a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> 会显示是谁的解析器在回答你的查询。</p>''',
    },
    'official_docs': [
        {'url': 'https://docs.amnezia.org/documentation/instructions/vpn-split-tunneling', 'label': 'AmneziaVPN：分流 &mdash; 模式、导入、限制'},
        {'url': 'https://github.com/amnezia-vpn/amnezia-client', 'label': 'AmneziaVPN：客户端源代码 &mdash; ipSplitTunnelingController 中的导入格式'},
        {'url': 'https://amnezia.org/blog/what-is-split-tunneling-and-why-you-need-it', 'label': 'Amnezia：什么是分流'},
    ],
    'shot_format': 'amnezia',
    'shot_caption': '选择「AmneziaVPN (site list)」格式的 NetRoute 弹窗：「路由」标签页中是用于导入的列表，带地址的主机和子网。扫描数据：github.com 页面。',
    'example_file': 'amnezia-sites.json',
    'example_desc': '用于导入 AmneziaVPN 的列表：带地址的主机和子网',
    'card': {
        'badge': 'vpn',
        'badge_label': 'VPN 客户端',
        'title': 'AmneziaVPN',
        'text': '用于分流的网站列表：带 IPv4 地址的主机和子网，通过 ⋮ 菜单导入。',
    },
    'related_desc': '用于分流的网站列表',
    'date_published': '2026-10-17',
}

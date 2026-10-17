# 生成指南页面的通用界面文案（简体中文）。可包含 HTML。
# 指南中引用的扩展界面文案来自 _locales/zh_CN/messages.json：「目标系统」「网关 IP」「网络设备 (可选)」
# 「分析网站」、标签页「路由」/「域名列表」、「下载」「路由模式」「路由优化」「URL 列表」、分组「代理客户端」/「VPN 客户端」。
UI = {
    'home': '首页',
    'guides': '指南',
    'back': '&larr; 返回首页',
    'examples_h2': '配置文件示例',
    'examples_p': '可直接编辑的模板。将示例中的域名和网段替换为 NetRoute 为目标网站生成的输出。',
    'comments_hint': '<strong>提示：</strong>文本格式下载时带有注释头。在 NetRoute 选项中取消勾选 <strong>「在导出文件中包含注释」</strong> 即可只保留规则；JSON 格式不含注释。',
    'all_examples': '在 GitHub 上查看所有示例 &rarr;',
    'official_docs': '官方文档',
    'related': '相关指南',
    'cta_h3': '准备好尝试了吗？',
    'cta_p': 'NetRoute — 免费的 Chrome 扩展，可从任何网站生成路由。',
    'cta_btn': '安装扩展',
    'updated': '更新于',
    'version_word': '版本',
    'shot_alt_default': '扫描 github.com 后的 NetRoute 弹窗：已选择的格式和「路由」标签页中的结果',
    'shot_caption_default': 'NetRoute 中的结果：在「目标系统」中选择格式，输出显示在「路由」标签页。扫描数据：github.com 页面。',
    'classic_names': {
        'keenetic': 'Keenetic', 'mikrotik': 'MikroTik', 'wireguard': 'WireGuard', 'linux': 'Linux', 'openvpn': 'OpenVPN',
    },
    'classic_related': {
        'keenetic': '通过 <code>.bat</code> 文件上传路由',
        'mikrotik': '将 <code>.rsc</code> 脚本导入 RouterOS',
        'wireguard': '通过 <code>AllowedIPs</code> 分流',
        'linux': '<code>ip route</code> shell 脚本',
        'openvpn': '客户端配置中的 <code>route</code> 指令',
    },
}

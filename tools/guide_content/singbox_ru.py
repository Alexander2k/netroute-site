# Инструкция: sing-box rule-set (Hiddify, NekoBox, Karing, sing-box). Русский.
PAGE = {
    'title': 'Правила sing-box из любого сайта: rule-set для Hiddify и NekoBox — инструкция | NetRoute',
    'description': 'Как получить rule-set sing-box с доменами и сетями сайта в NetRoute и подключить его в Hiddify, NekoBox, Karing или sing-box: локальный файл, ссылка, компиляция в .srs, проверка.',
    'keywords': 'sing-box rule-set, sing-box rule_set source, hiddify правила маршрутизации, hiddify rule set, nekobox rule set, sing-box domain_suffix ip_cidr, sing-box srs compile, split tunneling sing-box, маршрутизация по доменам sing-box',
    'og_title': 'Правила sing-box из любого сайта: rule-set для Hiddify и NekoBox',
    'og_description': 'NetRoute собирает домены и сети сайта в rule-set sing-box. Подключите его в Hiddify, NekoBox, Karing или sing-box за три шага.',
    'breadcrumb': 'sing-box',
    'h1': 'Правила sing-box из любого сайта: rule-set для Hiddify и NekoBox',
    'lead': 'Клиенты на ядре sing-box &mdash; Hiddify, NekoBox, Karing, официальные приложения SFA/SFI/SFM &mdash; решают, что пускать через прокси, по <strong>правилам</strong>: списку доменов и сетей. NetRoute генерирует такой список в формате rule-set прямо со страницы сайта: открыли сайт, нажали «Анализировать», скачали <code>.json</code> &mdash; и подключили.',
    'howto': {
        'name': 'Как подключить rule-set NetRoute в sing-box, Hiddify или NekoBox',
        'description': 'Сгенерируйте rule-set в формате sing-box в расширении NetRoute, сохраните файл или опубликуйте по ссылке и добавьте правило route.rules с outbound прокси.',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Сгенерируйте rule-set в NetRoute', 'text': 'Откройте нужный сайт в Chrome, запустите NetRoute, в списке форматов выберите «sing-box / Hiddify / NekoBox», нажмите «Анализировать» и скачайте файл <сайт>_rules.json.'},
            {'name': 'Подключите rule-set в конфиге', 'text': 'В секции route.rule_set опишите файл как type: local, format: source (или type: remote с url, если файл опубликован), а в route.rules добавьте правило rule_set: netroute с outbound вашего прокси.'},
            {'name': 'Проверьте', 'text': 'Выполните sing-box check -c config.json, запустите клиент и откройте сайт: в логах sing-box должно быть совпадение по rule_set=netroute.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'Что внутри файла',
            'html': '''    <p>Rule-set в исходном формате (<code>source</code>) &mdash; это JSON с версией и списком правил. NetRoute пишет домены и сети <strong>двумя отдельными правилами</strong>: в sing-box условия внутри одного правила объединяются по «И», и правило с доменами и сетями вместе никогда бы не сработало.</p>
    <pre><code>{
  "version": 1,
  "rules": [
    { "domain_suffix": ["github.com", "githubusercontent.com"] },
    { "ip_cidr": ["140.82.112.0/20", "185.199.108.0/22", "2606:50c0::/32"] }
  ]
}</code></pre>
    <ul>
        <li><code>domain_suffix</code> &mdash; домен и все его поддомены. NetRoute сворачивает список: если найдены <code>api.github.com</code> и <code>github.com</code>, остаётся только <code>github.com</code>, а <code>www.</code> отбрасывается.</li>
        <li><code>ip_cidr</code> &mdash; агрегированные сети, IPv4 и IPv6 вместе: те же маршруты, что NetRoute выдал бы для роутера, включая режимы BGP Prefix и Full AS.</li>
        <li><code>version: 1</code> &mdash; формат sing-box 1.8 и новее; все последующие версии читают его без изменений.</li>
    </ul>''',
        },
        {
            'h2': 'Что понадобится',
            'html': '''    <ul>
        <li>Клиент на sing-box: <a href="https://github.com/hiddify/hiddify-app" target="_blank" rel="noopener">Hiddify</a>, <a href="https://github.com/MatsuriDayo/NekoBoxForAndroid" target="_blank" rel="noopener">NekoBox</a>, <a href="https://github.com/KaringX/karing" target="_blank" rel="noopener">Karing</a>, приложения SFA/SFI/SFM или сам <code>sing-box</code> на компьютере или роутере</li>
        <li>Рабочее подключение к прокси (VLESS, Hysteria, Shadowsocks, WireGuard &mdash; любое, у которого в конфиге есть outbound)</li>
        <li>Расширение <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> в Chrome</li>
    </ul>''',
        },
        {
            'h2': 'Шаг 1. Сгенерируйте rule-set в NetRoute',
            'html': '''    <ol>
        <li>Откройте нужный сайт в Chrome и обновите страницу, чтобы сниффер поймал фоновые запросы</li>
        <li>Запустите <strong>NetRoute</strong></li>
        <li>В списке форматов выберите <strong>sing-box / Hiddify / NekoBox</strong> в группе «Прокси-клиенты»</li>
        <li>Поля «Шлюз» и «Устройство» для этого формата не нужны</li>
        <li>Нажмите <strong>Анализировать</strong></li>
        <li>На вкладке <strong>Домены</strong> снимите галочки с лишнего &mdash; счётчики, рекламные сети, чужие CDN; правила пересчитаются сразу</li>
        <li>Скачайте файл: он называется по сайту, например <code>github_com_rules.json</code></li>
    </ol>
    <div class="callout">
        <strong>Сети нужны не всегда.</strong> Клиент сопоставляет домен ещё до резолва, поэтому для обычных сайтов хватает правила <code>domain_suffix</code>. Сети пригодятся, когда приложение ходит на серверы по IP, минуя DNS &mdash; так делают мессенджеры и игры. Если хотите только домены, выключите IPv4 и IPv6 в параметрах скана &mdash; правило <code>ip_cidr</code> исчезнет.
    </div>''',
        },
        {
            'h2': 'Шаг 2. Подключите файл в sing-box',
            'html': '''    <p>Локальный файл рядом с конфигом:</p>
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
      { "rule_set": "netroute", "outbound": "proxy" }
    ],
    "final": "direct"
  }
}</code></pre>
    <p>Файл по ссылке &mdash; удобно для телефонов и для обновления без правки конфига. Положите <code>.json</code> в репозиторий на GitHub, приватный gist или на свой сервер и укажите прямую ссылку на сырой файл:</p>
    <pre><code>{
  "type": "remote",
  "tag": "netroute",
  "format": "source",
  "url": "https://raw.githubusercontent.com/you/rules/main/github_com_rules.json",
  "download_detour": "proxy",
  "update_interval": "24h"
}</code></pre>
    <p><code>outbound</code> должен совпадать с тегом вашего прокси-outbound (часто <code>proxy</code>, <code>select</code> или имя сервера). <code>download_detour</code> скачивает сам список через прокси &mdash; полезно, если GitHub у вас недоступен напрямую.</p>
    <div class="callout">
        <strong>Hiddify, NekoBox, Karing.</strong> Графические клиенты принимают либо ссылку на rule-set в настройках маршрутизации, либо полный JSON-конфиг sing-box с блоком <code>route</code> выше. Название пункта меняется от версии к версии &mdash; ищите «Rule set», «Routing» или «Пользовательские правила». Если клиент даёт только поле для URL, опубликуйте файл по ссылке, как во втором примере.
    </div>''',
        },
        {
            'h2': 'Шаг 3. Проверьте',
            'html': '''    <p>Синтаксис конфига вместе с rule-set:</p>
    <pre><code>sing-box check -c config.json</code></pre>
    <p>Запустите клиент и откройте сайт. При <code>"log": {"level": "info"}</code> в журнале sing-box видно, какое правило сработало:</p>
    <pre><code>INFO [1234567890] inbound/tun[tun-in]: inbound connection to github.com:443
INFO [1234567890] router: match[0] rule_set=netroute =&gt; proxy</code></pre>
    <p>Если сайт должен открываться через прокси, а в логе <code>=&gt; direct</code> &mdash; правило не совпало: проверьте, что домен есть в <code>domain_suffix</code> и что правило стоит выше правил с <code>final</code> или <code>geosite</code>-исключениями.</p>''',
        },
        {
            'h2': 'Скомпилированный rule-set (.srs)',
            'html': '''    <p>Для больших списков sing-box читает бинарный формат быстрее. Скомпилируйте файл NetRoute один раз:</p>
    <pre><code>sing-box rule-set compile github_com_rules.json
# → github_com_rules.srs</code></pre>
    <p>В конфиге укажите <code>"format": "binary"</code> и путь к <code>.srs</code>. Для десятка сайтов это не нужно &mdash; исходный JSON читается мгновенно.</p>''',
        },
        {
            'h2': 'Частые проблемы',
            'html': '''    <h3>decode rule-set: unsupported version</h3>
    <p>Клиент на sing-box старше 1.8 не знает формата rule-set. Обновите клиент: NetRoute уже пишет минимальную <code>version: 1</code>, ниже опускаться некуда.</p>

    <h3>Правило не срабатывает на поддомене</h3>
    <p><code>domain_suffix</code> покрывает поддомены, но только того домена, который в списке. Если сайт тянет данные с другого домена &mdash; откройте вкладку <strong>Домены</strong> в NetRoute: он там есть, если страница к нему обращалась. Пройдитесь по сайту перед сканом &mdash; войдите в аккаунт, откройте видео, &mdash; тогда сниффер увидит и ленивые запросы.</p>

    <h3>Трафик по IP идёт мимо прокси</h3>
    <p>Правило <code>ip_cidr</code> сравнивает адрес назначения уже после резолва. Если в клиенте включён <code>sniff</code> и домен определился &mdash; сработает правило по домену; если нет &mdash; адрес должен попасть в одну из сетей. Для сервисов с меняющимися IP включите в NetRoute <strong>Оптимизация маршрутов &rarr; BGP Prefix</strong>: вместо отдельных адресов в <code>ip_cidr</code> попадут анонсируемые префиксы.</p>

    <h3>Один rule-set на несколько сайтов</h3>
    <p>Используйте массовое сканирование: вставьте список URL или доменов &mdash; NetRoute соберёт один rule-set на всех, файл будет называться <code>bulk_N_rules.json</code>.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS и утечки',
        'html': '''    <p>В отличие от маршрутов на роутере, правило по домену срабатывает <em>до</em> резолва: sing-box видит имя из SNI или HTTP-запроса и отправляет соединение в outbound, не спрашивая системный DNS. Но сам DNS-запрос браузера всё равно уходит &mdash; и если он идёт к провайдеру, провайдер видит имена сайтов.</p>
    <ul>
        <li>Направьте DNS в прокси: в секции <code>dns.servers</code> задайте сервер с <code>"detour": "proxy"</code> для доменов из правила, например через <code>dns.rules</code> с тем же <code>rule_set: netroute</code>.</li>
        <li>Включите <code>"sniff": true</code> на inbound &mdash; тогда соединения по IP тоже получат домен и попадут под <code>domain_suffix</code>.</li>
        <li>В браузере отключите собственный DNS-over-HTTPS или укажите в нём резолвер, идущий через туннель, иначе Chrome резолвит имена в обход клиента.</li>
    </ul>
    <p>Проверка: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> при включённом клиенте должен показывать резолвер прокси, а не провайдера.</p>''',
    },
    'official_docs': [
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/', 'label': 'sing-box: Rule Set (en)'},
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/source-format/', 'label': 'sing-box: Source Format &mdash; version и headless rules (en)'},
        {'url': 'https://sing-box.sagernet.org/configuration/route/rule/', 'label': 'sing-box: Route Rule (en)'},
        {'url': 'https://sing-box.sagernet.org/configuration/dns/', 'label': 'sing-box: DNS (en)'},
    ],
    'example_file': 'singbox-rules.json',
    'example_desc': 'rule-set в исходном формате с правилами <code>domain_suffix</code> и <code>ip_cidr</code>',
    'card': {
        'badge': 'proxy',
        'badge_label': 'Прокси-клиент',
        'title': 'sing-box / Hiddify',
        'text': 'Rule-set с доменами и сетями сайта: локальный файл или ссылка, компиляция в .srs, проверка в логах.',
    },
    'related_desc': 'rule-set для Hiddify, NekoBox и sing-box',
    'date_published': '2026-10-16',
}

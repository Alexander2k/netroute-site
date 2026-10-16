# Инструкция: sing-box rule-set (sing-box, Hiddify и другие клиенты на ядре sing-box). Русский.
#
# Источники фактов (проверены 2026-10-16):
#   NetRoute — popup.html, options.html, _locales/ru/messages.json, modules/RuleFormats.js
#   sing-box — sing-box.sagernet.org: configuration/rule-set/, rule-set/source-format/,
#              rule-set/headless-rule/, route/, route/rule/, route/rule_action/, route/sniff/,
#              dns/rule/, dns/server/https/, shared/dial/, shared/listen/, configuration/ (команды)
#   Hiddify — README github.com/hiddify/hiddify-app; NekoBox — README github.com/MatsuriDayo/NekoBoxForAndroid
PAGE = {
    'title': 'Rule-set sing-box из любого сайта: домены и сети для Hiddify и sing-box — инструкция | NetRoute',
    'description': 'Как получить rule-set sing-box с доменами и сетями сайта в NetRoute и подключить его в конфиге sing-box или Hiddify: route.rule_set, правило с action route, компиляция в .srs, DNS.',
    'keywords': 'sing-box rule-set, sing-box rule_set source, sing-box domain_suffix ip_cidr, hiddify sing-box конфиг, sing-box srs compile, split tunneling sing-box, маршрутизация по доменам sing-box, sing-box правила для сайта',
    'og_title': 'Rule-set sing-box из любого сайта: домены и сети для Hiddify и sing-box',
    'og_description': 'NetRoute собирает домены и сети сайта в rule-set sing-box. Подключение в route.rule_set, правило с action route, компиляция в .srs.',
    'breadcrumb': 'sing-box',
    'h1': 'Rule-set sing-box из любого сайта: домены и сети для Hiddify и sing-box',
    'lead': 'sing-box и клиенты на его ядре &mdash; официальные приложения sing-box, Hiddify, NekoBox &mdash; решают, что пускать через прокси, по <strong>правилам</strong>: спискам доменов и сетей, которые с версии 1.8.0 оформляются как rule-set. NetRoute собирает такой rule-set прямо со страницы сайта: открыли сайт, нажали «Анализировать сайт», скачали <code>.json</code>.',
    'howto': {
        'name': 'Как подключить rule-set NetRoute в sing-box',
        'description': 'Сгенерируйте rule-set в формате sing-box в расширении NetRoute, опишите файл в route.rule_set и добавьте правило route.rules с action route и outbound вашего прокси.',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Сгенерируйте rule-set в NetRoute', 'text': 'Откройте нужный сайт в Chrome, запустите NetRoute, в списке «Целевая ОС» выберите «sing-box / Hiddify / NekoBox», нажмите «Анализировать сайт» и скачайте файл <сайт>_rules.json.'},
            {'name': 'Опишите файл в конфиге sing-box', 'text': 'В route.rule_set добавьте запись type local с format source и path к файлу (или type remote с url, если файл опубликован), а в route.rules — правило с rule_set, action route и outbound вашего прокси.'},
            {'name': 'Проверьте конфиг', 'text': 'Выполните sing-box check -c config.json, запустите sing-box и откройте сайт.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'Что внутри файла',
            'html': '''    <p>Rule-set в исходном формате (<code>source</code>) &mdash; это JSON с полями <code>version</code> и <code>rules</code>. NetRoute пишет домены и сети <strong>двумя отдельными правилами</strong>: по документации sing-box условия внутри одного правила объединяются логическим «И», и одно правило с доменами и сетями срабатывало бы только при совпадении и того, и другого.</p>
    <pre><code>{
  "version": 1,
  "rules": [
    { "domain_suffix": ["github.com", "githubusercontent.com"] },
    { "ip_cidr": ["140.82.112.0/20", "185.199.108.0/22", "2606:50c0::/32"] }
  ]
}</code></pre>
    <ul>
        <li><code>domain_suffix</code> &mdash; совпадение по суффиксу домена: сам домен и все его поддомены. NetRoute сворачивает список: если на странице найдены <code>api.github.com</code> и <code>github.com</code>, остаётся <code>github.com</code>; префикс <code>www.</code> отбрасывается. В список попадают все домены скана, в том числе те, что не удалось разрешить в IP.</li>
        <li><code>ip_cidr</code> &mdash; совпадение по сети. Это те же агрегированные сети, которые NetRoute выдал бы маршрутами для роутера, IPv4 и IPv6 вместе; правило есть, если хотя бы один домен разрешился в адрес.</li>
        <li><code>version: 1</code> &mdash; первая версия формата, появившаяся в sing-box 1.8.0.</li>
    </ul>''',
        },
        {
            'h2': 'Что понадобится',
            'html': '''    <ul>
        <li>sing-box 1.8.0 или новее: сам <code>sing-box</code> на компьютере, сервере или роутере либо официальные приложения <em>sing-box for Android</em>, <em>sing-box for Apple platforms</em>, <em>sing-box for Desktop</em></li>
        <li>или <a href="https://github.com/hiddify/hiddify-app" target="_blank" rel="noopener">Hiddify</a> &mdash; клиент на ядре sing-box, который по README принимает конфигурации в формате sing-box (Android, iOS, Windows, macOS, Linux)</li>
        <li>Рабочий outbound прокси в конфиге &mdash; протокол любой</li>
        <li>Расширение <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> в Chrome</li>
    </ul>
    <div class="callout">
        <strong>NekoBox для Android</strong> тоже работает на ядре sing-box, но, по его README, из подписок берёт только узлы, а правила маршрутизации игнорирует. Rule-set туда можно принести только внутри полного конфига sing-box.
    </div>''',
        },
        {
            'h2': 'Шаг 1. Сгенерируйте rule-set в NetRoute',
            'html': '''    <ol>
        <li>Откройте нужный сайт в Chrome и обновите страницу, чтобы сниффер расширения увидел фоновые запросы</li>
        <li>Запустите <strong>NetRoute</strong></li>
        <li>В списке <strong>Целевая ОС</strong> выберите <strong>sing-box / Hiddify / NekoBox</strong> &mdash; группа «Прокси-клиенты»</li>
        <li>Поля <strong>IP шлюза</strong> и <strong>Интерфейс</strong> на этот формат не влияют</li>
        <li>Нажмите <strong>Анализировать сайт</strong></li>
        <li>На вкладке <strong>Домены</strong> снимите галочки с лишнего &mdash; счётчики, рекламные сети, чужие CDN; правила пересчитаются сразу</li>
        <li>Нажмите <strong>Скачать</strong>: файл называется по сайту, например <code>github_com_rules.json</code></li>
    </ol>
    <div class="callout">
        <strong>Про сети.</strong> Правило <code>ip_cidr</code> попадает в файл всегда, когда есть разрешённые адреса, и домену оно не мешает. Нужен список из одних доменов &mdash; удалите второе правило из файла. Чтобы сетей было меньше, выберите в <strong>Режим роутов</strong> вариант <strong>IPv4 Only</strong>: правило останется без IPv6-префиксов.
    </div>''',
        },
        {
            'h2': 'Шаг 2. Опишите файл в конфиге sing-box',
            'html': '''    <p>Локальный файл рядом с конфигом. <code>format</code> можно не указывать, если путь заканчивается на <code>.json</code> или <code>.srs</code>; с версии 1.10.0 sing-box перечитывает файл сам при изменении.</p>
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
        <li><code>outbound</code> &mdash; тег вашего прокси-outbound. Запись <code>"action": "route"</code> обязательна начиная с sing-box 1.11.0: старое поле <code>outbound</code> прямо в правиле там объявлено устаревшим.</li>
        <li><code>final</code> &mdash; outbound по умолчанию для всего, что не совпало ни с одним правилом; <code>direct</code> даёт классический split tunneling.</li>
    </ul>
    <p>Файл по ссылке. Положите <code>.json</code> в репозиторий на GitHub или на свой сервер и укажите прямую ссылку на сырой файл; по умолчанию sing-box обновляет его раз в сутки (<code>update_interval</code> = <code>1d</code>):</p>
    <pre><code>{
  "type": "remote",
  "tag": "netroute",
  "format": "source",
  "url": "https://raw.githubusercontent.com/you/rules/main/github_com_rules.json",
  "update_interval": "1d"
}</code></pre>
    <p>Если ссылка должна скачиваться через прокси: до sing-box 1.13 для этого служило поле <code>download_detour</code> с тегом outbound, с 1.14.0 оно объявлено устаревшим в пользу <code>http_client</code>, а в 1.16.0 удалено.</p>
    <div class="callout">
        <strong>Hiddify.</strong> Приложение принимает конфигурации в формате sing-box &mdash; добавьте в такой конфиг блок <code>route</code> выше вместе с вашим outbound и импортируйте его как профиль. Как именно импортировать профиль в вашей версии Hiddify, смотрите в документации приложения.
    </div>''',
        },
        {
            'h2': 'Шаг 3. Проверьте',
            'html': '''    <p>Синтаксис конфига вместе с rule-set:</p>
    <pre><code>sing-box check -c config.json</code></pre>
    <p>Затем запустите sing-box и откройте сайт. Если он открывается через прокси, а остальные сайты идут напрямую &mdash; правило работает. Если нет, пройдите по списку частых проблем ниже.</p>''',
        },
        {
            'h2': 'Скомпилированный rule-set (.srs)',
            'html': '''    <p>Для больших списков sing-box предлагает бинарный формат. Скомпилируйте файл NetRoute командой из документации:</p>
    <pre><code>sing-box rule-set compile github_com_rules.json
# → github_com_rules.srs</code></pre>
    <p>В конфиге укажите <code>"format": "binary"</code> и путь к <code>.srs</code>. Для десятка сайтов это не обязательно.</p>''',
        },
        {
            'h2': 'Частые проблемы',
            'html': '''    <h3>sing-box не принимает файл</h3>
    <p>Rule-set появился в sing-box 1.8.0; более старые версии и клиенты на них формат не знают. NetRoute пишет минимальную <code>version: 1</code> &mdash; все последующие версии её читают.</p>

    <h3>Правило не срабатывает на поддомене</h3>
    <p><code>domain_suffix</code> покрывает поддомены только тех доменов, что есть в списке. Если сайт тянет данные с другого домена, его должно быть видно на вкладке <strong>Домены</strong> в NetRoute. Пройдитесь по сайту перед сканом &mdash; войдите в аккаунт, откройте видео &mdash; тогда сниффер расширения увидит и отложенные запросы.</p>

    <h3>Соединения по IP идут мимо прокси</h3>
    <p>Правило по домену требует, чтобы sing-box знал имя назначения. Для этого служит сниффинг: он достаёт имя из поля Host в HTTP и из Server Name в TLS и QUIC. С sing-box 1.11.0 сниффинг включается правилом с <code>"action": "sniff"</code> в <code>route.rules</code> (старое поле <code>sniff</code> у inbound объявлено устаревшим и удалено в 1.13.0). Соединения без имени сравниваются по правилу <code>ip_cidr</code> &mdash; для сервисов с меняющимися адресами включите в настройках NetRoute <strong>Оптимизация маршрутов &rarr; BGP Prefix</strong>: в сети попадут анонсируемые префиксы, а не отдельные адреса.</p>

    <h3>Один rule-set на несколько сайтов</h3>
    <p>Нажмите <strong>URL list</strong> рядом с кнопкой анализа и вставьте список сайтов &mdash; NetRoute соберёт один rule-set на всех, файл будет называться <code>bulk_N_rules.json</code>.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS и утечки',
        'html': '''    <p>Правило по домену не меняет того, как браузер разрешает имена: DNS-запрос к <code>github.com</code> всё равно уходит на тот резолвер, который настроен в системе или в самом браузере, и если это резолвер провайдера &mdash; провайдер видит имена сайтов.</p>
    <ul>
        <li>В sing-box правила DNS умеют ссылаться на тот же rule-set: правило <code>dns.rules</code> с <code>"rule_set": "netroute"</code>, <code>"action": "route"</code> и <code>server</code> отправит запросы к этим доменам на выбранный DNS-сервер. Чтобы сам сервер ходил через прокси, задайте у него <code>detour</code> с тегом outbound &mdash; это поле из общих параметров подключения (Dial Fields); серверы в новом формате (<code>"type": "https"</code> и другие) появились в sing-box 1.12.0.</li>
        <li>В Chrome отключите «Использовать безопасный DNS» или укажите в нём резолвер, которому доверяете: собственный DNS-over-HTTPS браузера работает в обход системного резолвера &mdash; подробнее в <a href="https://github.com/Alexander2k/netroute-site" target="_blank" rel="noopener">разделе Troubleshooting</a> проекта.</li>
    </ul>
    <p>Проверка: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> при включённом клиенте должен показывать резолвер прокси, а не провайдера.</p>''',
    },
    'official_docs': [
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/', 'label': 'sing-box: Rule Set &mdash; поля local и remote (en)'},
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/source-format/', 'label': 'sing-box: Source Format &mdash; version, команда compile (en)'},
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/headless-rule/', 'label': 'sing-box: Headless Rule &mdash; domain_suffix, ip_cidr (en)'},
        {'url': 'https://sing-box.sagernet.org/configuration/route/rule_action/', 'label': 'sing-box: Rule Action &mdash; route, sniff (en)'},
        {'url': 'https://sing-box.sagernet.org/configuration/dns/rule/', 'label': 'sing-box: DNS Rule (en)'},
        {'url': 'https://github.com/hiddify/hiddify-app', 'label': 'Hiddify &mdash; README: поддерживаемые форматы конфигураций (en)'},
    ],
    'example_file': 'singbox-rules.json',
    'example_desc': 'rule-set в исходном формате с правилами <code>domain_suffix</code> и <code>ip_cidr</code>',
    'card': {
        'badge': 'proxy',
        'badge_label': 'Прокси-клиент',
        'title': 'sing-box / Hiddify',
        'text': 'Rule-set с доменами и сетями сайта: локальный файл или ссылка в route.rule_set, компиляция в .srs.',
    },
    'related_desc': 'rule-set для sing-box и Hiddify',
    'date_published': '2026-10-16',
}

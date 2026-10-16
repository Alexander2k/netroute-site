# Инструкция: профиль маршрутизации Happ. Русский.
#
# Источники фактов (проверены 2026-10-17):
#   NetRoute — popup.html, _locales/ru/messages.json, modules/RuleFormats.js
#   Happ — happ.su/main (описание, платформы), happ.su/main/ru/dev-docs/routing.md (ссылки add/onadd,
#          base64, смысл полей, LastUpdated, Reconnect), happ.su/main/ru/faq/adding-configuration-subscription.md
#          (кнопка «+», буфер обмена, QR, диплинк), happ.su/main/dev-docs/examples-of-links-and-parameters.md
#   Xray — xtls.github.io/config/routing.html (форма domain: в списках доменов)
PAGE = {
    'title': 'Профиль маршрутизации Happ из любого сайта: домены и сети через прокси — инструкция | NetRoute',
    'description': 'Как получить в NetRoute профиль маршрутизации Happ с доменами и сетями сайта и добавить его ссылкой happ://routing/onadd: кодирование в base64, импорт из буфера обмена или QR-кода, проверка.',
    'keywords': 'happ маршрутизация, happ routing профиль, happ routing onadd, happ json профиль маршрутизации, happ proxysites, happ split tunneling, happ правила для сайта, happ xray маршрутизация',
    'og_title': 'Профиль маршрутизации Happ из любого сайта',
    'og_description': 'NetRoute собирает домены и сети сайта в профиль маршрутизации Happ. Кодируете в base64, добавляете ссылкой happ://routing/onadd — только эти сайты идут через прокси.',
    'breadcrumb': 'Happ',
    'h1': 'Профиль маршрутизации Happ из любого сайта',
    'lead': 'Happ &mdash; кроссплатформенный клиент на ядре Xray для Windows, macOS, Linux, iOS, Android и ТВ-платформ. Что пускать через прокси, он решает по <strong>профилю маршрутизации</strong>: спискам доменов и адресов. NetRoute собирает такой профиль со страницы сайта в формате JSON, а в приложение он попадает ссылкой <code>happ://routing/onadd/…</code>.',
    'howto': {
        'name': 'Как добавить в Happ профиль маршрутизации из NetRoute',
        'description': 'Сгенерируйте профиль Happ в расширении NetRoute, закодируйте JSON в base64, соберите ссылку happ://routing/onadd/{base64} и добавьте её в Happ из буфера обмена, по QR-коду или диплинком.',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Сгенерируйте профиль в NetRoute', 'text': 'Откройте нужный сайт в Chrome, запустите NetRoute, в списке «Целевая ОС» выберите «Happ», нажмите «Анализировать сайт» и скачайте файл <сайт>_rules.json.'},
            {'name': 'Соберите ссылку', 'text': 'Закодируйте содержимое файла в base64 и допишите спереди happ://routing/onadd/ — получится ссылка, которая добавляет и сразу активирует профиль.'},
            {'name': 'Добавьте ссылку в Happ', 'text': 'Скопируйте ссылку в буфер обмена, откройте Happ и добавьте её кнопкой «+» (из буфера обмена, по QR-коду или диплинком). После изменений профиля переподключитесь.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'Что внутри файла',
            'html': '''    <p>Профиль маршрутизации Happ &mdash; это JSON с настройками DNS, geo-файлов и шестью списками: что через прокси, что напрямую, что блокировать &mdash; отдельно для доменов и для адресов. NetRoute заполняет списки прокси и оставляет остальное в значениях, которые Happ принимает по умолчанию:</p>
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
    <p>Что означают поля &mdash; по документации Happ:</p>
    <ul>
        <li><code>GlobalProxy</code> &mdash; при <code>true</code> весь трафик по умолчанию идёт через прокси, при <code>false</code> &mdash; напрямую; это же значение определяет выход для всего, что не попало ни в одно правило. NetRoute ставит <code>false</code>: через прокси идут только перечисленные сайты.</li>
        <li><code>ProxySites</code> / <code>ProxyIp</code> &mdash; домены и адреса, которые идут через прокси. Домены записаны в форме <code>domain:имя</code> &mdash; по документации Xray это сам домен и все его поддомены; список свёрнут, <code>www.</code> отброшен. Адреса &mdash; те же агрегированные сети, что NetRoute выдаёт маршрутами для роутера, IPv4 и IPv6.</li>
        <li><code>DirectSites</code> / <code>DirectIp</code> и <code>BlockSites</code> / <code>BlockIp</code> &mdash; напрямую и блокировать; NetRoute оставляет напрямую только частные адреса (<code>geoip:private</code>).</li>
        <li><code>RouteOrder</code> &mdash; порядок проверки правил: сначала блокировка, затем прокси, затем прямое подключение.</li>
        <li><code>DomainStrategy</code> &mdash; стратегия Xray: <code>IPIfNonMatch</code> разрешает домен в адрес только если по имени правило не нашлось.</li>
        <li><code>RemoteDNS*</code> / <code>DomesticDNS*</code> &mdash; DNS для сайтов через прокси и для остальных; <code>DoH</code> &mdash; DNS-over-HTTPS. Значения можно поменять в файле до импорта.</li>
        <li><code>Geoipurl</code> / <code>Geositeurl</code> &mdash; ссылки на geoip.dat и geosite.dat; пустые значения Happ заполняет из профиля по умолчанию.</li>
        <li><code>LastUpdated</code> &mdash; дата в формате Unix; профиль обновляется, если она больше предыдущей. NetRoute ставит время генерации.</li>
        <li><code>DnsHosts</code> &mdash; ручные соответствия «домен: IP», аналог файла hosts; у NetRoute пуст.</li>
    </ul>''',
        },
        {
            'h2': 'Что понадобится',
            'html': '''    <ul>
        <li>Приложение <a href="https://www.happ.su/main" target="_blank" rel="noopener">Happ</a> с добавленным сервером (Windows, macOS, Linux, iOS, Android, Android TV или Apple TV)</li>
        <li>Расширение <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> в Chrome</li>
        <li>Способ закодировать файл в base64 &mdash; команда есть в каждой системе, примеры ниже</li>
    </ul>''',
        },
        {
            'h2': 'Шаг 1. Сгенерируйте профиль в NetRoute',
            'html': '''    <ol>
        <li>Откройте нужный сайт в Chrome и обновите страницу, чтобы сниффер расширения увидел фоновые запросы</li>
        <li>Запустите <strong>NetRoute</strong></li>
        <li>В списке <strong>Целевая ОС</strong> выберите <strong>Happ</strong> &mdash; группа «Прокси-клиенты»</li>
        <li>Поля <strong>IP шлюза</strong> и <strong>Интерфейс</strong> на этот формат не влияют</li>
        <li>Нажмите <strong>Анализировать сайт</strong></li>
        <li>На вкладке <strong>Домены</strong> снимите галочки с лишнего &mdash; счётчики, рекламные сети, чужие CDN; профиль пересчитается сразу</li>
        <li>Нажмите <strong>Скачать</strong>: файл называется по сайту, например <code>github_com_rules.json</code></li>
    </ol>''',
        },
        {
            'h2': 'Шаг 2. Соберите ссылку happ://routing/…',
            'html': '''    <p>По документации Happ профиль добавляется ссылкой, где <code>{base64}</code> &mdash; JSON-профиль, преобразованный в текст base64:</p>
    <ul>
        <li><code>happ://routing/add/{base64}</code> &mdash; добавляет профиль в список;</li>
        <li><code>happ://routing/onadd/{base64}</code> &mdash; добавляет и сразу активирует, даже если активен другой профиль.</li>
    </ul>
    <p>Закодируйте скачанный файл:</p>
    <pre><code># Windows, PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("github_com_rules.json"))

# macOS
base64 -i github_com_rules.json

# Linux
base64 -w0 github_com_rules.json</code></pre>
    <p>Допишите к результату префикс <code>happ://routing/onadd/</code> &mdash; одной строкой, без пробелов и переносов. Ссылка получится длинной, это нормально.</p>
    <div class="callout">
        Кодируйте файл локально &mdash; онлайн-кодировщики увидят список сайтов. Встроенная кнопка «Скопировать как ссылку Happ» в NetRoute запланирована.
    </div>''',
        },
        {
            'h2': 'Шаг 3. Добавьте ссылку в Happ',
            'html': '''    <p>По документации Happ ссылки принимаются тремя способами &mdash; копированием из буфера обмена, сканированием QR-кода и диплинком:</p>
    <ol>
        <li>Скопируйте собранную ссылку в буфер обмена</li>
        <li>Откройте Happ и нажмите <strong>+</strong> в правом верхнем углу главного экрана</li>
        <li>Добавьте ссылку из буфера обмена. На телефон ссылку удобно передать QR-кодом или открыть как диплинк &mdash; система предложит открыть её в Happ</li>
        <li>Если использовали <code>onadd</code>, профиль уже активен; с <code>add</code> выберите его в списке профилей маршрутизации</li>
        <li>Переподключитесь: по документации изменения профиля применяются после <strong>Reconnect</strong></li>
    </ol>''',
        },
        {
            'h2': 'Шаг 4. Проверьте',
            'html': '''    <p>Откройте сайт, для которого собирали профиль, &mdash; он должен открываться через прокси, а остальные сайты идти напрямую (<code>GlobalProxy: false</code>). Если наоборот &mdash; проверьте, какой профиль маршрутизации активен в Happ, и что вы переподключились после импорта.</p>''',
        },
        {
            'h2': 'Частые проблемы',
            'html': '''    <h3>Ссылка не принимается</h3>
    <p>Проверьте, что base64 получился одной строкой без переносов (в Linux для этого нужен ключ <code>-w0</code>) и что перед ним стоит ровно <code>happ://routing/onadd/</code> или <code>happ://routing/add/</code>.</p>

    <h3>Профиль добавился, но ничего не изменилось</h3>
    <p>После смены профиля Happ применяет его при переподключении. Со ссылкой <code>add</code> профиль нужно ещё выбрать активным.</p>

    <h3>Сайт тянет данные с других доменов</h3>
    <p>Их должно быть видно на вкладке <strong>Домены</strong> в NetRoute &mdash; расширение собирает домены со страницы и из её фоновых запросов. Пройдитесь по сайту перед сканом (войдите в аккаунт, откройте видео), тогда в профиль попадут и отложенные запросы. Несколько сайтов в один профиль &mdash; кнопка <strong>URL list</strong> рядом с кнопкой анализа: файл будет называться <code>bulk_N_rules.json</code>.</p>

    <h3>Профиль в подписке</h3>
    <p>По документации Happ в JSON-подписке может быть строго 0 или 1 профиль маршрутизации, а ссылку на профиль можно передавать в заголовке <code>routing</code> или прямо в теле подписки &mdash; удобно, если вы раздаёте настройки нескольким устройствам.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS и утечки',
        'html': '''    <p>В профиле заданы два DNS: <code>RemoteDNS</code> для сайтов, идущих через прокси, и <code>DomesticDNS</code> для остальных &mdash; оба по DNS-over-HTTPS (Cloudflare и Яндекс в файле NetRoute). Поменяйте их в JSON до кодирования, если нужны другие резолверы. Запросы браузера при этом всё равно идут туда, куда настроен его собственный DNS: в Chrome отключите «Использовать безопасный DNS» или укажите в нём резолвер, которому доверяете, иначе Chrome разрешает имена в обход клиента.</p>
    <p>Проверка: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> при включённом Happ должен показывать резолвер из профиля, а не провайдера.</p>''',
    },
    'official_docs': [
        {'url': 'https://www.happ.su/main/ru/dev-docs/routing.md', 'label': 'Happ: Геонастройки / Routing &mdash; ссылки add и onadd, поля профиля (ru)'},
        {'url': 'https://www.happ.su/main/ru/faq/adding-configuration-subscription.md', 'label': 'Happ: Добавление конфигурации &mdash; буфер обмена, QR-код, диплинк (ru)'},
        {'url': 'https://www.happ.su/main/dev-docs/examples-of-links-and-parameters.md', 'label': 'Happ: Examples of links and parameters (en)'},
        {'url': 'https://xtls.github.io/config/routing.html', 'label': 'Xray: Routing &mdash; форма domain: и стратегии доменов (zh)'},
    ],
    'shot_format': 'happ',
    'shot_caption': 'Попап NetRoute с форматом «Happ»: на вкладке «Маршруты» &mdash; профиль маршрутизации, который остаётся закодировать в ссылку. Данные скана &mdash; страница github.com.',
    'example_file': 'happ-routing.json',
    'example_desc': 'профиль маршрутизации Happ со списками <code>ProxySites</code> и <code>ProxyIp</code>',
    'card': {
        'badge': 'proxy',
        'badge_label': 'Прокси-клиент',
        'title': 'Happ',
        'text': 'Профиль маршрутизации с доменами и сетями сайта: base64 → ссылка happ://routing/onadd → импорт из буфера обмена или QR-кода.',
    },
    'related_desc': 'профиль маршрутизации ссылкой happ://routing',
    'date_published': '2026-10-17',
}

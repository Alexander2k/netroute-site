# Инструкция: правила маршрутизации Xray — Xray-core, 3X-UI, v2rayN, Streisand. Русский.
#
# Источники фактов (проверены 2026-10-17):
#   NetRoute — popup.html, _locales/ru/messages.json, modules/RuleFormats.js
#   Xray — xtls.github.io/config/routing.html (domainStrategy, порядок правил, формы domain и ip, outboundTag)
#   v2rayN — README github.com/2dust/v2rayN (платформы, ядра), wiki Description-of-custom-routing-rules,
#            строки интерфейса ServiceLib/Resx/ResUI.resx (Routing, Routing Setting, Import Rules From …,
#            Domain, IP or IP CIDR, запрос append/replace), формат github.com/2dust/v2rayCustomRoutingList
#   3X-UI — README github.com/MHSanaei/3x-ui, docs/content/docs/ru/operations/outbounds-routing.mdx
#   Streisand — страница в App Store (id6450534064)
PAGE = {
    'title': 'Правила маршрутизации Xray из любого сайта: для Xray-core, 3X-UI и v2rayN — инструкция | NetRoute',
    'description': 'Как получить в NetRoute правила routing.rules Xray с доменами и сетями сайта и применить их в конфиге Xray-core, в настройках Xray панели 3X-UI или импортом правил в v2rayN.',
    'keywords': 'xray routing rules, xray правила маршрутизации, xray domain: outboundTag, xray split tunneling, 3x-ui маршрутизация, 3x-ui routing rules, v2rayn импорт правил, v2rayn routing setting, v2rayn правила маршрутизации, xray json routing',
    'og_title': 'Правила маршрутизации Xray из любого сайта',
    'og_description': 'NetRoute собирает домены и сети сайта в правила routing.rules Xray — для конфига Xray-core, панели 3X-UI и импорта в v2rayN.',
    'breadcrumb': 'Xray',
    'h1': 'Правила маршрутизации Xray из любого сайта: Xray-core, 3X-UI, v2rayN',
    'lead': 'Xray направляет соединения по правилам <code>routing.rules</code>: списки доменов и адресов и тег исходящего подключения. NetRoute собирает такие правила со страницы сайта в двух вариантах: фрагмент конфига Xray-core &mdash; он же подходит для панели 3X-UI, где конфиг Xray редактируется как JSON, &mdash; и файл для импорта правил в v2rayN.',
    'howto': {
        'name': 'Как применить правила маршрутизации Xray из NetRoute',
        'description': 'Сгенерируйте правила в формате Xray или v2rayN в расширении NetRoute и вставьте их в routing.rules конфига Xray-core, в настройки Xray панели 3X-UI или импортируйте в v2rayN из буфера обмена.',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Сгенерируйте правила в NetRoute', 'text': 'Откройте нужный сайт в Chrome, запустите NetRoute, в списке «Целевая ОС» выберите «Xray / 3X-UI / Streisand» или «v2rayN (rules import)», в поле «Интерфейс» укажите тег исходящего подключения (по умолчанию proxy), нажмите «Анализировать сайт» и скачайте файл.'},
            {'name': 'Вставьте правила', 'text': 'Xray-core и 3X-UI: добавьте объекты из rules в начало routing.rules вашего конфига. v2rayN: Routing → Routing Setting → Import Rules From Clipboard, в вопросе о добавлении ответьте «да», чтобы дополнить правила.'},
            {'name': 'Проверьте', 'text': 'Перезапустите Xray (панель 3X-UI перезагружает его сама) и откройте сайт — он должен идти через исходящее подключение с указанным тегом.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'Что внутри файла',
            'html': '''    <p><strong>Формат «Xray / 3X-UI / Streisand»</strong> &mdash; фрагмент конфига Xray-core с секцией <code>routing</code>. Домены и сети записаны двумя правилами, у каждого свой список и общий <code>outboundTag</code>:</p>
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
        <li><code>domain:имя</code> &mdash; по документации Xray это сам домен и его поддомены. Список свёрнут: если найдены <code>api.github.com</code> и <code>github.com</code>, остаётся <code>github.com</code>; <code>www.</code> отброшен. В него входят все домены скана, в том числе не разрешённые в IP.</li>
        <li><code>ip</code> &mdash; адреса в форме CIDR; это те же агрегированные сети, что NetRoute выдаёт маршрутами для роутера, IPv4 и IPv6.</li>
        <li><code>outboundTag</code> &mdash; тег исходящего подключения из поля <strong>Интерфейс</strong> в NetRoute; по умолчанию <code>proxy</code>.</li>
        <li><code>domainStrategy: IPIfNonMatch</code> &mdash; по документации Xray домен разрешается в адрес только если по имени ни одно правило не совпало; по умолчанию у Xray <code>AsIs</code>, без резолва.</li>
    </ul>
    <p><strong>Формат «v2rayN (rules import)»</strong> &mdash; массив правил в том виде, в каком v2rayN импортирует их из буфера обмена или файла (как в репозитории <code>v2rayCustomRoutingList</code> автора v2rayN):</p>
    <pre><code>[
  { "port": "", "outboundTag": "proxy", "domain": ["domain:github.com", "domain:githubusercontent.com"], "enabled": true, "remarks": "NetRoute github.com domains" },
  { "port": "", "outboundTag": "proxy", "ip": ["140.82.112.0/20", "185.199.108.0/22", "2606:50c0::/32"], "enabled": true, "remarks": "NetRoute github.com networks" }
]</code></pre>''',
        },
        {
            'h2': 'Что понадобится',
            'html': '''    <ul>
        <li>Xray-core с настроенным исходящим подключением (outbound) и известным тегом &mdash; на компьютере, сервере или в панели <a href="https://github.com/MHSanaei/3x-ui" target="_blank" rel="noopener">3X-UI</a></li>
        <li>или <a href="https://github.com/2dust/v2rayN" target="_blank" rel="noopener">v2rayN</a> для Windows, Linux или macOS &mdash; клиент с ядрами Xray и sing-box</li>
        <li>Расширение <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> в Chrome</li>
    </ul>''',
        },
        {
            'h2': 'Шаг 1. Сгенерируйте правила в NetRoute',
            'html': '''    <ol>
        <li>Откройте нужный сайт в Chrome и обновите страницу, чтобы сниффер расширения увидел фоновые запросы</li>
        <li>Запустите <strong>NetRoute</strong></li>
        <li>В списке <strong>Целевая ОС</strong>, группа «Прокси-клиенты», выберите <strong>Xray / 3X-UI / Streisand</strong> для конфига Xray-core или <strong>v2rayN (rules import)</strong> для импорта в v2rayN</li>
        <li>В поле <strong>Интерфейс</strong> укажите тег вашего исходящего подключения &mdash; подсказка в поле показывает значение по умолчанию <code>proxy</code>. Поле <strong>IP шлюза</strong> на эти форматы не влияет</li>
        <li>Нажмите <strong>Анализировать сайт</strong></li>
        <li>На вкладке <strong>Домены</strong> снимите галочки с лишнего &mdash; правила пересчитаются сразу</li>
        <li>Нажмите <strong>Скачать</strong>: файл называется по сайту, например <code>github_com_rules.json</code></li>
    </ol>''',
        },
        {
            'h2': 'Шаг 2а. Xray-core: вставьте правила в конфиг',
            'html': '''    <p>Откройте <code>config.json</code> Xray и добавьте оба объекта из <code>rules</code> в массив <code>routing.rules</code> <strong>выше</strong> общих правил. По документации Xray правила проверяются сверху вниз, срабатывает первое совпавшее; соединение, не подошедшее ни под одно правило, уходит в первый outbound конфига. Убедитесь, что <code>outboundTag</code> совпадает с тегом вашего прокси-outbound, а <code>domainStrategy</code> в секции <code>routing</code> задана один раз.</p>
    <p>Перезапустите Xray.</p>''',
        },
        {
            'h2': 'Шаг 2б. 3X-UI: правила в настройках Xray',
            'html': '''    <p>3X-UI &mdash; веб-панель для серверов Xray-core. По её документации правила маршрутизации &mdash; это правила Xray с полями <code>domain</code>, <code>ip</code>, <code>port</code>, <code>network</code>, <code>protocol</code>, <code>inboundTag</code>, <code>sourceIP</code> и целью <code>outboundTag</code> или <code>balancerTag</code>; отдельного редактора на каждое правило нет &mdash; вы редактируете JSON конфига в разделе <strong>Xray Settings</strong>, а панель сама перезагружает Xray.</p>
    <ol>
        <li>Откройте в панели <strong>Xray Settings</strong></li>
        <li>Найдите в JSON массив <code>routing.rules</code> и вставьте в его начало оба объекта из файла NetRoute</li>
        <li>Поставьте в <code>outboundTag</code> тег нужного исходящего подключения &mdash; например, подключения WARP или другого сервера, если хотите пускать эти сайты через него</li>
        <li>Сохраните &mdash; панель перезагрузит Xray</li>
    </ol>
    <p>На сервере правило означает: трафик клиентов к этим доменам и сетям сервер отправит в указанный outbound, остальной &mdash; как настроено дальше по списку правил.</p>''',
        },
        {
            'h2': 'Шаг 2в. v2rayN: импорт правил',
            'html': '''    <p>Для v2rayN выберите в NetRoute формат <strong>v2rayN (rules import)</strong>. Строки интерфейса v2rayN, по которым ориентироваться:</p>
    <ol>
        <li>Откройте скачанный файл и скопируйте его содержимое в буфер обмена</li>
        <li>В v2rayN откройте <strong>Routing</strong> &rarr; <strong>Routing Setting</strong></li>
        <li>Выберите <strong>Import Rules From Clipboard</strong> (есть также <strong>Import Rules From File</strong> и <strong>Import Rules From Subscription URL</strong>)</li>
        <li>На вопрос <em>«Do you want to append rules? Choose yes to append, no to replace.»</em> ответьте <strong>Yes</strong>, чтобы добавить правила к существующим</li>
        <li>Проверьте, что набор правил, в который они попали, отмечен как активный (<strong>Set as active rule</strong>)</li>
    </ol>
    <p>В редакторе правила v2rayN те же списки видны в полях <strong>Domain</strong> и <strong>IP or IP CIDR</strong>; синтаксис записей &mdash; как у Xray, на его документацию ссылается и wiki v2rayN.</p>''',
        },
        {
            'h2': 'Шаг 3. Проверьте',
            'html': '''    <p>Откройте сайт &mdash; он должен идти через исходящее подключение с тегом из правила, остальные сайты &mdash; как раньше. Если сайт не открывается или идёт мимо прокси, пройдите по списку частых проблем.</p>''',
        },
        {
            'h2': 'Частые проблемы',
            'html': '''    <h3>Правило не срабатывает</h3>
    <p>Правила проверяются сверху вниз, срабатывает первое совпавшее &mdash; если выше стоит правило, которое уже забирает этот трафик (например, общее <code>geosite</code>-правило), до правила NetRoute очередь не дойдёт. Переставьте правила NetRoute выше.</p>

    <h3>Xray не стартует после правки</h3>
    <p>Проверьте JSON: лишняя запятая или вторая секция <code>routing</code> ломают конфиг. Вставлять нужно только объекты из массива <code>rules</code>, а не весь файл целиком.</p>

    <h3>Тег не найден</h3>
    <p><code>outboundTag</code> должен буквально совпадать с тегом существующего outbound. В NetRoute тег задаётся в поле <strong>Интерфейс</strong> до скана.</p>

    <h3>Streisand</h3>
    <p>Streisand &mdash; клиент для iOS, macOS и visionOS с настройкой прокси по правилам («Rule-based Proxy Setup» в описании в App Store). Как добавить в него собственные правила, смотрите в документации приложения; списки доменов и сетей из файла NetRoute для этого подойдут.</p>

    <h3>Несколько сайтов в одном файле</h3>
    <p>Нажмите <strong>URL list</strong> рядом с кнопкой анализа и вставьте список сайтов &mdash; NetRoute соберёт один набор правил на всех, файл будет называться <code>bulk_N_rules.json</code>.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS и утечки',
        'html': '''    <p>Правило по домену в Xray сопоставляется с именем назначения; как и куда при этом разрешаются имена, определяют <code>domainStrategy</code> и секция <code>dns</code> вашего конфига &mdash; правила NetRoute их не меняют. Запросы браузера идут туда, куда настроен его собственный DNS: в Chrome отключите «Использовать безопасный DNS» или укажите в нём резолвер, которому доверяете, иначе Chrome разрешает имена в обход клиента.</p>
    <p>Проверка: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> при включённом клиенте должен показывать не резолвер провайдера.</p>''',
    },
    'official_docs': [
        {'url': 'https://xtls.github.io/config/routing.html', 'label': 'Xray: Routing &mdash; domainStrategy, порядок правил, формы domain и ip (zh)'},
        {'url': 'https://github.com/MHSanaei/3x-ui', 'label': '3X-UI &mdash; README и документация панели (en)'},
        {'url': 'https://github.com/MHSanaei/3x-ui/blob/main/docs/content/docs/ru/operations/outbounds-routing.mdx', 'label': '3X-UI: Исходящие соединения и маршрутизация (ru)'},
        {'url': 'https://github.com/2dust/v2rayN/wiki/Description-of-custom-routing-rules', 'label': 'v2rayN: описание пользовательских правил маршрутизации (zh)'},
        {'url': 'https://github.com/2dust/v2rayCustomRoutingList', 'label': 'v2rayN: формат списков правил для импорта (en)'},
    ],
    'example_file': 'xray-routing.json',
    'example_desc': 'фрагмент конфига Xray-core с секцией <code>routing</code>; рядом &mdash; <code>v2rayn-rules.json</code> для импорта в v2rayN',
    'card': {
        'badge': 'proxy',
        'badge_label': 'Прокси-клиент',
        'title': 'Xray / 3X-UI / v2rayN',
        'text': 'Правила routing.rules с доменами и сетями сайта: в конфиг Xray-core, в настройки Xray панели 3X-UI или импортом правил в v2rayN.',
    },
    'related_desc': 'правила routing.rules для Xray-core, 3X-UI и v2rayN',
    'date_published': '2026-10-17',
}

# Guía: rule-set de sing-box (sing-box, Hiddify y otros clientes basados en sing-box). Español.
# Mismos hechos y fuentes que singbox_ru.py (verificados 2026-10-16); etiquetas de la extensión de _locales/es.
PAGE = {
    'title': 'Rule-set de sing-box de cualquier sitio para Hiddify — guía | NetRoute',
    'description': 'Cómo obtener en NetRoute un rule-set de sing-box con dominios y redes de un sitio y conectarlo en sing-box o Hiddify: route.rule_set, action route, .srs.',
    'keywords': 'sing-box rule-set, sing-box rule_set source, sing-box domain_suffix ip_cidr, hiddify sing-box config, sing-box srs compile, split tunneling sing-box, reglas sing-box para un sitio web, sing-box enrutar por dominio',
    'og_title': 'Rule-set de sing-box desde cualquier sitio web: dominios y redes para Hiddify y sing-box',
    'og_description': 'NetRoute convierte los dominios y redes de un sitio web en un rule-set de sing-box. Conéctalo en route.rule_set con una regla action route, o compílalo a .srs.',
    'breadcrumb': 'sing-box',
    'h1': 'Rule-set de sing-box desde cualquier sitio web: dominios y redes para Hiddify y sing-box',
    'lead': 'sing-box y los clientes construidos sobre él &mdash; las apps oficiales de sing-box, Hiddify, NekoBox &mdash; deciden qué pasa por el proxy mediante <strong>reglas</strong>: listas de dominios y redes que desde la versión 1.8.0 se empaquetan como rule-sets. NetRoute construye ese rule-set directamente desde un sitio web: abre el sitio, haz clic en «Analizar sitio web», descarga el <code>.json</code>.',
    'howto': {
        'name': 'Cómo conectar un rule-set de NetRoute en sing-box',
        'description': 'Genera un rule-set en el formato de sing-box con la extensión NetRoute, describe el archivo en route.rule_set y añade una entrada en route.rules con action route y el outbound de tu proxy.',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Genera el rule-set en NetRoute', 'text': 'Abre el sitio web en Chrome, inicia NetRoute, elige «sing-box / Hiddify / NekoBox» en «SO de destino», haz clic en «Analizar sitio web» y descarga <sitio>_rules.json.'},
            {'name': 'Describe el archivo en la configuración de sing-box', 'text': 'Añade en route.rule_set una entrada de type local con format source y el path al archivo (o type remote con url cuando el archivo está publicado), y en route.rules una entrada con rule_set, action route y el outbound de tu proxy.'},
            {'name': 'Comprueba la configuración', 'text': 'Ejecuta sing-box check -c config.json, inicia sing-box y abre el sitio.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'Qué contiene el archivo',
            'html': '''    <p>Un rule-set en el formato fuente (<code>source</code>) es un documento JSON con <code>version</code> y <code>rules</code>. NetRoute escribe los dominios y las redes como <strong>dos reglas separadas</strong>: según la documentación de sing-box, las condiciones dentro de una regla se combinan con un AND lógico, así que una sola regla con dominios y redes coincidiría solo cuando ambos coincidieran.</p>
    <pre><code>{
  "version": 1,
  "rules": [
    { "domain_suffix": ["github.com", "githubusercontent.com"] },
    { "ip_cidr": ["140.82.112.0/20", "185.199.108.0/22", "2606:50c0::/32"] }
  ]
}</code></pre>
    <ul>
        <li><code>domain_suffix</code> &mdash; coincidencia por sufijo de dominio: el propio dominio y todos sus subdominios. NetRoute compacta la lista: cuando la página usa <code>api.github.com</code> y <code>github.com</code>, solo queda <code>github.com</code>; el prefijo <code>www.</code> se descarta. Se listan todos los dominios del escaneo, incluidos los que no se resolvieron a una IP.</li>
        <li><code>ip_cidr</code> &mdash; coincidencia por red. Son las mismas redes agregadas que NetRoute emitiría como rutas para un router, IPv4 e IPv6 juntas; la regla está presente cuando al menos un dominio se resolvió a una dirección.</li>
        <li><code>version: 1</code> &mdash; la primera versión del formato, introducida en sing-box 1.8.0.</li>
    </ul>''',
        },
        {
            'h2': 'Qué necesitas',
            'html': '''    <ul>
        <li>sing-box 1.8.0 o más reciente: el binario <code>sing-box</code> en un equipo, servidor o router, o las apps oficiales <em>sing-box for Android</em>, <em>sing-box for Apple platforms</em>, <em>sing-box for Desktop</em></li>
        <li>o <a href="https://github.com/hiddify/hiddify-app" target="_blank" rel="noopener">Hiddify</a> &mdash; un cliente construido sobre el núcleo de sing-box que, según su README, acepta configuraciones en el formato de sing-box (Android, iOS, Windows, macOS, Linux)</li>
        <li>Un outbound de proxy funcional en la configuración &mdash; cualquier protocolo</li>
        <li>La extensión <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> en Chrome</li>
    </ul>
    <div class="callout">
        <strong>NekoBox para Android</strong> también funciona sobre el núcleo de sing-box, pero, según su README, de una suscripción toma solo los nodos e ignora las reglas de enrutamiento. Un rule-set solo puede llegar a él dentro de una configuración completa de sing-box.
    </div>''',
        },
        {
            'h2': 'Paso 1. Genera el rule-set en NetRoute',
            'html': '''    <ol>
        <li>Abre el sitio web en Chrome y recarga la página para que el sniffer de la extensión vea las solicitudes en segundo plano</li>
        <li>Inicia <strong>NetRoute</strong></li>
        <li>En <strong>SO de destino</strong> elige <strong>sing-box / Hiddify / NekoBox</strong> &mdash; el grupo «Clientes proxy»</li>
        <li>Los campos <strong>IP de puerta de enlace</strong> y <strong>Dispositivo</strong> no afectan a este formato</li>
        <li>Haz clic en <strong>Analizar sitio web</strong></li>
        <li>En la pestaña <strong>Dominios</strong> desmarca lo que no necesites &mdash; contadores, redes publicitarias, CDN de terceros; las reglas se actualizan al instante</li>
        <li>Haz clic en <strong>Descargar</strong>: el archivo recibe el nombre del sitio, por ejemplo <code>github_com_rules.json</code></li>
    </ol>
    <div class="callout">
        <strong>Sobre las redes.</strong> La regla <code>ip_cidr</code> está siempre en el archivo cuando hay direcciones resueltas, y no estorba a la regla de dominios. Si quieres solo dominios &mdash; elimina la segunda regla del archivo. Si quieres menos redes &mdash; elige <strong>IPv4 Only</strong> en <strong>Modo de ruta</strong>: la regla no conservará prefijos IPv6.
    </div>''',
        },
        {
            'h2': 'Paso 2. Describe el archivo en la configuración de sing-box',
            'html': '''    <p>Un archivo local junto a la configuración. <code>format</code> puede omitirse cuando la ruta del archivo termina en <code>.json</code> o <code>.srs</code>; desde 1.10.0 sing-box recarga el archivo por sí mismo cuando cambia.</p>
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
        <li><code>outbound</code> &mdash; el tag de tu outbound de proxy. <code>"action": "route"</code> es obligatorio a partir de sing-box 1.11.0: el antiguo campo <code>outbound</code> directamente en la regla está obsoleto allí.</li>
        <li><code>final</code> &mdash; el outbound por defecto para todo lo que no coincidió con ninguna regla; <code>direct</code> da el split tunneling clásico.</li>
    </ul>
    <p>Un archivo por URL. Sube el <code>.json</code> a un repositorio de GitHub o a tu propio servidor e indica el enlace directo al archivo raw; por defecto sing-box lo actualiza una vez al día (<code>update_interval</code> = <code>1d</code>):</p>
    <pre><code>{
  "type": "remote",
  "tag": "netroute",
  "format": "source",
  "url": "https://raw.githubusercontent.com/you/rules/main/github_com_rules.json",
  "update_interval": "1d"
}</code></pre>
    <p>Si el enlace tiene que descargarse a través del proxy: hasta sing-box 1.13 lo hacía el campo <code>download_detour</code> con el tag de un outbound; 1.14.0 lo declaró obsoleto en favor de <code>http_client</code>, y 1.16.0 lo eliminó.</p>
    <div class="callout">
        <strong>Hiddify.</strong> La app acepta configuraciones en el formato de sing-box &mdash; añade el bloque <code>route</code> de arriba junto con tu outbound a esa configuración e impórtala como perfil. Cómo se importa exactamente un perfil en tu versión de Hiddify se describe en la documentación de la app.
    </div>''',
        },
        {
            'h2': 'Paso 3. Comprueba',
            'html': '''    <p>La sintaxis de la configuración junto con el rule-set:</p>
    <pre><code>sing-box check -c config.json</code></pre>
    <p>Después inicia sing-box y abre el sitio. Si se abre a través del proxy mientras los demás sitios salen directamente &mdash; la regla funciona. Si no, repasa los problemas frecuentes de abajo.</p>''',
        },
        {
            'h2': 'Rule-set compilado (.srs)',
            'html': '''    <p>Para listas grandes sing-box ofrece un formato binario. Compila el archivo de NetRoute con el comando de la documentación:</p>
    <pre><code>sing-box rule-set compile github_com_rules.json
# → github_com_rules.srs</code></pre>
    <p>En la configuración indica <code>"format": "binary"</code> y la ruta al <code>.srs</code>. Para una docena de sitios no es necesario.</p>''',
        },
        {
            'h2': 'Problemas frecuentes',
            'html': '''    <h3>sing-box rechaza el archivo</h3>
    <p>Los rule-sets aparecieron en sing-box 1.8.0; las versiones anteriores y los clientes construidos sobre ellas no conocen el formato. NetRoute escribe la mínima <code>version: 1</code> &mdash; todas las versiones posteriores la leen.</p>

    <h3>La regla no coincide con un subdominio</h3>
    <p><code>domain_suffix</code> cubre solo los subdominios de los dominios de la lista. Si el sitio obtiene datos de otro dominio, debería verse en la pestaña <strong>Dominios</strong> de NetRoute. Recorre el sitio antes de escanear &mdash; inicia sesión, abre un video &mdash; para que el sniffer de la extensión vea también las solicitudes diferidas.</p>

    <h3>Las conexiones por IP eluden el proxy</h3>
    <p>Una regla de dominio necesita que sing-box conozca el nombre de destino. Para eso sirve el sniffing: toma el nombre del campo Host de HTTP y del Server Name en TLS y QUIC. Desde sing-box 1.11.0 el sniffing se activa con una regla con <code>"action": "sniff"</code> en <code>route.rules</code> (el antiguo campo <code>sniff</code> del inbound está obsoleto y se eliminó en 1.13.0). Las conexiones sin nombre se comparan con la regla <code>ip_cidr</code> &mdash; para servicios cuyas direcciones cambian, activa <strong>Optimización de rutas &rarr; Prefijo BGP</strong> en las opciones de NetRoute: las redes pasan a ser los prefijos anunciados en lugar de direcciones sueltas.</p>

    <h3>Un rule-set para varios sitios</h3>
    <p>Haz clic en <strong>Lista de URL</strong> junto al botón de análisis y pega la lista de sitios &mdash; NetRoute construye un rule-set para todos ellos; el archivo se llama <code>bulk_N_rules.json</code>.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS y fugas',
        'html': '''    <p>Una regla de dominio no cambia cómo el navegador resuelve los nombres: la consulta DNS de <code>github.com</code> sigue yendo al resolver configurado en el sistema o en el propio navegador, y cuando ese es el resolver del ISP, el ISP ve los nombres de los sitios.</p>
    <ul>
        <li>En sing-box las reglas DNS pueden referenciar el mismo rule-set: una entrada en <code>dns.rules</code> con <code>"rule_set": "netroute"</code>, <code>"action": "route"</code> y <code>server</code> envía las consultas de estos dominios al servidor DNS elegido. Para que el propio servidor salga por el proxy, dale un <code>detour</code> con el tag del outbound &mdash; un campo de los Dial Fields compartidos; los servidores en el nuevo formato (<code>"type": "https"</code> y otros) aparecieron en sing-box 1.12.0.</li>
        <li>En Chrome desactiva «Usar DNS seguro» o apúntalo a un resolver en el que confíes: el DNS-over-HTTPS propio del navegador funciona saltándose el resolver del sistema &mdash; consulta la <a href="https://github.com/Alexander2k/netroute-site" target="_blank" rel="noopener">sección Troubleshooting</a> del proyecto.</li>
    </ul>
    <p>Comprobación: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> con el cliente activado debe mostrar el resolver del proxy, no el del ISP.</p>''',
    },
    'official_docs': [
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/', 'label': 'sing-box: Rule Set &mdash; campos local y remote'},
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/source-format/', 'label': 'sing-box: Source Format &mdash; version, el comando compile'},
        {'url': 'https://sing-box.sagernet.org/configuration/rule-set/headless-rule/', 'label': 'sing-box: Headless Rule &mdash; domain_suffix, ip_cidr'},
        {'url': 'https://sing-box.sagernet.org/configuration/route/rule_action/', 'label': 'sing-box: Rule Action &mdash; route, sniff'},
        {'url': 'https://sing-box.sagernet.org/configuration/dns/rule/', 'label': 'sing-box: DNS Rule'},
        {'url': 'https://github.com/hiddify/hiddify-app', 'label': 'Hiddify &mdash; README: formatos de configuración compatibles'},
    ],
    'shot_format': 'singbox',
    'shot_caption': 'El popup de NetRoute con el formato «sing-box / Hiddify / NekoBox»: la pestaña Rutas contiene el rule-set terminado, el contador muestra el número de reglas. Datos del escaneo: una página de github.com.',
    'example_file': 'singbox-rules.json',
    'example_desc': 'un rule-set en el formato fuente con reglas <code>domain_suffix</code> e <code>ip_cidr</code>',
    'card': {
        'badge': 'proxy',
        'badge_label': 'Cliente proxy',
        'title': 'sing-box / Hiddify',
        'text': 'Un rule-set con los dominios y redes de un sitio: archivo local o URL en route.rule_set, compilación a .srs.',
    },
    'related_desc': 'rule-set para sing-box y Hiddify',
    'date_published': '2026-10-16',
}

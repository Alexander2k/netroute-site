# Guía: reglas de enrutamiento de Xray — Xray-core, 3X-UI, v2rayN, Streisand. Español.
# Mismos hechos y fuentes que xray_ru.py (verificados 2026-10-17); etiquetas de la extensión de _locales/es.
PAGE = {
    'title': 'Reglas de enrutamiento Xray para 3X-UI y v2rayN — guía | NetRoute',
    'description': 'Cómo obtener en NetRoute reglas routing.rules de Xray con dominios y redes de un sitio y aplicarlas en Xray-core, en Xray Settings de 3X-UI o en v2rayN.',
    'keywords': 'xray routing rules, xray reglas de enrutamiento, xray domain: outboundTag, xray split tunneling, 3x-ui routing rules, 3x-ui xray settings routing, v2rayn importar reglas, v2rayn routing setting, v2rayn reglas de enrutamiento personalizadas, xray json routing',
    'og_title': 'Reglas de enrutamiento de Xray desde cualquier sitio web',
    'og_description': 'NetRoute convierte los dominios y redes de un sitio web en routing.rules de Xray — para una configuración de Xray-core, el panel 3X-UI y la importación de reglas en v2rayN.',
    'breadcrumb': 'Xray',
    'h1': 'Reglas de enrutamiento de Xray desde cualquier sitio web: Xray-core, 3X-UI, v2rayN',
    'lead': 'Xray dirige las conexiones mediante <code>routing.rules</code>: listas de dominios y direcciones más el tag de un outbound. NetRoute construye esas reglas desde un sitio web en dos variantes: un fragmento de configuración de Xray-core &mdash; que sirve también para el panel 3X-UI, donde la configuración de Xray se edita como JSON &mdash; y un archivo para importar reglas en v2rayN.',
    'howto': {
        'name': 'Cómo aplicar reglas de enrutamiento de Xray desde NetRoute',
        'description': 'Genera reglas en el formato Xray o v2rayN con la extensión NetRoute y pégalas en routing.rules de una configuración de Xray-core, en los ajustes de Xray del panel 3X-UI, o impórtalas en v2rayN desde el portapapeles.',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Genera las reglas en NetRoute', 'text': 'Abre el sitio web en Chrome, inicia NetRoute, elige «Xray / 3X-UI / Streisand» o «v2rayN (rules import)» en «SO de destino», escribe el tag de tu outbound en el campo «Dispositivo» (proxy por defecto), haz clic en «Analizar sitio web» y descarga el archivo.'},
            {'name': 'Inserta las reglas', 'text': 'Xray-core y 3X-UI: añade los objetos de rules al principio de routing.rules de tu configuración. v2rayN: Routing → Routing Setting → Import Rules From Clipboard, responde «yes» (sí) a la pregunta sobre añadir las reglas para conservar las existentes.'},
            {'name': 'Comprueba', 'text': 'Reinicia Xray (el panel 3X-UI lo recarga por sí mismo) y abre el sitio — debería pasar por el outbound con el tag indicado.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'Qué contiene el archivo',
            'html': '''    <p><strong>El formato «Xray / 3X-UI / Streisand»</strong> es un fragmento de configuración de Xray-core con una sección <code>routing</code>. Los dominios y las redes son dos reglas, cada una con su propia lista y un <code>outboundTag</code> común:</p>
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
        <li><code>domain:name</code> &mdash; según la documentación de Xray, el propio dominio y sus subdominios. La lista está compactada: cuando se encuentran <code>api.github.com</code> y <code>github.com</code>, solo queda <code>github.com</code>; <code>www.</code> se descarta. Se incluyen todos los dominios del escaneo, también los que no se resolvieron a una IP.</li>
        <li><code>ip</code> &mdash; direcciones en forma CIDR; las mismas redes agregadas que NetRoute emite como rutas de router, IPv4 e IPv6.</li>
        <li><code>outboundTag</code> &mdash; el tag del outbound del campo <strong>Dispositivo</strong> de NetRoute; <code>proxy</code> por defecto.</li>
        <li><code>domainStrategy: IPIfNonMatch</code> &mdash; según la documentación de Xray, un dominio se resuelve a una dirección solo cuando ninguna regla coincidió por nombre; el valor por defecto del propio Xray es <code>AsIs</code>, sin resolución.</li>
    </ul>
    <p><strong>El formato «v2rayN (rules import)»</strong> es un array de reglas con la forma que v2rayN importa desde el portapapeles o un archivo (como en el repositorio <code>v2rayCustomRoutingList</code> del autor de v2rayN):</p>
    <pre><code>[
  { "port": "", "outboundTag": "proxy", "domain": ["domain:github.com", "domain:githubusercontent.com"], "enabled": true, "remarks": "NetRoute github.com domains" },
  { "port": "", "outboundTag": "proxy", "ip": ["140.82.112.0/20", "185.199.108.0/22", "2606:50c0::/32"], "enabled": true, "remarks": "NetRoute github.com networks" }
]</code></pre>''',
        },
        {
            'h2': 'Qué necesitas',
            'html': '''    <ul>
        <li>Xray-core con un outbound configurado y un tag conocido &mdash; en un equipo, un servidor o en el panel <a href="https://github.com/MHSanaei/3x-ui" target="_blank" rel="noopener">3X-UI</a></li>
        <li>o <a href="https://github.com/2dust/v2rayN" target="_blank" rel="noopener">v2rayN</a> para Windows, Linux o macOS &mdash; un cliente con los núcleos Xray y sing-box</li>
        <li>La extensión <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> en Chrome</li>
    </ul>''',
        },
        {
            'h2': 'Paso 1. Genera las reglas en NetRoute',
            'html': '''    <ol>
        <li>Abre el sitio web en Chrome y recarga la página para que el sniffer de la extensión vea las solicitudes en segundo plano</li>
        <li>Inicia <strong>NetRoute</strong></li>
        <li>En <strong>SO de destino</strong>, grupo «Clientes proxy», elige <strong>Xray / 3X-UI / Streisand</strong> para una configuración de Xray-core o <strong>v2rayN (rules import)</strong> para importar en v2rayN</li>
        <li>En el campo <strong>Dispositivo</strong> introduce el tag de tu outbound &mdash; el texto de ejemplo del campo muestra el valor por defecto <code>proxy</code>. El campo <strong>IP de puerta de enlace</strong> no afecta a estos formatos</li>
        <li>Haz clic en <strong>Analizar sitio web</strong></li>
        <li>En la pestaña <strong>Dominios</strong> desmarca lo que no necesites &mdash; las reglas se actualizan al instante</li>
        <li>Haz clic en <strong>Descargar</strong>: el archivo recibe el nombre del sitio, por ejemplo <code>github_com_rules.json</code></li>
    </ol>''',
        },
        {
            'h2': 'Paso 2a. Xray-core: inserta las reglas en la configuración',
            'html': '''    <p>Abre el <code>config.json</code> de Xray y añade ambos objetos de <code>rules</code> al array <code>routing.rules</code> <strong>por encima</strong> de las reglas generales. Según la documentación de Xray, las reglas se comprueban de arriba abajo y gana la primera coincidencia; una conexión que no coincidió con ninguna regla sale por el primer outbound de la configuración. Asegúrate de que <code>outboundTag</code> es igual al tag de tu outbound de proxy y de que <code>domainStrategy</code> está definido una sola vez en la sección <code>routing</code>.</p>
    <p>Reinicia Xray.</p>''',
        },
        {
            'h2': 'Paso 2b. 3X-UI: reglas en los ajustes de Xray',
            'html': '''    <p>3X-UI es un panel web para servidores Xray-core. Según su documentación, las reglas de enrutamiento son reglas de Xray con los matchers <code>domain</code>, <code>ip</code>, <code>port</code>, <code>network</code>, <code>protocol</code>, <code>inboundTag</code>, <code>sourceIP</code> y un destino <code>outboundTag</code> o <code>balancerTag</code>; no hay un editor separado por regla &mdash; editas el JSON de la configuración en <strong>Xray Settings</strong> (ajustes de Xray), y el panel recarga Xray por sí mismo.</p>
    <ol>
        <li>Abre <strong>Xray Settings</strong> en el panel</li>
        <li>Busca el array <code>routing.rules</code> en el JSON e inserta ambos objetos del archivo de NetRoute al principio</li>
        <li>Pon en <code>outboundTag</code> el tag del outbound deseado &mdash; por ejemplo una conexión WARP u otro servidor, si estos sitios deben salir por ahí</li>
        <li>Guarda &mdash; el panel recarga Xray</li>
    </ol>
    <p>En un servidor la regla significa: el tráfico de los clientes hacia estos dominios y redes lo envía el servidor al outbound indicado, el resto según lo configurado más abajo en la lista de reglas.</p>''',
        },
        {
            'h2': 'Paso 2c. v2rayN: importar las reglas',
            'html': '''    <p>Para v2rayN elige en NetRoute el formato <strong>v2rayN (rules import)</strong>. Las cadenas de la interfaz de v2rayN que hay que seguir:</p>
    <ol>
        <li>Abre el archivo descargado y copia su contenido al portapapeles</li>
        <li>En v2rayN abre <strong>Routing</strong> &rarr; <strong>Routing Setting</strong> (ajustes de enrutamiento)</li>
        <li>Elige <strong>Import Rules From Clipboard</strong>, importar reglas desde el portapapeles (también existen <strong>Import Rules From File</strong> e <strong>Import Rules From Subscription URL</strong>)</li>
        <li>A la pregunta <em>«Do you want to append rules? Choose yes to append, no to replace.»</em> responde <strong>Yes</strong> para añadir las reglas a las existentes</li>
        <li>Comprueba que el conjunto de reglas en el que han quedado está marcado como activo (<strong>Set as active rule</strong>)</li>
    </ol>
    <p>En el editor de reglas de v2rayN las mismas listas aparecen en los campos <strong>Domain</strong> e <strong>IP or IP CIDR</strong>; la sintaxis de las entradas es la de Xray, y la wiki de v2rayN remite a la documentación de Xray para ello.</p>''',
        },
        {
            'h2': 'Paso 3. Comprueba',
            'html': '''    <p>Abre el sitio &mdash; debería pasar por el outbound con el tag de la regla, los demás sitios como antes. Si el sitio no se abre o elude el proxy, repasa los problemas frecuentes.</p>''',
        },
        {
            'h2': 'Problemas frecuentes',
            'html': '''    <h3>La regla no se activa</h3>
    <p>Las reglas se comprueban de arriba abajo y gana la primera coincidencia &mdash; si una regla superior ya se queda con este tráfico (por ejemplo una regla general <code>geosite</code>), nunca se llega a la regla de NetRoute. Mueve las reglas de NetRoute hacia arriba.</p>

    <h3>Xray no arranca tras la edición</h3>
    <p>Revisa el JSON: una coma sobrante o una segunda sección <code>routing</code> rompen la configuración. Solo se insertan los objetos del array <code>rules</code>, no el archivo entero.</p>

    <h3>Tag no encontrado</h3>
    <p><code>outboundTag</code> tiene que ser literalmente igual al tag de un outbound existente. En NetRoute el tag se define en el campo <strong>Dispositivo</strong> antes del escaneo.</p>

    <h3>Streisand</h3>
    <p>Streisand es un cliente para iOS, macOS y visionOS con configuración de proxy basada en reglas («Rule-based Proxy Setup» en su descripción de la App Store). Cómo añadirle tus propias reglas se describe en la documentación de la app; las listas de dominios y redes del archivo de NetRoute sirven para ese fin.</p>

    <h3>Varios sitios en un archivo</h3>
    <p>Haz clic en <strong>Lista de URL</strong> junto al botón de análisis y pega la lista de sitios &mdash; NetRoute construye un conjunto de reglas para todos ellos; el archivo se llama <code>bulk_N_rules.json</code>.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS y fugas',
        'html': '''    <p>Una regla de dominio en Xray se compara con el nombre de destino; cómo y dónde se resuelven los nombres lo deciden <code>domainStrategy</code> y la sección <code>dns</code> de tu configuración &mdash; las reglas de NetRoute no los cambian. Las consultas del navegador van adonde esté configurado su propio DNS: en Chrome desactiva «Usar DNS seguro» o apúntalo a un resolver en el que confíes; de lo contrario Chrome resuelve los nombres saltándose el cliente.</p>
    <p>Comprobación: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> con el cliente activado no debería mostrar el resolver del ISP.</p>''',
    },
    'official_docs': [
        {'url': 'https://xtls.github.io/config/routing.html', 'label': 'Xray: Routing &mdash; domainStrategy, orden de las reglas, las formas domain e ip (zh)'},
        {'url': 'https://github.com/MHSanaei/3x-ui', 'label': '3X-UI &mdash; README y la documentación del panel'},
        {'url': 'https://github.com/MHSanaei/3x-ui/blob/main/docs/content/docs/en/operations/outbounds-routing.mdx', 'label': '3X-UI: Outbounds &amp; Routing'},
        {'url': 'https://github.com/2dust/v2rayN/wiki/Description-of-custom-routing-rules', 'label': 'v2rayN: descripción de las reglas de enrutamiento personalizadas (zh)'},
        {'url': 'https://github.com/2dust/v2rayCustomRoutingList', 'label': 'v2rayN: el formato de las listas de reglas para importar'},
    ],
    'shot_format': 'xray',
    'shot_caption': 'El popup de NetRoute con el formato «Xray / 3X-UI / Streisand»: el campo Dispositivo contiene el tag proxy, la pestaña Rutas un fragmento de routing.rules. Datos del escaneo: una página de github.com.',
    'example_file': 'xray-routing.json',
    'example_desc': 'un fragmento de configuración de Xray-core con una sección <code>routing</code>; junto a él, <code>v2rayn-rules.json</code> para importar en v2rayN',
    'card': {
        'badge': 'proxy',
        'badge_label': 'Cliente proxy',
        'title': 'Xray / 3X-UI / v2rayN',
        'text': 'routing.rules con los dominios y redes de un sitio: en una configuración de Xray-core, en los ajustes de Xray del panel 3X-UI o importando reglas en v2rayN.',
    },
    'related_desc': 'routing.rules para Xray-core, 3X-UI y v2rayN',
    'date_published': '2026-10-17',
}

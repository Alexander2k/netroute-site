# Guía: perfil de enrutamiento de Happ. Español.
# Mismos hechos y fuentes que happ_ru.py (verificados 2026-10-17); etiquetas de la extensión de _locales/es.
PAGE = {
    'title': 'Perfil de enrutamiento de Happ desde cualquier sitio — guía | NetRoute',
    'description': 'Cómo obtener en NetRoute un perfil de rutas de Happ con dominios y redes de un sitio y añadirlo con el enlace happ://routing/onadd: base64, portapapeles, QR.',
    'keywords': 'happ routing, happ perfil de enrutamiento, happ routing onadd, happ json perfil de enrutamiento, happ proxysites, happ split tunneling, happ reglas para un sitio web, happ xray enrutamiento',
    'og_title': 'Perfil de enrutamiento de Happ desde cualquier sitio web',
    'og_description': 'NetRoute convierte los dominios y redes de un sitio web en un perfil de enrutamiento de Happ. Codifícalo en base64, añádelo con un enlace happ://routing/onadd — solo estos sitios pasan por el proxy.',
    'breadcrumb': 'Happ',
    'h1': 'Perfil de enrutamiento de Happ desde cualquier sitio web',
    'lead': 'Happ es un cliente multiplataforma sobre el núcleo Xray para Windows, macOS, Linux, iOS, Android y plataformas de TV. Qué pasa por el proxy lo decide un <strong>perfil de enrutamiento</strong>: listas de dominios y direcciones. NetRoute construye ese perfil desde un sitio web como JSON, y entra en la app como un enlace <code>happ://routing/onadd/…</code>.',
    'howto': {
        'name': 'Cómo añadir a Happ un perfil de enrutamiento de NetRoute',
        'description': 'Genera un perfil de Happ con la extensión NetRoute, codifica el JSON en base64, construye el enlace happ://routing/onadd/{base64} y añádelo a Happ desde el portapapeles, por código QR o como deeplink.',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Genera el perfil en NetRoute', 'text': 'Abre el sitio web en Chrome, inicia NetRoute, elige «Happ» en «SO de destino», haz clic en «Analizar sitio web» y descarga <sitio>_rules.json.'},
            {'name': 'Construye el enlace', 'text': 'Codifica el contenido del archivo en base64 y antepón happ://routing/onadd/ — el enlace resultante añade el perfil y lo activa al instante.'},
            {'name': 'Añade el enlace a Happ', 'text': 'Copia el enlace al portapapeles, abre Happ y añádelo con el botón «+» (desde el portapapeles, por código QR o como deeplink). Reconecta después de cambiar el perfil.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'Qué contiene el archivo',
            'html': '''    <p>Un perfil de enrutamiento de Happ es un documento JSON con ajustes de DNS y de archivos geo y seis listas: qué pasa por el proxy, qué va directo y qué se bloquea &mdash; por separado para dominios y para direcciones. NetRoute rellena las listas del proxy y deja el resto en valores que Happ acepta por defecto:</p>
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
    <p>Qué significan los campos, según la documentación de Happ:</p>
    <ul>
        <li><code>GlobalProxy</code> &mdash; con <code>true</code> todo el tráfico pasa por el proxy por defecto, con <code>false</code> va directo; el mismo valor fija la salida de todo lo que no coincidió con ninguna regla. NetRoute pone <code>false</code>: solo los sitios listados pasan por el proxy.</li>
        <li><code>ProxySites</code> / <code>ProxyIp</code> &mdash; dominios y direcciones que pasan por el proxy. Los dominios se escriben como <code>domain:name</code> &mdash; según la documentación de Xray, es el dominio y todos sus subdominios; la lista está compactada, <code>www.</code> descartado. Las direcciones son las mismas redes agregadas que NetRoute emite como rutas de router, IPv4 e IPv6.</li>
        <li><code>DirectSites</code> / <code>DirectIp</code> y <code>BlockSites</code> / <code>BlockIp</code> &mdash; directo y bloqueado; NetRoute deja en directo solo las direcciones privadas (<code>geoip:private</code>).</li>
        <li><code>RouteOrder</code> &mdash; el orden en que se comprueban las reglas: primero bloqueo, luego proxy, luego directo.</li>
        <li><code>DomainStrategy</code> &mdash; la estrategia de Xray: <code>IPIfNonMatch</code> resuelve un dominio a una dirección solo cuando ninguna regla coincidió por nombre.</li>
        <li><code>RemoteDNS*</code> / <code>DomesticDNS*</code> &mdash; DNS para los sitios detrás del proxy y para el resto; <code>DoH</code> es DNS-over-HTTPS. Cambia los valores en el archivo antes de importar si quieres otros resolvers.</li>
        <li><code>Geoipurl</code> / <code>Geositeurl</code> &mdash; enlaces a geoip.dat y geosite.dat; Happ rellena los valores vacíos desde su perfil por defecto.</li>
        <li><code>LastUpdated</code> &mdash; una fecha Unix; el perfil se actualiza cuando es mayor que la anterior. NetRoute escribe la hora de generación.</li>
        <li><code>DnsHosts</code> &mdash; correspondencias manuales «dominio: IP», como un archivo hosts; vacío en el perfil de NetRoute.</li>
    </ul>''',
        },
        {
            'h2': 'Qué necesitas',
            'html': '''    <ul>
        <li>La app <a href="https://www.happ.su/main" target="_blank" rel="noopener">Happ</a> con un servidor añadido (Windows, macOS, Linux, iOS, Android, Android TV o Apple TV)</li>
        <li>La extensión <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> en Chrome</li>
        <li>Una forma de codificar un archivo en base64 &mdash; todos los sistemas tienen un comando para ello, ejemplos abajo</li>
    </ul>''',
        },
        {
            'h2': 'Paso 1. Genera el perfil en NetRoute',
            'html': '''    <ol>
        <li>Abre el sitio web en Chrome y recarga la página para que el sniffer de la extensión vea las solicitudes en segundo plano</li>
        <li>Inicia <strong>NetRoute</strong></li>
        <li>En <strong>SO de destino</strong> elige <strong>Happ</strong> &mdash; el grupo «Clientes proxy»</li>
        <li>Los campos <strong>IP de puerta de enlace</strong> y <strong>Dispositivo</strong> no afectan a este formato</li>
        <li>Haz clic en <strong>Analizar sitio web</strong></li>
        <li>En la pestaña <strong>Dominios</strong> desmarca lo que no necesites &mdash; contadores, redes publicitarias, CDN de terceros; el perfil se actualiza al instante</li>
        <li>Haz clic en <strong>Descargar</strong>: el archivo recibe el nombre del sitio, por ejemplo <code>github_com_rules.json</code></li>
    </ol>''',
        },
        {
            'h2': 'Paso 2. Construye el enlace happ://routing/…',
            'html': '''    <p>Según la documentación de Happ, un perfil se añade con un enlace en el que <code>{base64}</code> es el perfil JSON convertido a texto base64:</p>
    <ul>
        <li><code>happ://routing/add/{base64}</code> &mdash; añade el perfil a la lista;</li>
        <li><code>happ://routing/onadd/{base64}</code> &mdash; lo añade y lo activa al instante, incluso cuando otro perfil está activo.</li>
    </ul>
    <p>Codifica el archivo descargado:</p>
    <pre><code># Windows, PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("github_com_rules.json"))

# macOS
base64 -i github_com_rules.json

# Linux
base64 -w0 github_com_rules.json</code></pre>
    <p>Antepón <code>happ://routing/onadd/</code> al resultado &mdash; una sola línea, sin espacios ni saltos de línea. El enlace queda largo; es normal.</p>
    <div class="callout">
        Codifica el archivo localmente &mdash; un codificador en línea vería tu lista de sitios. Está planeado un botón integrado «Copiar como enlace de Happ» en NetRoute.
    </div>''',
        },
        {
            'h2': 'Paso 3. Añade el enlace a Happ',
            'html': '''    <p>Según la documentación de Happ, los enlaces se aceptan de tres maneras &mdash; copiados desde el portapapeles, escaneados desde un código QR y como deeplink:</p>
    <ol>
        <li>Copia el enlace construido al portapapeles</li>
        <li>Abre Happ y toca <strong>+</strong> en la esquina superior derecha de la pantalla principal</li>
        <li>Añade el enlace desde el portapapeles. A un teléfono lo más fácil es pasar el enlace como código QR o abrirlo como deeplink &mdash; el sistema ofrece abrirlo en Happ</li>
        <li>Con <code>onadd</code> el perfil ya está activo; con <code>add</code> selecciónalo en la lista de perfiles de enrutamiento</li>
        <li>Reconecta: según la documentación, los cambios de perfil se aplican tras <strong>Reconnect</strong> (reconectar)</li>
    </ol>''',
        },
        {
            'h2': 'Paso 4. Comprueba',
            'html': '''    <p>Abre el sitio para el que se construyó el perfil &mdash; debería abrirse a través del proxy, mientras que los demás sitios salen directamente (<code>GlobalProxy: false</code>). Si es al revés, comprueba qué perfil de enrutamiento está activo en Happ y que reconectaste tras la importación.</p>''',
        },
        {
            'h2': 'Problemas frecuentes',
            'html': '''    <h3>El enlace no se acepta</h3>
    <p>Comprueba que el base64 es una sola línea sin saltos (en Linux eso requiere el modificador <code>-w0</code>) y que va precedido exactamente de <code>happ://routing/onadd/</code> o <code>happ://routing/add/</code>.</p>

    <h3>El perfil se añadió pero nada cambió</h3>
    <p>Happ aplica un perfil cambiado al reconectar. Con un enlace <code>add</code> el perfil además tiene que seleccionarse como activo.</p>

    <h3>El sitio obtiene datos de otros dominios</h3>
    <p>Deberían verse en la pestaña <strong>Dominios</strong> de NetRoute &mdash; la extensión recoge los dominios de la página y de sus solicitudes en segundo plano. Recorre el sitio antes de escanear (inicia sesión, abre un video) para que las solicitudes diferidas también acaben en el perfil. Varios sitios en un perfil &mdash; el botón <strong>Lista de URL</strong> junto al botón de análisis: el archivo se llama <code>bulk_N_rules.json</code>.</p>

    <h3>Un perfil en una suscripción</h3>
    <p>Según la documentación de Happ, una suscripción JSON puede llevar estrictamente 0 o 1 perfil de enrutamiento, y un enlace de perfil puede pasarse en la cabecera <code>routing</code> o directamente en el cuerpo de la suscripción &mdash; práctico cuando repartes ajustes a varios dispositivos.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS y fugas',
        'html': '''    <p>El perfil fija dos servidores DNS: <code>RemoteDNS</code> para los sitios detrás del proxy y <code>DomesticDNS</code> para el resto &mdash; ambos por DNS-over-HTTPS (Cloudflare y Yandex en el archivo de NetRoute). Cámbialos en el JSON antes de codificar si necesitas otros resolvers. Las consultas del navegador siguen yendo adonde esté configurado su propio DNS: en Chrome desactiva «Usar DNS seguro» o apúntalo a un resolver en el que confíes; de lo contrario Chrome resuelve los nombres saltándose el cliente.</p>
    <p>Comprobación: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> con Happ activado debe mostrar el resolver del perfil, no el del ISP.</p>''',
    },
    'official_docs': [
        {'url': 'https://www.happ.su/main/dev-docs/routing.md', 'label': 'Happ: Routing &mdash; los enlaces add y onadd, campos del perfil'},
        {'url': 'https://www.happ.su/main/faq/adding-configuration-subscription.md', 'label': 'Happ: Adding Configuration/Subscription &mdash; portapapeles, código QR, deeplink'},
        {'url': 'https://www.happ.su/main/dev-docs/examples-of-links-and-parameters.md', 'label': 'Happ: Examples of links and parameters'},
        {'url': 'https://xtls.github.io/config/routing.html', 'label': 'Xray: Routing &mdash; la forma domain: y las estrategias de dominio (zh)'},
    ],
    'shot_format': 'happ',
    'shot_caption': 'El popup de NetRoute con el formato «Happ»: la pestaña Rutas contiene el perfil de enrutamiento que queda por codificar en un enlace. Datos del escaneo: una página de github.com.',
    'example_file': 'happ-routing.json',
    'example_desc': 'un perfil de enrutamiento de Happ con las listas <code>ProxySites</code> y <code>ProxyIp</code>',
    'card': {
        'badge': 'proxy',
        'badge_label': 'Cliente proxy',
        'title': 'Happ',
        'text': 'Un perfil de enrutamiento con los dominios y redes de un sitio: base64 → enlace happ://routing/onadd → importación desde el portapapeles o un código QR.',
    },
    'related_desc': 'perfil de enrutamiento como enlace happ://routing',
    'date_published': '2026-10-17',
}

# Guía: lista de sitios de AmneziaVPN para split tunneling. Español.
# Mismos hechos y fuentes que amnezia_ru.py (verificados 2026-10-17); etiquetas de la extensión de _locales/es; los
# nombres de pantallas de AmneziaVPN siguen docs.amnezia.org/documentation/instructions/vpn-split-tunneling (inglés).
PAGE = {
    'title': 'Lista de sitios de AmneziaVPN para split tunneling — guía | NetRoute',
    'description': 'Cómo obtener en NetRoute un archivo de importación para AmneziaVPN con direcciones y subredes de un sitio y activar el split tunneling de sitios: modos, ⋮, IPv4.',
    'keywords': 'amnezia split tunneling, amneziavpn split tunneling sitios, amnezia lista de sitios, amnezia importar ip-list.json, amnezia only the sites listed here, amneziawg split tunneling sitios, amnezia subredes de servicio',
    'og_title': 'Lista de sitios de AmneziaVPN desde cualquier sitio web',
    'og_description': 'NetRoute convierte las direcciones y subredes de un sitio web en un archivo para importar en AmneziaVPN — split tunneling de sitios en tres pasos.',
    'breadcrumb': 'AmneziaVPN',
    'h1': 'Lista de sitios de AmneziaVPN desde cualquier sitio web',
    'lead': 'AmneziaVPN puede enviar a través de la VPN solo las direcciones de una lista &mdash; split tunneling de sitios. La lista se compone de direcciones y subredes IPv4, y construirla a mano para un sitio con decenas de dominios lleva mucho tiempo. NetRoute lo hace desde la página: abre el sitio, haz clic en «Analizar sitio web», descarga el archivo para importar.',
    'howto': {
        'name': 'Cómo importar una lista de sitios de NetRoute en AmneziaVPN',
        'description': 'Genera una lista de AmneziaVPN con la extensión NetRoute, importa el archivo en los ajustes de split tunneling de sitios mediante el menú ⋮ y activa el modo «Only the sites listed here will be accessed through the VPN».',
        'total_time': 'PT5M',
        'steps': [
            {'name': 'Genera la lista en NetRoute', 'text': 'Abre el sitio web en Chrome, inicia NetRoute, elige «AmneziaVPN (site list)» en «SO de destino», haz clic en «Analizar sitio web» y descarga <sitio>_rules.json.'},
            {'name': 'Importa el archivo en AmneziaVPN', 'text': 'Abre los ajustes de split tunneling de sitios, elige la importación en el menú ⋮ — reemplazar la lista o añadir a la existente — y selecciona el archivo.'},
            {'name': 'Activa el modo y conéctate', 'text': 'Elige el modo «Only the sites listed here will be accessed through the VPN», activa el split tunneling y conéctate a la VPN.'},
        ],
    },
    'sections': [
        {
            'id': 'syntax',
            'h2': 'Qué contiene el archivo',
            'html': '''    <p>El archivo es un array JSON de entradas con la forma en que la propia AmneziaVPN exporta su lista: cada entrada tiene un <code>hostname</code>, la lista de direcciones <code>ips</code> y la primera de ellas en <code>ip</code> &mdash; para versiones antiguas de la app.</p>
    <pre><code>[
  { "hostname": "api.github.com", "ips": ["140.82.112.4"], "ip": "140.82.112.4" },
  { "hostname": "github.com", "ips": ["140.82.112.3"], "ip": "140.82.112.3" },
  { "hostname": "140.82.112.0/20", "ips": [], "ip": "" },
  { "hostname": "185.199.108.0/22", "ips": [], "ip": "" }
]</code></pre>
    <ul>
        <li><strong>Hosts con direcciones.</strong> Según el código fuente del cliente, AmneziaVPN no resuelve nombres al importar &mdash; las entradas se guardan tal cual, y la resolución solo ocurre cuando un sitio se añade a mano. Por eso NetRoute escribe cada host con las direcciones IPv4 encontradas durante el escaneo; los hosts sin direcciones IPv4 se omiten. Los nombres no se compactan: <code>www.ozon.ru</code> y <code>ozon.ru</code> son entradas separadas con sus propias direcciones.</li>
        <li><strong>Subredes.</strong> Tras los hosts vienen las redes IPv4 agregadas &mdash; las mismas que NetRoute emite como rutas de router; con <strong>Optimización de rutas &rarr; Prefijo BGP</strong> son los prefijos anunciados del proveedor en lugar de direcciones sueltas.</li>
        <li><strong>Solo IPv4.</strong> Según la documentación de AmneziaVPN, IPv6 no está soportado; las direcciones IPv6 no se escriben en el archivo.</li>
    </ul>''',
        },
        {
            'h2': 'Qué necesitas',
            'html': '''    <ul>
        <li>La app <a href="https://amnezia.org/" target="_blank" rel="noopener">AmneziaVPN</a> con una conexión configurada. Según la documentación, el split tunneling por direcciones no está disponible en Amnezia Free</li>
        <li>Una plataforma con tunneling por direcciones: según la documentación, iOS, macOS y Linux soportan solo ese, Windows y Android tanto por direcciones como por aplicaciones</li>
        <li>La extensión <a href="https://chromewebstore.google.com/detail/netroute-domain-to-ip-map/binkmcoafjdoalbbbakpaojbknjmdmla" target="_blank" rel="noopener">NetRoute</a> en Chrome</li>
    </ul>''',
        },
        {
            'h2': 'Paso 1. Genera la lista en NetRoute',
            'html': '''    <ol>
        <li>Abre el sitio web en Chrome y recarga la página para que el sniffer de la extensión vea las solicitudes en segundo plano</li>
        <li>Inicia <strong>NetRoute</strong></li>
        <li>En <strong>SO de destino</strong> elige <strong>AmneziaVPN (site list)</strong> &mdash; el grupo «Clientes VPN»</li>
        <li>Los campos <strong>IP de puerta de enlace</strong> y <strong>Dispositivo</strong> no afectan a este formato</li>
        <li>Haz clic en <strong>Analizar sitio web</strong></li>
        <li>En la pestaña <strong>Dominios</strong> desmarca lo que no necesites &mdash; contadores, redes publicitarias, CDN de terceros; la lista se actualiza al instante</li>
        <li>Haz clic en <strong>Descargar</strong>: el archivo recibe el nombre del sitio, por ejemplo <code>github_com_rules.json</code></li>
    </ol>
    <div class="callout">
        <strong>Sobre las direcciones que cambian.</strong> La documentación de AmneziaVPN advierte de que una dirección obtenida de un dominio no se actualiza automáticamente, y de que los servicios grandes necesitan subredes enteras. Por eso, antes de escanear activa <strong>Optimización de rutas &rarr; Prefijo BGP</strong> en las opciones de NetRoute &mdash; el archivo lleva entonces las subredes anunciadas, que sobreviven a la rotación de direcciones en las CDN.
    </div>''',
        },
        {
            'h2': 'Paso 2. Importa el archivo en AmneziaVPN',
            'html': '''    <p>Según la documentación de AmneziaVPN, la lista se importa desde los ajustes de split tunneling de sitios:</p>
    <ol>
        <li>Abre <strong>Split tunneling</strong> y ve a los ajustes de split tunneling de sitios</li>
        <li>Toca el icono <strong>⋮</strong> y elige la importación: reemplazar la lista &mdash; cuando empiezas desde cero, o añadir los sitios importados a los existentes &mdash; cuando amplías</li>
        <li>Selecciona el archivo descargado; las entradas aparecen en la lista</li>
    </ol>''',
        },
        {
            'h2': 'Paso 3. Activa el modo y conéctate',
            'html': '''    <ol>
        <li>Elige el modo <strong>Only the sites listed here will be accessed through the VPN</strong> (solo se accederá a través de la VPN a los sitios listados aquí) &mdash; solo los sitios del archivo pasan por el túnel, el resto del tráfico sale directamente. El segundo modo, <strong>Addresses from the list should not be accessed via VPN</strong> (no se debe acceder por VPN a las direcciones de la lista), hace lo contrario: excluye la lista del túnel</li>
        <li>Activa el split tunneling de sitios</li>
        <li>Conéctate a la VPN</li>
    </ol>''',
        },
        {
            'h2': 'Paso 4. Comprueba',
            'html': '''    <p>Abre el sitio para el que se construyó la lista: debería abrirse a través de la VPN, y los sitios fuera de la lista directamente. Si el sitio se abre solo en parte &mdash; faltan algunos de sus dominios en la lista: revisa la pestaña <strong>Dominios</strong> en NetRoute, recorre el sitio antes de escanear (inicia sesión, abre un video) para que el sniffer vea las solicitudes diferidas, e importa el archivo de nuevo reemplazando la lista.</p>''',
        },
        {
            'h2': 'Problemas frecuentes',
            'html': '''    <h3>El archivo no se importa</h3>
    <p>Según el código fuente del cliente, el archivo debe ser un array JSON de objetos; un array simple de cadenas se rechaza. El archivo de NetRoute ya tiene la forma correcta &mdash; comprueba que se descargó completo y que no se editó en un editor de texto que reemplace las comillas.</p>

    <h3>El sitio funcionaba y luego dejó de hacerlo</h3>
    <p>Las direcciones del sitio cambiaron. Vuelve a construir el archivo en NetRoute &mdash; con <strong>Prefijo BGP</strong> activado lleva subredes en lugar de direcciones sueltas &mdash; e impórtalo reemplazando la lista.</p>

    <h3>Tráfico ajeno pasó por la VPN</h3>
    <p>La documentación de AmneziaVPN advierte de que las subredes amplias de los servicios grandes pueden capturar tráfico ajeno. Desmarca las CDN de terceros en la pestaña <strong>Dominios</strong> de NetRoute o desactiva la optimización BGP para esos sitios.</p>

    <h3>Se perdió la conexión con tu propio servidor</h3>
    <p>Según la documentación, cuando la dirección de tu servidor VPN cae dentro de una de las subredes añadidas la conexión se rompe &mdash; elimina esa subred de la lista.</p>

    <h3>Varios sitios en una lista</h3>
    <p>Haz clic en <strong>Lista de URL</strong> junto al botón de análisis y pega la lista de sitios &mdash; NetRoute construye un archivo para todos ellos, llamado <code>bulk_N_rules.json</code>.</p>''',
        },
    ],
    'dns_leak': {
        'h2': 'DNS y fugas',
        'html': '''    <p>El split tunneling de AmneziaVPN funciona por direcciones: el tráfico hacia las direcciones de la lista entra en el túnel, mientras que las consultas DNS del navegador van adonde esté configurado su resolver. Cuando ese es el resolver del ISP, este ve los nombres de los sitios incluso cuando el tráfico en sí pasa por la VPN. En Chrome desactiva «Usar DNS seguro» o apúntalo a un resolver en el que confíes; los ajustes de DNS de la propia AmneziaVPN se describen en su documentación.</p>
    <p>Comprobación: <a href="https://www.dnsleaktest.com/" target="_blank" rel="noopener">dnsleaktest.com</a> con la VPN conectada muestra qué resolver responde a tus consultas.</p>''',
    },
    'official_docs': [
        {'url': 'https://docs.amnezia.org/documentation/instructions/vpn-split-tunneling', 'label': 'AmneziaVPN: split tunneling &mdash; modos, importación, límites'},
        {'url': 'https://github.com/amnezia-vpn/amnezia-client', 'label': 'AmneziaVPN: código fuente del cliente &mdash; el formato de importación en ipSplitTunnelingController'},
        {'url': 'https://amnezia.org/blog/what-is-split-tunneling-and-why-you-need-it', 'label': 'Amnezia: qué es el split tunneling'},
    ],
    'shot_format': 'amnezia',
    'shot_caption': 'El popup de NetRoute con el formato «AmneziaVPN (site list)»: la pestaña Rutas contiene la lista para importar, hosts con direcciones y subredes. Datos del escaneo: una página de github.com.',
    'example_file': 'amnezia-sites.json',
    'example_desc': 'una lista para importar en AmneziaVPN: hosts con direcciones y subredes',
    'card': {
        'badge': 'vpn',
        'badge_label': 'Cliente VPN',
        'title': 'AmneziaVPN',
        'text': 'Una lista de sitios para split tunneling: hosts con direcciones IPv4 y subredes, importación por el menú ⋮.',
    },
    'related_desc': 'lista de sitios para split tunneling',
    'date_published': '2026-10-17',
}

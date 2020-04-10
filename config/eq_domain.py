_author__ = 'alexeyymnaikin'

# Списки эквивалентности доменов, используются для схлопывания ns/mx
eq_domains = {
    'google.com': 'googlemail.com',
    'timeweb.ru': 'timeweb.org',

    # The Secondary (Slave) Domain Name System (DNS) Server of Itlibitum, Corp.
    'primary.su': 'secondary.su',
    # Hetzner Online AG DNS Service
    'first-ns.de': 'second-ns.de',
    'second-ns.de': 'second-ns.com'
}


provider_eq = {
    'cloudflare.com.': 'cloudflare.com',
    'hosting.reg.ru.': 'hosting.reg.ru',
    'expired.reg.ru.': 'expired.reg.ru',
    '.mail.ru.': 'mail.ru',
    '.hostinger.': 'hostinger',
    '.nsone.net.': 'nsone.net',
    '.expired.r01.ru.': 'expired.r01.ru',
    '.expired.beget.com.': 'expired.beget.com',
    '.infobox.ru.': 'infobox.ru',
    '.shop.reg.ru.': 'shop.reg.ru',
    '.hosting.su.': 'hosting.su'
}

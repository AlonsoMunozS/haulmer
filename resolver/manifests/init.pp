class resolver($domainname = $domain, $searchpath = [], $nameservers = ['8.8.8.8', '8.8.4.4']) {
    
    file { '/etc/resolv.conf':
        owner   => root,
        group   => root,
        mode    => '0644',
        content => template('resolver/resolv.conf.erb'),
    }
}

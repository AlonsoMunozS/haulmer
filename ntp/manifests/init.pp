class ntp(
    $servers='ntp.shoa.cl',
    $localtime='/usr/share/zoneinfo/America/Santiago',
    $timezone="America/Santiago") {

    $escaped_timezone=regsubst($timezone, '/', '\/', 'G')

    package { 'ntp':
        ensure => latest
    }->
    package { 'tzdata':
        ensure => latest
    }->
    file { '/etc/localtime':
        ensure => 'link',
        target => "${localtime}",
        force => true,
    }->
    file {'/etc/sysconfig/clock':
        content => template('ntp/clock'),
    }->
    exec { 'config_tz_var':
        command => "/bin/echo 'TZ=\"$timezone\"' >> /etc/environment",
        unless  => "/bin/grep 'TZ=' /etc/environment",
    }->
    exec { 'config_tz_environment':
        command => "/bin/sed -i 's/^TZ=.*/TZ=\"$escaped_timezone\"/' /etc/environment",
        unless  => "/bin/grep '$timezone' /etc/environment",
    }->
    file { '/etc/ntp.conf':
        owner   => 'root',
        mode    => '0644',
        group       => root,
        content => template('ntp/ntpd_config'),
    }~>
    service { 'ntpd':
        ensure => running,
        enable => true,
    }
}
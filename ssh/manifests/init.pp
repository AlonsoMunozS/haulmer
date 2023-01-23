class ssh(
    $interface=$ipaddress_eth0,
    $allowusers='',
    $gateway=$network_gateway,
    $port = '22') {

    exec { 'restart_sshd_service_post_config':
        command => '/usr/sbin/service sshd restart && systemctl restart systemd-logind',
        refreshonly => true,
    }

    file {'/etc/ssh/sshd_config':
        content => template('ssh/sshd_config')
    }~>Exec['restart_sshd_service_post_config']
    ->
    service { 'sshd' :
        ensure => running,
        enable => true,
    }
}

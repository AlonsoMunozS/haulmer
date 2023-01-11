class zabbix ($ip_server='10.0.4.2'){
	#import "pip"

	file { '/etc/zabbix/':
		ensure => directory,
		mode => '0644',
	}#->

#	if $osfamily == 'RedHat' and $operatingsystemrelease =~ /^5.*/  {
#		file { '/etc/sysconfig/network-scripts/route-eth1':
#			ensure  => file,
#		 	owner  => 'root',
#		 	group  => 'root',
#		 	mode   => '0644',
#		 	content => "10.0.4.0/23 via $internal_gateway dev eth1",
#		}~> Service { 'network':
#				ensure    => 'running',
#				enable    => 'true',
#		}
#	} else {
#		network::mroute { 'zabbix_ip_route':
#			routes => {
#				ipaddress => '10.0.4.0',
#				netmask   => '255.255.254.0',
#				gateway   => '10.2.51.254',
#				interface   => 'eth1',
#			}
#		}
#	}


#	if $osfamily == 'RedHat' and $operatingsystemrelease !~ /^5.*/  {
#		pip::install {"function_install":}->
#		pip::install_lib {"requests":;"docker": version=>"3.4.1";}
#	}

	exec { 'delete_zabbix_2.2':
		onlyif  => "/usr/bin/test -f /usr/local/etc/zabbix_agentd.conf",
		command => "/etc/init.d/zabbix_agentd stop; rm -rfv /usr/local/bin/zabbix_* /usr/local/sbin/zabbix_* /usr/local/etc/zabbix_* /var/lock/subsys/zabbix_agentd /etc/rc.d/init.d/zabbix_* /etc/init.d/zabbix_* /tmp/zabbix_agentd.pid;",
    }->

	file {'zabbix_agentd_script_files':
	    source => "puppet:///modules/zabbix/scripts/",
	    recurse => true,
	    purge => true,
	    force => true,
	    path  => "/etc/zabbix/zabbix_agentd_script.d/",
	    mode => '0755',
	    owner => "root",
	    group => "root",
	    notify => Exec['restart_zabbix_agent'],
	}->

	file {'zabbix_agentd_conf':
		source => "puppet:///modules/zabbix/conf/",
		recurse => true,
		purge => true,
		force => true,
		path  => "/etc/zabbix/zabbix_agentd.d/",
		mode => '0644',
		owner => "root",
		group => "root",
		notify => Exec['restart_zabbix_agent'],
	}->

	cron { 'ASSP_info_Zabbix':
		command  => '/usr/bin/perl /etc/zabbix/zabbix_agentd_script.d/send_stats_to_zabbix.pl',
		ensure => absent,
		user     => 'root',
		month    => '*',
		monthday => '*',
		hour     => '*',
		minute   => '*/2',
	}

##	file {'zabbix_agentd_modules':
##		source => "puppet:///modules/zabbix/modules/",
##		recurse => true,
##		purge => true,
##		force => true,
##		path  => "/etc/zabbix/modules/",
##		mode => '0644',
##		owner => "root",
##		group => "root",
##		notify => Exec['restart_zabbix_agent'],
##	}

	if $osfamily == 'RedHat' and $operatingsystemrelease =~ /^7.*/  {
	 	package {'zabbix-release':
			provider => rpm,
		 	ensure   => installed,
		 	source   => "http://repo.zabbix.com/zabbix/3.4/rhel/7/x86_64/zabbix-release-3.4-2.el7.noarch.rpm"
		}->
		package {'zabbix-agent':
			ensure    => 'present',
			require => Package['zabbix-release'],
		}->
		package { 'zabbix-sender':
			ensure => installed,
		}

	}

	if $osfamily == 'RedHat' and $operatingsystemrelease =~ /^6.*/  {
	  	package {'zabbix-release':
			provider => rpm,
			ensure   => installed,
			source   => "http://repo.zabbix.com/zabbix/3.4/rhel/6/x86_64/zabbix-release-3.4-1.el6.noarch.rpm"
		}->
		package {'zabbix-agent':
			ensure    => 'present',
			require => Package['zabbix-release'],
		}
	}

	if $osfamily == 'RedHat' and $operatingsystemrelease =~ /^5.*/  {
		file {'/root/zabbix-agent-3.4.9-1.el5.x86_64.rpm':
			ensure => present,
			mode   => "0755",
			source => "puppet:///modules/zabbix/zabbix-agent-3.4.9-1.el5.x86_64.rpm",
		}->
		package{ 'zabbix-agent':
    		provider => rpm,
    		ensure => installed,
    		source  => "/root/zabbix-agent-3.4.9-1.el5.x86_64.rpm",
    	}
	}

	service { 'zabbix-agent':
		ensure => 'running',
		enable => 'true',
		require => Package['zabbix-agent'],
	}

	file { "zabbix_agentd.conf":
		path => "/etc/zabbix/zabbix_agentd.conf",
		content => template("zabbix/zabbix_agentd.rb"),
		owner     => 'root',
		group     => 'root',
		mode      => "0644",
		#require => Package['zabbix-agent'],
		notify => Exec['restart_zabbix_agent'],
	}

	exec { 'restart_zabbix_agent':
		command => 'service zabbix-agent restart',
		path => '/usr/bin:/usr/sbin:/bin:/usr/local/bin:/sbin',
		refreshonly => true,
	}
}

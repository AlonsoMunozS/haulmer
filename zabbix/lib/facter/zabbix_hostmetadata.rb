Facter.add("zabbix_hostmetadata") do
    setcode do
    zabbix_hostmetadata = %x{if /usr/bin/test -e /etc/zabbix/zabbix_hostmetadata; then cat /etc/zabbix/zabbix_hostmetadata; else echo "error"; fi}
    zabbix_hostmetadata = zabbix_hostmetadata.gsub("\n", "")
    end
end

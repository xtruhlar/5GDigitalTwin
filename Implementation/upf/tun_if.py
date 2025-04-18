import click
import subprocess
import ipaddress

"""
Usage in command line:
e.g:
$ python3 tun_if.py --tun_ifname ogstun --ipv4_range 192.168.100.0/24 --ipv6_range 2001:230:cafe::/48
"""


def validate_ip_net(ctx, param, value):
    try:
        ip_net = ipaddress.ip_network(value)
        return ip_net
    except ValueError:
        raise click.BadParameter(
            'Value does not represent a valid IPv4/IPv6 range')


@click.command()
@click.option('--tun_ifname',
              required=True,
              help='TUN interface name e.g. ogstun')
@click.option('--ipv4_range',
              required=True,
              callback=validate_ip_net,
              help='UE IPv4 Address range in CIDR format e.g. 192.168.100.0/24')
@click.option('--ipv6_range',
              required=True,
              callback=validate_ip_net,
              help='UE IPv6 Address range in CIDR format e.g. 2001:230:cafe::/48')
@click.option('--nat_rule',
              default='yes',
              help='Option specifying whether to add NATing iptables rule or not')
def start(tun_ifname,
          ipv4_range,
          ipv6_range,
          nat_rule):

    # Get the first IP address in the IP range and netmask prefix length
    first_ipv4_addr = next(ipv4_range.hosts(), None)
    if not first_ipv4_addr:
        raise ValueError('Invalid UE IPv4 range. Only one IP given')
    else:
        first_ipv4_addr = first_ipv4_addr.exploded
    first_ipv6_addr = next(ipv6_range.hosts(), None)
    if not first_ipv6_addr:
        raise ValueError('Invalid UE IPv6 range. Only one IP given')
    else:
        first_ipv6_addr = first_ipv6_addr.exploded

    ipv4_netmask_prefix = ipv4_range.prefixlen
    ipv6_netmask_prefix = ipv6_range.prefixlen

    # Setup the TUN interface, set IP address and setup IPtables
    # if ls /sys/class/net | grep "ogstun" ; then ip link delete ogstun; fi
    execute_bash_cmd('ip tuntap add name ' + tun_ifname + ' mode tun')
    execute_bash_cmd('ip addr add ' + first_ipv4_addr + '/' +
                     str(ipv4_netmask_prefix) + ' dev ' + tun_ifname)
    execute_bash_cmd('ip addr add ' + first_ipv6_addr + '/' +
                     str(ipv6_netmask_prefix) + ' dev ' + tun_ifname)
    execute_bash_cmd('ip link set ' + tun_ifname + ' mtu 1450')
    execute_bash_cmd('ip link set ' + tun_ifname + ' up')
    if nat_rule == 'yes':
        execute_bash_cmd('if ! iptables-save | grep -- \"-A POSTROUTING -s ' + ipv4_range.with_prefixlen + ' ! -o ' + tun_ifname + ' -j MASQUERADE\" ; then ' +
                         'iptables -t nat -A POSTROUTING -s ' + ipv4_range.with_prefixlen + ' ! -o ' + tun_ifname + ' -j MASQUERADE; fi')
        execute_bash_cmd('if ! ip6tables-save | grep -- \"-A POSTROUTING -s ' + ipv6_range.with_prefixlen + ' ! -o ' + tun_ifname + ' -j MASQUERADE\" ; then ' +
                         'ip6tables -t nat -A POSTROUTING -s ' + ipv6_range.with_prefixlen + ' ! -o ' + tun_ifname + ' -j MASQUERADE; fi')
        execute_bash_cmd('if ! iptables-save | grep -- \"-A INPUT -i ' + tun_ifname + ' -j ACCEPT\" ; then ' +
                         'iptables -A INPUT -i ' + tun_ifname + ' -j ACCEPT; fi')
        execute_bash_cmd('if ! ip6tables-save | grep -- \"-A INPUT -i ' + tun_ifname + ' -j ACCEPT\" ; then ' +
                         'ip6tables -A INPUT -i ' + tun_ifname + ' -j ACCEPT; fi')


def execute_bash_cmd(bash_cmd):
    # print("Executing: /bin/bash -c " + bash_cmd)
    return subprocess.run(bash_cmd, stdout=subprocess.PIPE, shell=True)


if __name__ == '__main__':
    start()

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.
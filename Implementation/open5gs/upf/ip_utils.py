import click
import sys
import ipaddress

"""
Script used to fetch first IP address in a given IP range. i.e. the calling bash script reads the std output

Usage in command line:
e.g:
$ python3 ip_utils.py --ip_range 192.168.100.0/24
$ python3 ip_utils.py --ip_range 2001:230:cafe::/48
"""


def validate_ip_net(ctx, param, value):
    try:
        ip_net = ipaddress.ip_network(value)
        return ip_net
    except ValueError:
        raise click.BadParameter(
            'Value does not represent a valid IPv4/IPv6 range')


@click.command()
@click.option('--ip_range',
              required=True,
              callback=validate_ip_net,
              help='UE IPv4/IPv6 Address range in CIDR format e.g. 192.168.100.0/24 or 2001:230:cafe::/48')
def start(ip_range):

    # Get the first IP address in the IP range and netmask prefix length
    first_ip_addr = next(ip_range.hosts(), None)
    if not first_ip_addr:
        raise ValueError('Invalid UE IPv4 range. Only one IP given')
    else:
        first_ip_addr = first_ip_addr.exploded
        print(str(first_ip_addr))

if __name__ == '__main__':
    try:
        start()
        sys.exit(0)
    except ValueError:
        sys.exit(1)

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.
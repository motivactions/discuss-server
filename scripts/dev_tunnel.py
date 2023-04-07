#!/usr/bin/env python3

import argparse
from os import system

TUNNEL_SERVER = "dev-tunnel.ovh-6.server.mitija.com"
TUNNEL_USER = "dev"

cli = argparse.ArgumentParser(description="SSH tunnel to dev-tunnel.mitija.com")
cli.add_argument(
    "-r",
    "--remote-port",
    type=int,
    default=0,
    required=False,
    help="Destination port on remote server",
)
cli.add_argument(
    "-l", "--local-port", type=int, required=True, help="Local port to forward"
)
cli.add_argument(
    "-H",
    "--host",
    type=str,
    default="localhost",
    required=False,
    help="Host to forward to",
)
cli.add_argument("-d", "--subdomain", required=True, help="Subdomain to use for tunnel")
args = cli.parse_args()

if args.remote_port == 0:
    import random

    args.remote_port = random.randint(1025, 59999)

if args.remote_port <= 1024 or args.remote_port > 59999:
    print("Remote port must be between 1025 and 59999")
    exit(1)

from shutil import which

if which("ssh") is None:
    print("ssh is not in PATH")
    exit(1)

if which("cloudflared") is None:
    print("cloudflared is not in PATH")
    exit(1)

system(
    f'ssh -o StrictHostKeyChecking=no -o ProxyCommand="cloudflared access ssh --hostname {TUNNEL_SERVER}" -R{args.remote_port}:{args.host}:{args.local_port} {TUNNEL_USER}@mplus-dev-tunnel {args.subdomain} {args.remote_port}'
)

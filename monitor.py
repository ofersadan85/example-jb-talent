import argparse
import sys
from datetime import datetime
from time import sleep

import httpx


def write_log(url: str, log=True, verbose: int = 0):
    message = ""
    if verbose > 0:
        message = "Website is DOWN"
    if verbose > 1:
        message = url + " is DOWN"
    if verbose > 0:
        print(message)
    if log:
        with open("monitor.log", "a") as f:
            f.write(str(datetime.now()) + " " + message + "\n")


def monitor_url(
    url: str, interval: float, valid_statuses: list[int], log: bool, verbose: int
):
    while True:
        try:
            response = httpx.get(url)
            if response.status_code in valid_statuses:
                print("Website is up")
            else:
                write_log(url, log, verbose)
        except Exception:
            write_log(url, log, verbose)
        sleep(interval)


if __name__ == "__main__":
    print(sys.argv)

    parser = argparse.ArgumentParser(description="Continuously monitor URLs")
    parser.add_argument(
        "url", help="URL to monitor, must include http:// or https://"
    )  # parser.add_argument("--url", required=True)
    parser.add_argument(
        "-n",
        "--interval",
        type=float,
        default=0.5,
        help="Interval in seconds (default 3.0)",
    )
    parser.add_argument(
        "-s",
        "--status-code",
        type=int,
        default=[200],
        # action="append",
        nargs="+",
        help="HTTP Status code for registering success (default 200)",
    )
    
    # action="append" => append to list (but it's better to use nargs)
    # action="count" => int value of how many times the flag was set (better to use with default=0)
    # action="store_true" => boolean value, True if flag is set, False by default
    # action="store_false" => boolean value, False if flag is set, True by default

    # nargs=3  => 3 arguments
    # nargs="*"  => zero or more arguments
    # nargs="+"  => one or more arguments
    # nargs="?"  => zero or one arguments

    parser.add_argument("--no-log", action="store_false", dest="log")
    parser.add_argument("-v", "--verbose", action="count", default=0)
    
    args = parser.parse_args()
    print(args)

    if not (args.url.startswith("http://") or args.url.startswith("https://")):
        parser.print_usage()
        exit("URL must include http:// or https://")

    monitor_url(args.url, args.interval, args.status_code, args.log, args.verbose)

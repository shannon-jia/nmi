# -*- coding: utf-8 -*-

"""Console script for rps."""

import click
from .log import get_log
import asyncio
from .server import Site
from .api import start


def validate_url(ctx, param, value):
    try:
        return value
    except ValueError:
        raise click.BadParameter('url need to be format: tcp://ipv4:port')


@click.command()
@click.option('--unit_id', default=1,
              envvar='UNIT_ID',
              help='the NM’s Unit ID, ENV: UNIT_ID, default: 1')
@click.option('--device_type', default='plc_430',
              envvar='DEVICE_TYPE',
              help='NM_DeviceType, also ENV: DEVICE_TYPE')
@click.option('--port', default=80,
              envvar='SVC_PORT',
              help='Api port, default=80, ENV: SVC_PORT')
@click.option('--debug', is_flag=True)
def main(unit_id, device_type, port, debug):

    click.echo("See more documentation at http://www.mingvale.com")

    info = {
        'unit_id': unit_id,
        'device_type': device_type,
        'api_port': port,
    }
    log = get_log(debug)
    log.info('Basic Information: {}'.format(info))

    loop = asyncio.get_event_loop()
    loop.set_debug(0)

    try:
        site = Site(unit_id, device_type, loop)
        site.start()
        api_task = loop.create_task(start(port, site))
        loop.run_forever()
    except OSError as e:
        log.error(e)
    except KeyboardInterrupt:
        if api_task:
            api_task.cancel()
            loop.run_until_complete(api_task)
    finally:
        loop.stop()
        loop.close()

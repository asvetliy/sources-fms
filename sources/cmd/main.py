import logging
import asyncio
import uvloop
import os

from argparse import ArgumentParser
from sources.config import Config
from sources.core.use_cases.use_cases import UseCases


def init_config() -> Config:
    parser = ArgumentParser(description='Feed Service')
    parser.add_argument(
        '-config',
        dest='filepath',
        required=False,
        help='config file path (default is ./config/main.[json])',
        metavar='./PATH/TO/FILE or $HOME/app/<FILE>.json',
        default=None
    )
    parsed_args = parser.parse_args()
    if parsed_args.filepath is not None:
        if not os.path.isfile(parsed_args.filepath):
            log.warning(f'The file [{parsed_args.filepath}] does not exist!')
            return Config()
        else:
            try:
                return Config(parsed_args.filepath)
            except Exception as e:
                log.exception(e, exc_info=False)
    return Config()


async def init_app(config_: Config) -> dict:
    repository = await config_.repo.make()
    use_cases = UseCases.make(repository)
    entrypoints = []

    for e in config_.entrypoints:
        t = e.start(use_cases)
        entrypoints.append({'type': e.type, 'threads': t})

    return {
        'config': config_,
        'repository': repository,
        'use_cases': use_cases,
        'entrypoints': entrypoints,
    }


if __name__ == '__main__':
    log = logging.getLogger(__name__)
    uvloop.install()
    loop = asyncio.get_event_loop()
    config = init_config()
    log.info('Starting...')
    try:
        app = loop.run_until_complete(init_app(config))
        loop.run_forever()
    except KeyboardInterrupt as e:
        log.warning('Caught keyboard interrupt. Canceling tasks...')
    except Exception as e:
        log.exception(str(e), exc_info=False)
    finally:
        loop.close()

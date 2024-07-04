#!/usr/bin/env python3

import argparse
import aiosmtpd
import asyncio
from aiosmtpd.controller import Controller

class CustomAUTHHandler:
    def start(self, host=('localhost', 9999)):
        print(f'[i] Running SMTP server on {host[0]}:{host[1]}')
        loop = asyncio.get_event_loop()
        controller = Controller(CustomAUTHHandler(), hostname=host[0], port=host[1], auth_require_tls=False, auth_required=True)

        controller.start()

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            controller.stop()

    async def handle_AUTH(self, server, session, envelope, args):
        print(f'[i] Auth Method: {args}')
        if len(args) == 1 and args[0] == 'PLAIN':
            credentials = await server.challenge_auth('')
            print(f'[i] Result: {credentials}')
        elif len(args) == 1 and args[0] == 'LOGIN':
            username = await server.challenge_auth('Username')
            password = await server.challenge_auth('Password')
            print(f'[i] Result: {username}:{password}')

        session.authenticated = True
        await server.push("235 2.7.0 Authentication successful")

if __name__ == '__main__':
    # cli arguemnt parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('--laddr', default="127.0.0.1", help='Local IP to listen on')
    parser.add_argument('--lport', default=9999, help='Local port to listen on')
    args = parser.parse_args()
    
    server = CustomAUTHHandler()
    server.start(host=(args.laddr if args.laddr else None , args.lport if args.lport else None))

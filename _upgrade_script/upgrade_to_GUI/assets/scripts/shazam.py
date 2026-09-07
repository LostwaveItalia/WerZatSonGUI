import argparse
import asyncio
from shazamio import Shazam

async def main(file):
    response = await Shazam().recognize(file)
    if 'matches' in response and len(response['matches']) > 0:
        print(response['track']['share']['text'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search an MP3 file on Shazam\'s API')
    parser.add_argument('file', type=str)
    args = parser.parse_args()
    asyncio.run(main(args.file))

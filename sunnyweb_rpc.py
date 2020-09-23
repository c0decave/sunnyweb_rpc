#!/usr/bin/env python3
# more information
#http://files.sma.de/dl/2585/SWebBoxRPC-BA-en-14.pdf
#http://files.sma.de/dl/4253/SWebBoxRPC-eng-BUS112713.pdf
#https://community.openhab.org/t/sma-sunny-webbox-data-with-script/67745
#http://files.sma.de/dl/2585/SWebBoxRPC-BA-US-CA_en-14.pdf

import argparse
import json
import os
import sys
import requests

__tool_name__ =  'sunnybox_rpc'
__tool_version__ = 'v0.1'
__tool_author__ = 'dash'
__tool_date__ = 'September 2020'

funcs = ['GetPlantOverview','GetProDataChannels','GetProcessData']
sunny_headers = {"User-Agent": "Feuerfux", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Connection": "close","Content-Type": "application/json"}

def get_devices(sunny_url):

        sunny_data = 'RPC={"version": "1.0","proc": "GetDevices","id":"1","format": "JSON","passwd": "000000000000000000*","params":{"devices":[{"key": "WR5KA-05:2000631420"}]}}'
        data = requests.post(sunny_url, headers=sunny_headers, data=sunny_data)
        jsonres = (data.json())
        total_dev = jsonres['result']['totalDevicesReturned'] 
        devices = {}
        for dev in jsonres['result']['devices']:
            devices[dev['key']] = dev['name']
        print('[+] Found {0} devices'.format(total_dev))
        for dev in devices.keys():
            print('[+] Device: {0}'.format(dev))

        return devices


def run(args):

    target = args.target
    port = args.port

    sunny_url = "http://{0}:{1}/rpc".format(target,str(port))
    devices = get_devices(sunny_url)
    # get the parameters
    for dev in devices:
        print('[+] GetParameter {0}'.format(dev))
        sunny_data = 'RPC={"version": "1.0","proc": "GetParameter","id":"1","format": "JSON","passwd": "000000000000000000*","params":{"devices":[{"key": "'+ dev +'"}]}}'
        data = requests.post(sunny_url, headers=sunny_headers, data=sunny_data)
        json_res =  (data.json())
        print(json.dumps(json_res, indent=1))

        print('[+] GetParameterChannels {0}'.format(dev))
        sunny_data = 'RPC={"version": "1.0","proc": "GetParameterChannels","id":"1","format": "JSON","passwd": "000000000000000000*","params":{"device":"'+ dev +'"}}'
        data = requests.post(sunny_url, headers=sunny_headers, data=sunny_data)
        json_res =  (data.json())
        print(json.dumps(json_res, indent=1))

        print('[+] GetProcessDataChannels {0}'.format(dev))
        sunny_data = 'RPC={"version": "1.0","proc": "GetProcessDataChannels","id":"1","format": "JSON","passwd": "000000000000000000*","params":{"device":"'+ dev +'"}}'
        data = requests.post(sunny_url, headers=sunny_headers, data=sunny_data)
        json_res =  (data.json())
        print(json.dumps(json_res, indent=1))

    for rpc_req in funcs:
        sunny_data = 'RPC={"version": "1.0","proc": "'+rpc_req+'","id":"1","format": "JSON","passwd": "000000000000000000*","params":{"devices":[{"key": ""}]}}'
        data = requests.post(sunny_url, headers=sunny_headers, data=sunny_data)
        json_res =  (data.json())
        print(json.dumps(json_res, indent=1))



def main():
    parser_desc = "{0} {1} {2} in {3}".format(
        __tool_name__, __tool_version__, __tool_author__, __tool_date__)
    parser = argparse.ArgumentParser(
        prog=__tool_name__, description=parser_desc)
    parser.add_argument('-t', '--target', action='store', dest='target',required=False, help='Define target', default='127.0.0.1')
    parser.add_argument('-p', '--port', action='store', type=int, dest='port',required=False, help='Define port', default=80)
                        

    if len(sys.argv) < 2:
        parser.print_help(sys.stderr)
        sys.exit()

    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()


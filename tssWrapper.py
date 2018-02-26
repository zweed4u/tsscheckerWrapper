#!/usr/bin/python3
# -*- coding: UTF-8 -*-
# add option for installation/build from git

# include save path option and move to allow for multiple saves of same version blob
# implement for loop to download multiples put this number in config and pull with parser
# eg. MaxSessions 20
# MaxSessions len(number of versions)
# Fix version display in threads always prints same version
# Git pull tsschecker/download compiled zip
# mac or linux binary
# os detection using os.environ? for name/file call
# implement find tsschecker folder or download it
# implement threading and blobs to save to designated destination (tsschecker command? cd?)

import os
import requests
import datetime
import threading
import configparser
import subprocess

# Get the project directory to avoid using relative paths
PROJECT_ROOT_DIR = os.getcwd()

# Parse configuration file
c = configparser.ConfigParser()
configFilePath = os.path.join(PROJECT_ROOT_DIR, 'config.cfg')
c.read(configFilePath)


class Config:
    # Pull user info
    ecid = c.get('device', 'ecid')
    deviceIdentifier = c.get('device', 'deviceIdentifier')


def build_firmware_dict():
    deviceInfo = {}
    json_response = requests.request('GET',
                                     'https://api.ipsw.me/v2.1/firmwares.json').json()
    for device in json_response['devices']:
        deviceInfo[device] = {}
        for version in json_response['devices'][device]['firmwares']:
            deviceInfo[device][version['version']] = version['buildid']
    return deviceInfo


deviceInfo = build_firmware_dict()
tsscheckerBinPath = os.path.join(PROJECT_ROOT_DIR, 'tsschecker_linux')


# need to adjust this function so that threads are made in for loop
def tsscheckSweep(version, myDeviceLUT, projectFolder, binaryPath, deviceId,
                  ecid):
    try:
        tsschecker_output = subprocess.run(
            [binaryPath, '-d', deviceId, '-e', ecid, '-i', version,
             '--buildid', myDeviceLUT[version], '-s', '--save-path',
             projectFolder], stdout=subprocess.PIPE)
        for line in tsschecker_output.stdout.decode().split('\n'):
            if 'signed' in line:
                result = line
                break
            else:
                result = '\'signed\' KEYWORD NOT FOUND'
        print(str(
            datetime.datetime.now().time()) + ' :: ' + result + ' :: ' + version)
    except Exception as e:
        # quit here the identifier provided by config is not in the device info dictionary
        print(str(e))


if __name__ == '__main__':
    """
    Main slots controller
    """
    user_config = Config()
    for version in deviceInfo[user_config.deviceIdentifier].keys():
        print(version, 'Thread initialized!')
        t = threading.Thread(target=tsscheckSweep, args=(
            version, deviceInfo[user_config.deviceIdentifier],
            PROJECT_ROOT_DIR,
            tsscheckerBinPath, user_config.deviceIdentifier,
            user_config.ecid,))
        t.start()
    print('')

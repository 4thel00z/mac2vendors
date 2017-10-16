import re


def write_mac_json(source, destination):
    '''
        >>> write_mac_json("vendors.txt","vendor.json")

        :param source: str
        :param destination: str
        :return:
    '''

    with open(source) as inputFile:
        lines = [line.split("\t") for line in inputFile.readlines() if
                 not line.startswith("  # ") or not line.strip() == ""]

        short = [[line[0]] + [line[1].strip("\n")] for line in lines if len(line) == 2]
        long = [line[0:2] + [line[2].rstrip("\n")] for line in lines if len(line) == 3]

        payload = {
            "short": {line[0]: line for line in short},
            "long": {line[0]: line for line in long}
        }

        write_json(destination, payload)


def write_json(destination, payload):
    import json
    with open(destination, mode="w") as outputFile:
        json.dump(payload, outputFile)


def read_json(source):
    import json
    with open(source) as inputFile:
        return json.load(inputFile)


def get_mac_vendor(source: str = "vendors.json", mac: str = "00:00:00"):
    assert_is_mac(mac)
    mac_addresses = read_json(source=source)
    short = mac_addresses["short"]
    long = mac_addresses["long"]

    if len(mac) >= 8:
        prefix = mac[:8]
        mac_identifier = short[prefix] if prefix in short else long[prefix] if prefix in long else None
        if mac_identifier is not None:
            return [mac_identifier]
        return []

    return [m for key, m in short.items() if mac.startswith(key)] + [m for key, m in long.items() if
                                                                     mac.startswith(key)]


def assert_is_mac(mac):
    '''
    >>> assert_is_mac("asdasd")
    Traceback (most recent call last):
        ...
    ValueError: [asdasd] is not a valid mac address

    >>> assert_is_mac("00:00:14:ff:fi:00")
    Traceback (most recent call last):
        ...
    ValueError: [00:00:14:ff:fi:00] is not a valid mac address

    >>> assert_is_mac("00:00:14:ff:fd:00")

    :param mac: str
    :return:
    '''
    if not re.search(r"([\dA-F]{2}(?:[-:][\dA-F]{2}){5})", mac, re.I) is not None:
        raise ValueError("[%s] is not a valid mac address" % mac)



import json

from ImageFaults import inject_external_faults


if __name__ == "__main__":
    # Get data
    # get configuration
    # do Fault injections
    # eval performance of model
    # either combined or seperately

    with open('Configuration.json', 'r') as f:
        config = json.load(f)
    # Get names of External Faults to be injected
    # Get names of External Faults to be injected

    if config["ExternalFaults"]["selected"]:
        inject_external_faults(config, 1)

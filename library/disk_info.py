#!/opt/anaconda3/bin/python3

from ansible.module_utils.basic import AnsibleModule
import platform
import psutil

def get_mount_info(mountpoint, include_total_size=True):
    """
    Get mount point information.
    """
    partitions = psutil.disk_partitions(all=True)
    info = None
    for partition in partitions:
        if partition.mountpoint == mountpoint:
            info = partition
            break

    if not info:
        return {"msg": f"Mount point '{mountpoint}' not found."}

    usage = psutil.disk_usage(mountpoint)

    result = {
        "mountpoint": info.mountpoint,
        "fstype": info.fstype,
        "device": info.device,
        "total_size": bytes2human(usage.total) if include_total_size else None,
        "free_space": bytes2human(usage.free),
    }
    return result

def bytes2human(n):
    """
    Convert bytes to human-readable format.
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return "%.1f%s" % (value, s)
    return "%sB" % n

def main():
    module = AnsibleModule(
        argument_spec={
            "mountpoint": {"required": True, "type": "str"},
            "total_size": {"required": False, "type": "bool", "default": True},
        }
    )
    mountpoint = module.params["mountpoint"]
    total_size = module.params["total_size"]
    result = get_mount_info(mountpoint, total_size)
    module.exit_json(changed=False, **result)

if __name__ == '__main__':
    main()

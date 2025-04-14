# ansible-module-disk-info

ansible localhost -M ./library -m disk_info.py -a "mountpoint=/ total_size=true"

ansible-playbook playbook_mount_info.yml -v

ansible-doc -t inventory -l 
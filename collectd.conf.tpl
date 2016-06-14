Hostname "{{ HOSTNAME }}"

FQDNLookup false
Interval 10
Timeout 2
ReadThreads 5
WriteThreads 5

LoadPlugin network
LoadPlugin Exec

<Plugin network>
    Server "{{ METRICS_HOST }}" "{{ METRICS_PORT }}"
</Plugin>

<Plugin "exec">
	Exec "operator" "python" "/usr/bin/collect-ecs.py"
</Plugin>

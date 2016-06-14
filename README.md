# collectd-ecs

A prototype of how EMC ECS metrics such as disk usage, bandwith, transactions and replication traffic can be collected by `collectd`, imported into the time series database `InfluxDB` and then displayed using `Grafana`.

## Installation

From an EMC ECS storage system, `collectd` will collect metrics and import them into `InfluxDB`.
To configure `collectd` correctly we need to add the `network` and `Exec` plugins to our `collectd.conf`:

```
LoadPlugin network
LoadPlugin Exec

<Plugin network>
    Server "influxdb" "25826"
</Plugin>

<Plugin "exec">
	Exec "operator" "python" "/usr/bin/collect-ecs.py"
</Plugin>
```

You also need to edit the EMC ECS configuration file (`emcecs-config.yml`) to set the EMC ECS IP, Token, Storagepool and Replication Group values like this::

```
ip: 104.197.166.218
token: BAAcbGtVUDJDdVp5eUlkalNSNFE2NUg3eElodjJJPQMAjAQASHVybjpzdG9yYWdlb3M6VmlydHVhbERhdGFDZW50ZXJEYXRhOmM2NDFkOTg3LTQ5NWQtNGVlOS05NDVlLWYwMDI3ZDE0MGI2NwIADTE0NjU4NDUwNzgzMTkDAC51cm46VG9rZW46YzI4MTdjOGUtMjQ4Ny00Nzk4LTg3NWItMDIyOTRmZWMxMjBhAgAC0A8=
storagepool: urn:storageos:VirtualArray:8f819354-d242-485c-becb-ad5cede8a741
replgroup: Replication_Group:urn:storageos:ReplicationGroupInfo:600127c3-e0be-4ed9-a0df-0815fa0d02d7:global
```

The default location for `emcecs-config.yml` is under `/usr/share/collectd/`. If you put it somewhere else you have to specify the configuration file location like this:

```
<Plugin "exec">
	Exec "operator" "python" "/usr/bin/collect-ecs.py" "-c" "/full/path/to/emcecs-config.yml"
</Plugin>
```

## Usage

This repo comes with a `Dockerfile` that will build your `collectd` container image correctly,
and a `docker-compose.yml` file for easy testing of a full setup of `collectd`, `InfluxDB` and `Grafana`.

After running `docker-compose up` you need to run the following commands to add the `InfluxDB` data source
and a new dashboard for EMC ECS to `Grafana`,

```
http POST http://admin:admin@192.168.99.100:3000/api/datasources < grafana/grafana-influxdb.json
http POST http://admin:admin@192.168.99.100:3000/api/dashboards/db < grafana/dashboard_emcecs.json
```

The end result will look something like this:

![Grafana dashboard showing EMC ECS metrics collected from collectd and stored in InfluxDB](docs/grafana-emc-ecs.png)

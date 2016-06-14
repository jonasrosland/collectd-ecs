import requests
import json
import configargparse

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

p = configargparse.ArgParser(default_config_files=['/usr/share/collectd/emcecs-config.yml'])
p.add('-c', '--config', required=False, is_config_file=True, help='config file path')
p.add('--ip', required=True, help='IP Address')
p.add('--token', required=True, help='SDS Auth Token')
p.add('--storagepool', required=True, help='Storagepool')
p.add('--replgroup', required=True, help='Replication Group')

args = p.parse_args()

if args.ip:
    IP = args.ip
if args.token:
    TOKEN = args.token
if args.storagepool:
    STORAGEPOOL = args.storagepool
if args.replgroup:
    REPLGROUP = args.replgroup

INTERVAL="interval=10"

headers = {'X-SDS-AUTH-TOKEN': TOKEN}
diskresponse = requests.get('https://' + IP + ':4443/dashboard/storagepools/' + STORAGEPOOL, verify=False, headers=headers)
response = requests.get('https://' + IP + ':4443/dashboard/zones/localzone/', verify=False, headers=headers)
replresponse = requests.get('https://' + IP + ':4443/dashboard/replicationgroups/' + REPLGROUP, verify=False, headers=headers)

data = response.json()
diskdata = diskresponse.json()
repldata = replresponse.json()

#print("Storage pool name " + data["name"])
print("PUTVAL emcecs/nodes/gauge-numNodes " + INTERVAL + " N:" + data["numNodes"])
print("PUTVAL emcecs/nodes/gauge-numGoodNodes "  + INTERVAL + " N:" + data["numGoodNodes"])
print("PUTVAL emcecs/nodes/gauge-numSuspectNodes "  + INTERVAL + " N:" + data["numSuspectNodes"])
print("PUTVAL emcecs/nodes/gauge-numBadNodes "  + INTERVAL + " N:" + data["numBadNodes"])
print("PUTVAL emcecs/nodes/gauge-nodeMemoryUtilizationAvgCurrent "  + INTERVAL + " N:" + data["nodeMemoryUtilizationAvgCurrent"][0]["Percent"])
print("PUTVAL emcecs/nodes/gauge-nodeCpuUtilizationAvgCurrent "  + INTERVAL + " N:" + data["nodeCpuUtilizationAvgCurrent"][0]["Percent"])
#print("-------------------------")
print("PUTVAL emcecs/disks/gauge-numDisks "  + INTERVAL + " N:" + data["numDisks"])
print("PUTVAL emcecs/disks/gauge-numGoodDisks "  + INTERVAL + " N:" + data["numGoodDisks"])
print("PUTVAL emcecs/disks/gauge-numSuspectDisks "  + INTERVAL + " N:" + data["numSuspectDisks"])
print("PUTVAL emcecs/disks/gauge-numBadDisks "  + INTERVAL + " N:" + data["numBadDisks"])
#print("-------------------------")
print("PUTVAL emcecs/space/gauge-diskSpaceTotalCurrent "  + INTERVAL + " N:" + str(round(int(data["diskSpaceTotalCurrent"][0]["Space"])/1024/1024/1024)))
print("PUTVAL emcecs/space/gauge-diskSpaceFreeCurrent "  + INTERVAL + " N:" + str(round(int(data["diskSpaceFreeCurrent"][0]["Space"])/1024/1024/1024)))
print("PUTVAL emcecs/space/gauge-diskSpaceAllocatedCurrent "  + INTERVAL + " N:" + str(round(int(data["diskSpaceAllocatedCurrent"][0]["Space"])/1024/1024/1024)))
#print("-------------------------")
print("PUTVAL emcecs/transactions/gauge-transactionErrorsCurrent "  + INTERVAL + " N:" + data["transactionErrorsCurrent"]["all"][0]["Rate"])
print("PUTVAL emcecs/transactions/gauge-transactionReadLatencyCurrent "  + INTERVAL + " N:" + data["transactionReadLatencyCurrent"][0]["Latency"])
print("PUTVAL emcecs/transactions/gauge-transactionWriteLatencyCurrent "  + INTERVAL + " N:" + data["transactionWriteLatencyCurrent"][0]["Latency"])
#print("NIC Utilization in %   " + data["nodeNicUtilizationAvgCurrent"][0]["Percent"])
print("PUTVAL emcecs/bandwidth/gauge-diskReadBandwidthTotalCurrent "  + INTERVAL + " N:" + str(round(float(data["diskReadBandwidthTotalCurrent"][0]["diskIO"]))))
print("PUTVAL emcecs/bandwidth/gauge-diskWriteBandwidthTotalCurrent "  + INTERVAL + " N:" + str(round(float(data["diskWriteBandwidthTotalCurrent"][0]["diskIO"]))))
#print("-------------------------")
print("PUTVAL emcecs/bandwidth/gauge-diskReadBandwidthRecoveryCurrent "  + INTERVAL + " N:" + data["diskReadBandwidthRecoveryCurrent"][0]["diskIO"])
print("PUTVAL emcecs/bandwidth/gauge-diskWriteBandwidthRecoveryCurrent "  + INTERVAL + " N:" + data["diskWriteBandwidthRecoveryCurrent"][0]["diskIO"])
print("PUTVAL emcecs/bandwidth/gauge-diskReadBandwidthGeoCurrent "  + INTERVAL + " N:" + data["diskReadBandwidthGeoCurrent"][0]["diskIO"])
print("PUTVAL emcecs/bandwidth/gauge-diskWriteBandwidthGeoCurrent "  + INTERVAL + " N:" + data["diskWriteBandwidthGeoCurrent"][0]["diskIO"])
print("PUTVAL emcecs/bandwidth/gauge-nodeNicBandwidthAvgCurrent "  + INTERVAL + " N:" + data["nodeNicBandwidthAvgCurrent"][0]["Bandwidth"])
print("PUTVAL emcecs/bandwidth/gauge-nodeNicReceivedBandwidthAvgCurrent "  + INTERVAL + " N:" + data["nodeNicReceivedBandwidthAvgCurrent"][0]["Bandwidth"])
print("PUTVAL emcecs/bandwidth/gauge-nodeNicTransmittedBandwidthAvgCurrent "  + INTERVAL + " N:" + data["nodeNicTransmittedBandwidthAvgCurrent"][0]["Bandwidth"])
#print("Recovery Rate          " + data["recoveryRate"][0]["Rate"])
#print("-------------------------")
print("PUTVAL emcecs/traffic/gauge-replicationEgressTrafficCurrent "  + INTERVAL + " N:" + data["replicationEgressTrafficCurrent"][0]["Bandwidth"])
print("PUTVAL emcecs/traffic/gauge-replicationIngressTrafficCurrent "  + INTERVAL + " N:" + data["replicationIngressTrafficCurrent"][0]["Bandwidth"])
#print("-------------------------")

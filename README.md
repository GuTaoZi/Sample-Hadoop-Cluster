# Sample-Hadoop-Cluster

A sample Hadoop cluster augmented with ZKFC and YARN, for MapReduce tasks.

The official Docker image of [Apache Hadoop](https://hub.docker.com/r/apache/hadoop) is based on CentOS 7, but as the EOL of CentOS 7 on June 30th, 2024, no new updates for CentOS will be made available. Time to deploy a Hadoop cluster in Docker on our own!

### Overview

In this experiment, we will set up a Hadoop cluster in Docker with 2 name nodes and 3 data nodes, along with ZKFC (Zookeeper Failover Controller) and YARN (Yet Another Resource Negotiator). 

### Use Guide

```sh
# After all the containers finish their boot-up:
docker exec -it namenode-active bash
# Inside NNA(name node active)
source /etc/profile
hadoop namenode -format
/usr/local/hadoop/sbin/start-all.sh
# Then a cluster with node managers and resource managers of YARN is settled up, we can check the node list by:

yarn node -list

# Try NNThroughputBenchmark on this cluster:
hadoop org.apache.hadoop.hdfs.server.namenode.NNThroughputBenchmark -fs hdfs://nna:9000 -op open -threads 1000 -files 100000

# Also try various benchmarks on this cluster:

hadoop jar /usr/local/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-client-jobclient-3.3.6-tests.jar nnbenchWithoutMR -baseDir /benchmarks/nnbench -numFiles 100 -replicationFactorPerFile 2 -blocksPerFile 1 -bytesPerBlock 67108864 -operation createWrite
```
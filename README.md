# Overview

This interface layer handles the communication with a Hadoop deployment via the
`hadoop-interface` interface protocol.  It will set two states when appropriate:

  * `yarn.ready` indicates that Yarn is available and ready to accept jobs
  * `hdfs.ready` indicates that HDFS is available and ready to store data

In addition, the charm providing this relation (e.g., [apache-hadoop-plugin][])
will install a JRE and the Hadoop API Java libraries, will manage the Hadoops
configuration in `/etc/hadoop/conf`, and will configure the environment in
`/etc/environment`.  The endpoint will also ensure that the distribution,
version, Java, etc. are all compatible to ensure a properly functioning
Hadoop ecosystem.


# Example Usage

An example of a charm using this interface would be:

```python
    @hook('install')
    def install():
        spark.install()

    @when('yarn.ready', 'hdfs.ready')
    def hadoop_ready(hadoop):
        spark.configure()
        spark.start()
        status_set('active', 'Spark is ready')
```

FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    openjdk-11-jdk-headless openssh-server openssh-client python3 python3-pip \
    wget curl nano net-tools iputils-ping procps ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# stable JAVA_HOME for both amd64 and arm64
RUN ln -s $(dirname $(dirname $(readlink -f $(which java)))) /usr/lib/jvm/java-home

ENV JAVA_HOME=/usr/lib/jvm/java-home
ENV HADOOP_VERSION=3.3.6
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:/opt/hadoop/bin:/opt/hadoop/sbin

# Hadoop (Apple Silicon: use hadoop-3.3.6-aarch64.tar.gz in the URL below)
RUN wget -q https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
 && tar -xzf hadoop-${HADOOP_VERSION}.tar.gz -C /opt \
 && mv /opt/hadoop-${HADOOP_VERSION} /opt/hadoop \
 && rm hadoop-${HADOOP_VERSION}.tar.gz

# passwordless SSH (same key baked in every container)
RUN mkdir -p /var/run/sshd /root/.ssh \
 && ssh-keygen -t rsa -P "" -f /root/.ssh/id_rsa \
 && cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys \
 && chmod 600 /root/.ssh/authorized_keys \
 && printf "Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile /dev/null\n" > /root/.ssh/config

# env for non-interactive SSH sessions and Hadoop daemons as root
RUN printf "JAVA_HOME=/usr/lib/jvm/java-home\nHADOOP_HOME=/opt/hadoop\nPATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/hadoop/bin:/opt/hadoop/sbin\n" > /etc/environment \
 && printf "export JAVA_HOME=/usr/lib/jvm/java-home\nexport HDFS_NAMENODE_USER=root\nexport HDFS_DATANODE_USER=root\nexport HDFS_SECONDARYNAMENODE_USER=root\nexport YARN_RESOURCEMANAGER_USER=root\nexport YARN_NODEMANAGER_USER=root\n" >> /opt/hadoop/etc/hadoop/hadoop-env.sh \
 && echo "export HADOOP_HOME=/opt/hadoop; export PATH=\$PATH:/opt/hadoop/bin:/opt/hadoop/sbin" >> /root/.bashrc

COPY config/hadoop/ /opt/hadoop/etc/hadoop/
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && mkdir -p /hadoop/dfs/name /hadoop/dfs/data

ENTRYPOINT ["/entrypoint.sh"]
FROM apache/airflow:2.6.0-python3.9

# Cài đặt OpenJDK 11
USER root
RUN apt-get update && apt-get install -y openjdk-11-jdk
# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
ENV PATH "$JAVA_HOME/bin:$PATH"
RUN export JAVA_HOME

RUN apt-get update && apt-get install -y procps


# Chuyển quyền lại cho người dùng airflow
USER airflow

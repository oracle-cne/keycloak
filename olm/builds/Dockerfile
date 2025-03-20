FROM container-registry.oracle.com/os/oraclelinux:8-slim AS ubi-micro-build

ENV KEYCLOAK_VERSION 21.1.2

COPY rpms /tmp/

RUN microdnf install -y tar gzip

# The next step makes it uniform for local development and upstream built.
# If it is a local tar archive then it is unpacked, if from remote is just downloaded.
RUN rpm -i /tmp/*.rpm && \
    mkdir -p /tmp/keycloak && \
    cd /tmp/keycloak && \
    tar -xvf /usr/share/keycloak/keycloak-*.tar.gz

RUN mv /tmp/keycloak/keycloak-* /opt/keycloak && mkdir -p /opt/keycloak/data
RUN chmod -R g+rwX /opt/keycloak

FROM container-registry.oracle.com/os/oraclelinux:8-slim
ENV LANG en_US.UTF-8

COPY --from=ubi-micro-build --chown=1000:0 /opt/keycloak /opt/keycloak

RUN microdnf update -y && \
    microdnf install -y java-17-openjdk-devel && \
    microdnf clean all && \
    echo "keycloak:x:0:root" >> /etc/group && \
    echo "keycloak:x:1000:0:keycloak user:/opt/keycloak:/sbin/nologin" >> /etc/passwd

USER 1000

ENV JAVA_HOME /usr/lib/jvm/java-17-openjdk
ENV PATH /usr/lib/jvm/java-17-openjdk/bin:${PATH}

EXPOSE 8080
EXPOSE 8443

ENTRYPOINT [ "/opt/keycloak/bin/kc.sh" ]

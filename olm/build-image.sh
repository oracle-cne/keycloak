#!/usr/bin/env bash

set -x

wget https://dlcdn.apache.org/maven/maven-3/3.9.9/binaries/apache-maven-3.9.9-bin.tar.gz
tar -xvf apache-maven-3.9.9-bin.tar.gz -C /opt
export M2_HOME=/opt/apache-maven-3.9.9
export PATH=$M2_HOME/bin:$PATH

dnf install java-17-openjdk-devel -y
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-17.0.14.0.7-3.0.1.el8.x86_64

pushd "$(dirname "$0")"/../quarkus

 # build the project for the first time to put required modules of Keycloak into local maven cache in package org.keycloak
mvn --settings ../maven-settings-ocne.xml -f ../pom.xml clean install -DskipTestsuite -DskipExamples -DskipTests  -Denforcer.skip=true

 # build Keycloak Quarkus distribution
mvn --settings ../maven-settings-ocne.xml -f dist/pom.xml clean install
popd

CONTAINER_CLI="${CONTAINER_CLI:-podman}"

name="keycloak"
version="21.1.2"
registry="container-registry.oracle.com/olcne"
docker_tag=${registry}/${name}:${version}

"${CONTAINER_CLI}" build --pull \
    --build-arg https_proxy=${https_proxy} \
    --build-arg istio_version=${version} \
    -t ${docker_tag} -f ./olm/builds/Dockerfile .
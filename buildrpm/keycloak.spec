
%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%ifarch %{arm} arm64 aarch64
%global custom_arch linux-aarch64
%else
%global custom_arch linux-x64
%endif

%global app_name                keycloak
%global app_version             21.1.2
%global oracle_release_version  1
%global _buildhost              build-ol%{?oraclelinux}-%{?_arch}.oracle.com
%global maven_artifacts_version 1.0
%global maven_version           3.9.9

Name:           %{app_name}
Version:        %{app_version}
Release:        %{oracle_release_version}%{?dist}
Summary:        Keycloak provides user federation, strong authentication, user management, fine-grained authorization, and more.
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/keycloak/keycloak
Source:         %{name}-%{version}.tar.bz2
BuildRequires:  maven-artifacts = %{maven_artifacts_version}
BuildRequires:  wget
BuildRequires:  java-17-openjdk-devel
BuildRequires:	nodejs >= 16.20
Patch0:         pom.xml.patch
Patch1:         adapters/oidc/js/pom.xml.patch

%description
Keycloak provides user federation, strong authentication, user management, fine-grained authorization, and more.

%prep
%setup -q -n %{name}-%{version}
%patch0
%patch1

%build
wget https://dlcdn.apache.org/maven/maven-3/3.9.9/binaries/apache-maven-%{maven_version}-bin.tar.gz
tar -xvf apache-maven-%{maven_version}-bin.tar.gz -C /opt

export M2_HOME=/opt/apache-maven-%{maven_version}
export PATH=$M2_HOME/bin:$PATH
mkdir -p ~/.m2/repository
cp -r /maven-artifacts/maven-artifacts-1.0/buildrpm/org ~/.m2/repository
cp -r /maven-artifacts/maven-artifacts-1.0/buildrpm/com ~/.m2/repository
cp olm/settings.xml ~/.m2

export JAVA_HOME=/usr/lib/jvm/java-17-openjdk
export PATH=$JAVA_HOME/bin:$PATH
java --version
mvn --version
node --version
npm version

# change dir to quarkus to do the mvn build
pushd ./quarkus

 # build the project for the first time to put required modules of Keycloak into local maven cache in package org.keycloak
mvn --settings ../olm/maven-settings-ocne.xml -f ../pom.xml clean install -DskipTestsuite -DskipExamples -DskipTests  -Denforcer.skip=true

 # build Keycloak Quarkus distribution
mvn --settings ../olm/maven-settings-ocne.xml -f dist/pom.xml clean install
popd

%install
mkdir -p %{buildroot}%{_datadir}/%{app_name}
cp quarkus/dist/target/*.gz %{buildroot}%{_datadir}/%{app_name}

%files
%{_datadir}/%{app_name}
#%license LICENSE.txt THIRD_PARTY_LICENSES.txt olm/SECURITY.md
#%license LICENSE.txt olm/SECURITY.md

%changelog
* Thu Feb 20 2025 Paul Mackin <paul.mackin@oracle.com> 21.1.2-1
- Initial build creation


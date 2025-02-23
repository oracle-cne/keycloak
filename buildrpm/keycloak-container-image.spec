%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%{!?registry: %global registry container-registry.oracle.com/olcne}
%global app_name               keycloak
%global app_version            21.1.2
%global oracle_release_version 1
%global _buildhost             build-ol%{?oraclelinux}-%{?_arch}.oracle.com

Name:           %{app_name}-container-image
Version:        %{app_version}
Release:        %{oracle_release_version}%{?dist}
Summary:        Keycloak provides user federation, strong authentication, user management, fine-grained authorization, and more.
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/keycloak/keycloak
Source:         %{name}-%{version}.tar.bz2

%description
Keycloak provides user federation, strong authentication, user management, fine-grained authorization, and more.

%prep
%setup -q -n %{name}-%{version}

%build
%global rpm_name %{app_name}-%{version}-%{release}.%{_build_arch}
%global docker_tag %{registry}/%{app_name}:v%{version}

yum clean all
yumdownloader --destdir=${PWD}/rpms %{rpm_name}

docker build --pull \
    --build-arg https_proxy=${https_proxy} \
    -v /etc/yum.repos.d:/etc/yum.repos.d \
    -t %{docker_tag} -f ./olm/builds/Dockerfile .
docker save -o %{app_name}.tar %{docker_tag}

%install
%__install -D -m 644 %{app_name}.tar %{buildroot}/usr/local/share/olcne/%{app_name}.tar

%files
/usr/local/share/olcne/%{app_name}.tar

%changelog
* Thu Feb 20 2025 Paul Mackin <paul.mackin@oracle.com> 21.1.2-1
- Initial build creation

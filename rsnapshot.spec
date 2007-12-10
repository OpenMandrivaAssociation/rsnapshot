%define name rsnapshot
%define version 1.3.0
%define release %mkrel 1

Summary:        Local and remote filesystem snapshot utility
Name:           %{name}
Version:        %{version}
Release:        %{release}
Source0:        %{name}-%{version}.tar.gz
Patch0:		%{name}.patch
License:        GPL
Group:          Archiving/Backup
Url:            http://www.rsnapshot.org
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildArch:      noarch
Requires:	rsync

%description
This is a remote backup program that uses rsync to take backup snapshots of
filesystems.  It uses hard links to save space on disk.
For more details see http://www.rsnapshot.org/.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0

%build
%configure					
%make

%install
install -d $RPM_BUILD_ROOT/%{_bindir}
install -m 755 rsnapshot $RPM_BUILD_ROOT/%{_bindir}/rsnapshot
install -m 755 rsnapshot-diff $RPM_BUILD_ROOT/%{_bindir}/rsnapshot-diff
install -m 755 utils/rsnapreport.pl $RPM_BUILD_ROOT/%{_bindir}/rsnapreport.pl

install -d $RPM_BUILD_ROOT/%{_mandir}/man1
install -m 644 rsnapshot.1 $RPM_BUILD_ROOT/%{_mandir}/man1/

install -d $RPM_BUILD_ROOT/%{_sysconfdir}
install -m 644 rsnapshot.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/rsnapshot.conf.default
install -m 600 rsnapshot.conf.default $RPM_BUILD_ROOT%{_sysconfdir}/rsnapshot.conf

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf $RPM_BUILD_DIR/%{name}-%{version}/

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog README INSTALL TODO
%doc docs/Upgrading_from_1.1 docs/HOWTOs/rsnapshot-HOWTO.en.html
%config %{_sysconfdir}/rsnapshot.conf.default
%config(noreplace) %{_sysconfdir}/rsnapshot.conf
%{_bindir}/rsnapshot
%{_bindir}/rsnapshot-diff
%{_bindir}/rsnapreport.pl
%{_mandir}/man1/rsnapshot.1*

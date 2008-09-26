Summary:	Local and remote filesystem snapshot utility
Name:		rsnapshot
Version:	1.3.1
Release:	%mkrel 2
License:	GPL
Group:		Archiving/Backup
URL:		http://www.rsnapshot.org
Source0:	%{name}-%{version}.tar.gz
Patch0:		%{name}.patch
Patch1:		rsnapshot-ionice.patch
BuildArch:	noarch
BuildRequires:	rsync openssh-clients
Requires:	rsync openssh-clients
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This is a remote backup program that uses rsync to take backup snapshots of
filesystems.  It uses hard links to save space on disk.
For more details see http://www.rsnapshot.org/.

%prep
%setup -q -n %{name}-%{version}
%patch0 -p0
%patch1 -p0

%build
%configure2_5x \
    --sysconfdir=%{buildroot}%{_sysconfdir}

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -m 755 rsnapshot %{buildroot}%{_bindir}/rsnapshot
install -m 755 rsnapshot-diff %{buildroot}%{_bindir}/rsnapshot-diff
install -m 755 utils/rsnapreport.pl %{buildroot}%{_bindir}/rsnapreport.pl

install -d %{buildroot}%{_mandir}/man1
install -m 644 rsnapshot.1 %{buildroot}%{_mandir}/man1/

install -d %{buildroot}%{_sysconfdir}
install -m 644 rsnapshot.conf.default %{buildroot}%{_sysconfdir}/rsnapshot.conf.default
install -m 600 rsnapshot.conf.default %{buildroot}%{_sysconfdir}/rsnapshot.conf

perl -pi -e  's/^#// if /^#cmd_ssh/; s!/path/to/ssh!/usr/bin/ssh!; s!(snapshot_root\s*)/.snapshots/!\1/home/.snapshots/!; s!^#(link_dest\s*)0!${1}1!' %{buildroot}%{_sysconfdir}/rsnapshot.conf

perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_bindir}/rsnapshot

# path fix
find %{buildroot} -type f | xargs perl -pi -e "s|/usr/local|%{_prefix}|g"

%clean
rm -rf %{buildroot}

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

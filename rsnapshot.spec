Summary:	Local and remote filesystem snapshot utility
Name:		rsnapshot
Version:	1.3.1
Release:	18
License:	GPLv2
Group:		Archiving/Backup
Url:		http://www.rsnapshot.org
Source0:	%{name}-%{version}.tar.gz
Patch0:		%{name}.patch
Patch1:		rsnapshot-ionice.patch
Patch2:		rsnapshot-exclude-snapshot_root.patch
Patch3:		pod2man.patch
BuildArch:	noarch
BuildRequires:	rsync openssh-clients
Requires:	rsync openssh-clients

%description
This is a remote backup program that uses rsync to take backup snapshots of
filesystems.  It uses hard links to save space on disk.
For more details see http://www.rsnapshot.org/.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p1

%build
%configure \
	--sysconfdir=%{buildroot}%{_sysconfdir}

%make

%install
install -d %{buildroot}%{_bindir}
install -m 755 rsnapshot %{buildroot}%{_bindir}/rsnapshot
install -m 755 rsnapshot-diff %{buildroot}%{_bindir}/rsnapshot-diff
install -m 755 utils/rsnapreport.pl %{buildroot}%{_bindir}/rsnapreport.pl

install -d %{buildroot}%{_datadir}/rsnapshot
mv utils/rsnapshotdb rsnapshotdb
mv utils/README README.utils
mv rsnapshotdb/CHANGES.txt rsnapshotdb/rsnapshotDB.CHANGES.txt
mv rsnapshotdb/TODO.txt rsnapshotdb/rsnapshotDB.TODO.txt
install -m 755 utils/* %{buildroot}%{_datadir}/rsnapshot
install -m 755 rsnapshotdb/rsnapshotDB.pl %{buildroot}%{_bindir}/rsnapshotDB

install -d %{buildroot}%{_mandir}/man1
install -m 644 rsnapshot.1 %{buildroot}%{_mandir}/man1/
install -m 644 rsnapshot-diff.1 %{buildroot}%{_mandir}/man1/

install -d %{buildroot}%{_sysconfdir}
install -m 644 rsnapshot.conf.default %{buildroot}%{_sysconfdir}/rsnapshot.conf.default
install -m 600 rsnapshot.conf.default %{buildroot}%{_sysconfdir}/rsnapshot.conf
install -m 600 rsnapshotdb/rsnapshotDB.conf.sample %{buildroot}%{_sysconfdir}/rsnapshotDB.conf
install -m 644 rsnapshotdb/rsnapshotDB.xsd %{buildroot}%{_sysconfdir}/rsnapshotDB.xsd

perl -pi -e  's/^#// if /^#cmd_ssh/; s!/path/to/ssh!/usr/bin/ssh!; s!(snapshot_root\s*)/.snapshots/!#\1/home/.snapshots/!; s!^#(link_dest\s*)0!${1}1!' %{buildroot}%{_sysconfdir}/rsnapshot.conf

perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_bindir}/rsnapshot

# path fix
find %{buildroot} -type f | xargs perl -pi -e "s|/usr/local|%{_prefix}|g"

#Remove unnessesary files
rm -f %{_datadir}/rsnapreport.pl
rm -f %{_datadir}/sign_packages.sh
rm -f %{_datadir}/rsnapshot_if_mounted.sh

%files
%doc AUTHORS ChangeLog README INSTALL TODO README.utils
%doc docs/Upgrading_from_1.1 docs/HOWTOs/rsnapshot-HOWTO.en.html
%doc rsnapshotdb/rsnapshotDB.CHANGES.txt rsnapshotdb/rsnapshotDB.TODO.txt 
%doc rsnapshotdb/rsnapshotDB.conf.sample
%config %{_sysconfdir}/rsnapshot.conf.default
%config(noreplace) %{_sysconfdir}/rsnapshot.conf
%config(noreplace) %{_sysconfdir}/rsnapshotDB.conf
%config %{_sysconfdir}/rsnapshotDB.xsd
%{_bindir}/rsnapshot
%{_bindir}/rsnapshot-diff
%{_bindir}/rsnapreport.pl
%{_bindir}/rsnapshotDB
%{_datadir}/rsnapshot
%{_mandir}/man1/rsnapshot.1*
%{_mandir}/man1/rsnapshot-diff.1*


Summary:	Local and remote filesystem snapshot utility
Name:		rsnapshot
Version:	1.3.1
Release:	12
License:	GPL
Group:		Archiving/Backup
URL:		http://www.rsnapshot.org
Source0:	%{name}-%{version}.tar.gz
Patch0:		%{name}.patch
Patch1:		rsnapshot-ionice.patch
Patch2:		rsnapshot-exclude-snapshot_root.patch
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
%patch2 -p0

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
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



%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-8mdv2011.0
+ Revision: 669451
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 1.3.1-7mdv2011.0
+ Revision: 607378
- rebuild

* Sun Jun 06 2010 Colin Guthrie <cguthrie@mandriva.org> 1.3.1-6mdv2010.1
+ Revision: 547158
- Bump release to ensure version is > 2010.0 update version

* Wed Jan 13 2010 Lonyai Gergely <aleph@mandriva.org> 1.3.1-5mdv2010.1
+ Revision: 490746
- fix: #45979 - Rsnapshot exclude to prevent backup of snapshots is too broad
  Add tools from utils dir
  Add rsnapshotDB tool

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 1.3.1-5mdv2010.0
+ Revision: 426963
- rebuild

* Sat Mar 07 2009 Antoine Ginies <aginies@mandriva.com> 1.3.1-4mdv2009.1
+ Revision: 351546
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - no default place, we use HAL to get proper place (#39802)

* Fri Sep 26 2008 Thierry Vignaud <tv@mandriva.org> 1.3.1-2mdv2009.0
+ Revision: 288663
- be nice(1) with other programs when backuping

* Mon Sep 08 2008 Frederic Crozat <fcrozat@mandriva.com> 1.3.1-1mdv2009.0
+ Revision: 282674
- Release 1.3.1

* Fri Aug 01 2008 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-6mdv2009.0
+ Revision: 259829
- fix weird build error and other stuff

* Tue Jun 24 2008 Thierry Vignaud <tv@mandriva.org> 1.3.0-5mdv2009.0
+ Revision: 228591
- patch 1: run with low I/O priority

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 1.3.0-4mdv2009.0
+ Revision: 225336
- rebuild

* Wed Jan 23 2008 Thierry Vignaud <tv@mandriva.org> 1.3.0-3mdv2008.1
+ Revision: 157029
- fix ssh path

* Tue Jan 08 2008 Thierry Vignaud <tv@mandriva.org> 1.3.0-2mdv2008.1
+ Revision: 146488
- enable ssh support
- enable link_dest support in rsync
- do snapshots in /home/.snapshots instead of /.snapshots/ (the odds're higher
  there's more space)
- fix %%clean so that it is --short-circuit aware
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 10 2007 Anne Nicolas <ennael@mandriva.org> 1.3.0-1mdv2008.1
+ Revision: 116960
- Fix build require
- Fix group name
- import rsnapshot



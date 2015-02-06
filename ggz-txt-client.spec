%define name    ggz-txt-client
%define version 0.0.14.1
%define release 7

%define libggz_version %{version}
%define ggz_client_libs_version %{version}

%define games_list tttxt

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	GGZ Text Mode Client
License:	GPL
Group:		Games/Other
URL:		http://ggzgamingzone.org/
Source0:	http://ftp.ggzgamingzone.org/pub/ggz/%{version}/%{name}-%{version}.tar.bz2
BuildRequires:	libggz-devel = %{libggz_version}
BuildRequires:	ggz-client-libs-devel = %{ggz_client_libs_version}
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
Requires:	libggz = %{libggz_version}
Requires:	ggz-client-libs = %{ggz_client_libs_version}
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
The official GGZ Gaming Zone client for text mode, suitable for
environment where no graphical desktop is available.

It also includes the following text mode GGZ game(s):
    TicTacToe

%prep
%setup -q

%build
%configure2_5x  \
    --bindir=%{_gamesbindir} \
    --with-libggz-libraries=%{_libdir} \
    --with-ggzmod-libraries=%{_libdir} \
    --with-ggzcore-libraries=%{_libdir}
%make

%install
rm -rf %{buildroot}
%makeinstall_std

rm %{buildroot}%{_sysconfdir}/ggz.modules
rmdir %{buildroot}%{_sysconfdir}

# Get a copy of all of our .dsc files
mkdir -p %{buildroot}%{_datadir}/ggz/ggz-config
for i in %games_list; do
  install -m 0644 $i/module.dsc %{buildroot}%{_datadir}/ggz/ggz-config/txt-$i.dsc
done

cat > README.mdv <<EOF
Notes:

Currently GGZ text client document is almost non-existant. You have to
look at the source to understand how to use it. Here are a few simple
instructions (though I still can't launch any playable game yet):

1. In command line, type

	ggz-txt ggz://username:password@live.ggzgamingzone.org

   You should substitute username and password appropriately, as what
   you would do when launching URI that requires username and password.
   No trailing slash!

2. Inside client, type '/help' for help message. Good luck :-)
EOF

%find_lang ggz-txt

%clean
rm -rf %{buildroot}

%post
# Run ggz-config vs. all installed games
if [ -f %{_sysconfdir}/ggz.modules ]; then
  for i in %games_list; do
    ggz-config --install --modfile=%{_datadir}/ggz/ggz-config/txt-$i.dsc --force
  done
fi

%preun
# Run ggz-config to uninstall all the games
if [ "$1" = "0" ]; then
  if [ -f %{_sysconfdir}/ggz.modules ]; then
    for i in %games_list; do
      ggz-config --remove --modfile=%{_datadir}/ggz/ggz-config/txt-$i.dsc
    done
  fi
fi

%files -f ggz-txt.lang
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README README.GGZ README.mdv 
%doc TODO QuickStart.GGZ
%{_gamesbindir}/ggz-txt
%{_mandir}/man?/*
%{_libdir}/ggz/*
%{_datadir}/ggz/ggz-config/*.dsc
%{_datadir}/applications/*




%changelog
* Thu Dec 09 2010 Oden Eriksson <oeriksson@mandriva.com> 0.0.14.1-6mdv2011.0
+ Revision: 618454
- the mass rebuild of 2010.0 packages

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.0.14.1-5mdv2010.0
+ Revision: 437674
- rebuild

* Sun Mar 15 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.0.14.1-4mdv2009.1
+ Revision: 355323
- drop readline detection patch, uneeded anymore
- rename README.mdk to README.mdv, and use herein document for it

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.0.14.1-3mdv2009.0
+ Revision: 246056
- rebuild

* Tue Feb 26 2008 Emmanuel Andry <eandry@mandriva.org> 0.0.14.1-1mdv2008.1
+ Revision: 175532
- New version

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Jul 16 2007 Emmanuel Andry <eandry@mandriva.org> 0.0.14-2mdv2008.0
+ Revision: 52725
- rebuild with latest autotools


* Sat Feb 10 2007 Emmanuel Andry <eandry@mandriva.org> 0.0.14-1mdv2007.0
+ Revision: 118738
- New version 0.0.14
- bunzipped patch
- Import ggz-txt-client

* Sun Sep 03 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.13-2mdv2007.0
- fix spec file's extension
- fix x86_64 build

* Mon May 22 2006 Emmanuel Andry <eandry@mandriva.org> 0.0.13-1mdk
- 0.0.13
- mkrel
- drop patch 1

* Tue Feb 08 2005 Abel Cheung <deaddog@mandrake.org> 0.0.9-2mdk
- rebuild against new readline

* Sat Nov 27 2004 Abel Cheung <deaddog@mandrake.org> 0.0.9-1mdk
- New version
- P1: Temporary hack to fix DESTDIR support in older gettext
- Now it includes a tictactoe game module (Doh)
- Include README to tell people how to connect to server.
  (fail to find any document about text client so far) But don't expect
  too much, I can't input any text into the only one available game


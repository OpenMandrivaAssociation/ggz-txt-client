%define name    ggz-txt-client
%define version 0.0.14
%define release %mkrel 1

%define libggz_version %{version}
%define ggz_client_libs_version %{version}

%define games_list tttxt

Name:		%{name}
Summary:	GGZ Text Mode Client
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Games/Other
URL:		http://ggzgamingzone.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source0:	http://ftp.ggzgamingzone.org/pub/ggz/%{version}/%{name}-%{version}.tar.bz2
Source1:	ggz-txt-client-README.mdk
Patch0:		%{name}-0.0.7-readline.patch
BuildRequires:	libggz-devel = %{libggz_version}
BuildRequires:	ggz-client-libs-devel = %{ggz_client_libs_version}
BuildRequires:	readline-devel
BuildRequires:	ncurses-devel
BuildRequires:	automake1.7
Requires:	libggz = %{libggz_version}
Requires:	ggz-client-libs = %{ggz_client_libs_version}
# (Abel) 0.0.9-1mdk don't need game modules, the only game module
# supporting txt client is also bundled here

%description
The official GGZ Gaming Zone client for text mode, suitable for
environment where no graphical desktop is available.

It also includes the following text mode GGZ game(s):
    TicTacToe

%prep
%setup -q
%patch0 -p1 -b .readline

cp %{SOURCE1} README.mdk

# needed by patch0
AUTOMAKE=automake-1.7 ACLOCAL=aclocal-1.7 autoreconf --force --install

%build
%configure2_5x --bindir=%{_gamesbindir} --with-libggz-libraries=%{_libdir} --with-ggzmod-libraries=%{_libdir} --with-ggzcore-libraries=%{_libdir}
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
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README README.GGZ README.mdk TODO QuickStart.GGZ
%{_gamesbindir}/ggz-txt
%{_mandir}/man?/*
%{_libdir}/ggz/*
%{_datadir}/ggz/ggz-config/*.dsc
%{_datadir}/applications/*



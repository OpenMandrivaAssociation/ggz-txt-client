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
BuildRequires:	pkgconfig(ncurses)
Requires:	libggz = %{libggz_version}
Requires:	ggz-client-libs = %{ggz_client_libs_version}

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


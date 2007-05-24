%define name glame
%define version 2.0.2
%define cvs 20070523
%if %cvs
%define release %mkrel 0.%cvs.1
%else
%define release %mkrel 6
%endif
%define build_plf 0
%{?_with_plf: %{expand: %%global build_plf 1}}
%if %build_plf
%define distsuffix plf
%endif

Summary:   	A sound editor
Name:      	%{name}
Version:   	%{version}
Release:   	%{release}
License: 	GPL
Group:     	Sound
%if %cvs
Source0:	%{name}-%{cvs}.tar.bz2
%else
Source0:   	http://prdownloads.sourceforge.net/glame/%{name}-%{version}.tar.bz2
%endif
Source1:      	%{name}-48x48.png
Source2:      	%{name}-32x32.png
Source3:      	%{name}-16x16.png
Patch: glame-2.0.1-xdg.patch
URL:       	http://glame.sourceforge.net/ 
Buildroot: 	%{_tmppath}/%{name}-buildroot
BuildRequires: 	libgnomeui2-devel
BuildRequires: 	libglade2.0-devel
BuildRequires: 	guile-devel >= 1.6
BuildRequires: 	fftw2-devel 
BuildRequires: 	ladspa-devel
BuildRequires: 	libmad-devel
BuildRequires: 	libvorbis-devel
BuildRequires:	libltdl-devel
#gw, that's for /usr/X11R6/include/X11/bitmaps/hlines3 :
BuildRequires:  x11-data-bitmaps
BuildRequires:	gettext-devel
# autogen.sh requires cvs binary for some weird reason.
%if %cvs
BuildRequires:	cvs
%endif

%description
GLAME is meant to be the GIMP of audio processing. It is designed to be
a powerful, fast, stable, and easily extensible sound editor for Linux
and compatible systems. Supported platforms are Linux and IRIX. 

%if %build_plf
This package is in PLF as it might violate some patents.

%package lame
Group: Sound
Summary: MP3 plugin for glame
BuildRequires: liblame-devel
Requires: %name = %version

%description lame
GLAME is meant to be the GIMP of audio processing. It is designed to be
a powerful, fast, stable, and easily extensible sound editor for Linux
and compatible systems. Supported platforms are Linux and IRIX. 

This is the MP3 encoding plugin for glame based on lame. It is in PLF
for patent reasons.
%endif

%prep
rm -rf $RPM_BUILD_ROOT

%if %cvs
%setup -q -n %{name}
%else
%setup -q
%endif
%patch -p1

%build
%if %cvs
./autogen.sh
%endif
# --enable-maintainer-mode appears to be needed to generate version.texi...
./configure --prefix=%_prefix --libdir=%_libdir --enable-maintainer-mode
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

(cd $RPM_BUILD_ROOT
mkdir -p .%{_menudir}
cat > .%{_menudir}/%{name} <<EOF
?package(%{name}):\
command="%{_bindir}/glame"\
title="Glame"\
longtitle="An audio processing tool"\
needs="x11"\
section="Multimedia/Sound"\
icon="%{name}.png" xdg="true"
EOF
)
mv %buildroot%{_datadir}/gnome/apps/Multimedia/ %buildroot%{_datadir}/applications
# install icons
mkdir -p $RPM_BUILD_ROOT{%{_liconsdir},%{_miconsdir},%{_iconsdir}}
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
cp %{SOURCE1} $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
cp %{SOURCE1} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png
cp %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
cp %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/%{name}.png
cp %{SOURCE3} $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png
cp %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%{find_lang} %{name}
#clean unpackaged files
rm -f %buildroot%_libdir/glame/*a

%post
/sbin/install-info %{_infodir}/glame.info.bz2 %{_infodir}/dir
/sbin/install-info %{_infodir}/glame-dev.info.bz2 %{_infodir}/dir
%{update_menus}
%update_icon_cache hicolor

%postun
/sbin/install-info --delete %{_infodir}/glame.info.bz2 %{_infodir}/dir
/sbin/install-info --delete %{_infodir}/glame-dev.info.bz2 %{_infodir}/dir
%{clean_menus}
%clean_icon_cache hicolor

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr (-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%{_bindir}/*
%{_libdir}/glame/
%{_datadir}/applications/glame.desktop
%{_datadir}/%{name}/
%{_infodir}/*
%{_menudir}/*
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png

%if %build_plf
%files lame
%defattr (-,root,root)
%{_libdir}/glame/file_mp3_out.so
%endif



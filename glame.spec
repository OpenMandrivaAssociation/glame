%define name	glame
%define version	2.0.2
%define cvs	0
%define pre	rc1
%define date	20070607
%if %cvs
%define release %mkrel 0.%cvs.2
%else
%if %pre
%define release	%mkrel 0.%date.%pre.3
%else
%define release %mkrel 1
%endif
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
License: 	GPLv2+
Group:     	Sound
%if %cvs
Source0:	%{name}-%{cvs}.tar.bz2
%else
Source0:   	http://prdownloads.sourceforge.net/glame/%{name}-%{version}-%{pre}.tar.gz
%endif
Source1:      	%{name}-48x48.png
Source2:      	%{name}-32x32.png
Source3:      	%{name}-16x16.png
Patch:		glame-2.0.1-xdg.patch
Patch1:		glame-2.0.2-rc1-format-strings.patch
URL:       	http://glame.sourceforge.net/ 
Buildroot: 	%{_tmppath}/%{name}-buildroot
BuildRequires: 	libgnomeui2-devel
BuildRequires: 	libglade2.0-devel
BuildRequires: 	guile-devel >= 1.6
BuildRequires: 	fftw2-devel 
BuildRequires: 	ladspa-devel
BuildRequires: 	libmad-devel
BuildRequires: 	libvorbis-devel
BuildRequires: 	libalsa-devel
BuildRequires:	libltdl-devel
#gw, that's for /usr/X11R6/include/X11/bitmaps/hlines3 :
BuildRequires:  x11-data-bitmaps
BuildRequires:	gettext-devel
# autogen.sh requires cvs binary for some weird reason.
%if %cvs
BuildRequires:	cvs
%endif
BuildRequires:	texinfo
%if %build_plf
Provides: glame-lame
Obsoletes: glame-lame
BuildRequires: liblame-devel
%endif

%description
GLAME is meant to be the GIMP of audio processing. It is designed to be
a powerful, fast, stable, and easily extensible sound editor for Linux
and compatible systems. Supported platforms are Linux and IRIX. 

%if %build_plf
This package is in PLF as it might violate some patents.
%endif


%prep
rm -rf $RPM_BUILD_ROOT

%if %cvs
%setup -q -n %{name}
%else
%if %pre
%setup -q -n %{name}-%{version}-%{pre}
%else
%setup -q
%endif
%endif
%patch -p1
%patch1 -p1
%if %cvs
./autogen.sh
%endif

%build
# --enable-maintainer-mode appears to be needed to generate version.texi...
%configure2_5x --enable-maintainer-mode
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

mv %buildroot%{_datadir}/gnome/apps/Multimedia/ %buildroot%{_datadir}/applications

# install icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{48x48,32x32,16x16}/apps
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/%{name}.png
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/%{name}.png

#clean unpackaged files
rm -f %buildroot%_libdir/glame/*a

%{find_lang} %{name}

%post
%_install_info %name
%_install_info glame-dev
%if %mdkversion < 200900
%{update_menus}
%{update_icon_cache hicolor}
%endif

%postun
%_remove_install_info %name
%_remove_install_info glame-dev
%if %mdkversion < 200900
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr (-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README TODO
%{_bindir}/*
%dir %{_libdir}/glame/
%{_libdir}/glame/audio_io_alsa.so
%{_libdir}/glame/audio_io_esd.so
%{_libdir}/glame/audio_io_oss.so
%{_libdir}/glame/debug.so
%{_libdir}/glame/fft_plugins.so
%{_libdir}/glame/file_oggvorbis_out.so
%{_libdir}/glame/mixer.so
%{_libdir}/glame/normalize.so
%{_libdir}/glame/resample.so
%{_libdir}/glame/tutorial.so
%if %build_plf
%{_libdir}/glame/file_mp3_out.so
%endif
%{_datadir}/applications/glame.desktop
%{_datadir}/%{name}/
%{_infodir}/*
%{_iconsdir}/hicolor/48x48/apps/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png



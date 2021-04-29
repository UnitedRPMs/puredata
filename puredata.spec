%global commit0 eeef4ba9130d3182146927c37fa57d61bbff0f0b
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%define _legacy_common_support 1
%global _lto_cflags %{nil}

Name:          puredata
Version:       0.51.4
Release:       1%{?dist}
Summary:       A real-time graphical programming environment for media processing
Group:         Applications/Multimedia
URL:           http://puredata.info
Source:        https://github.com/pure-data/pure-data/archive/%{commit0}.tar.gz#/%{name}-%{version}.tar.gz
Patch:         lib_fix.patch
Source1:       %{name}.png
License:       BSD
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc-c++
BuildRequires: libtool
BuildRequires: alsa-lib-devel
BuildRequires: portaudio-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: portmidi-devel
BuildRequires: fftw-devel
BuildRequires: tcl-devel
BuildRequires: tk-devel
Provides: pd = %{version}-%{release}

%description
PD (aka Pure Data) is a real-time graphical programming environment for audio,
video, and graphical processing. It is the third major branch of the family 
of patcher programming languages known as Max (Max/FTS, ISPW Max, Max/MSP, 
jMax, etc.) originally developed by Miller Puckette and company at IRCAM. 
The core of Pd is written and maintained by Miller Puckette and includes 
the work of many developers, making the whole package very much a community effort.

%package devel
Summary: Development package for puredata
Requires: %{name} = %{version}-%{release}

%description devel
puredata development header files and libraries.


%prep
%setup -n pure-data-%{commit0}
%ifarch x86_64
%patch -p1
%endif

%build
autoreconf -vfi

%configure --enable-alsa \
              --enable-jack \
              --enable-portaudio \
              --enable-portmidi \
              --without-local-portaudio \
              --without-local-portmidi \
              --enable-fftw \
              --without-local-portaudio
make

%install

%makeinstall MANINSTDIR=%{buildroot}/%{_mandir}

install -dm 755 %{buildroot}/%{_datadir}/applications \
          %{buildroot}/%{_datadir}/pixmaps

install -m644 %{S:1} %{buildroot}/%{_datadir}/pixmaps/

cat > %{buildroot}/%{_datadir}/applications/puredata.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Type=Application
Name=PureData
GenericName=Sound Editor
Comment=Synth
Icon=puredata
Exec=pd
Terminal=false
Categories=Audio;AudioVideo;Midi;X-Alsa;X-Jack;GTK;
EOF

# fix broken symlink
rm -fv %{buildroot}/%{_libdir}/pd/bin/pd
ln -sfv /usr/bin/pd %{buildroot}/%{_libdir}/pd/bin/pd

%files
%{_bindir}/pd
%{_bindir}/pd-gui
%{_bindir}/pdreceive
%{_bindir}/pdsend
%{_libdir}/pd/
%{_datadir}/applications/puredata.desktop
%{_mandir}/man1/pd.1.gz
%{_mandir}/man1/pdreceive.1.gz
%{_mandir}/man1/pdsend.1.gz
%{_datadir}/pixmaps/%{name}.png
%exclude %{_libdir}/pd/doc/6.externs/dspobj~.c
%exclude %{_libdir}/pd/doc/6.externs/obj1.c
%exclude %{_libdir}/pd/doc/6.externs/obj2.c
%exclude %{_libdir}/pd/doc/6.externs/obj3.c
%exclude %{_libdir}/pd/doc/6.externs/obj4.c
%exclude %{_libdir}/pd/doc/6.externs/obj5.c

%files devel
%{_includedir}/m_pd.h
%{_includedir}/pd/
%{_libdir}/pkgconfig/pd.pc
%{_libdir}/pd/doc/6.externs/dspobj~.c
%{_libdir}/pd/doc/6.externs/obj1.c
%{_libdir}/pd/doc/6.externs/obj2.c
%{_libdir}/pd/doc/6.externs/obj3.c
%{_libdir}/pd/doc/6.externs/obj4.c
%{_libdir}/pd/doc/6.externs/obj5.c

%changelog

* Mon Apr 26 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.51.4-1  
- Updated to 0.51.4

* Thu Sep 24 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.51.2-1  
- Updated to 0.51.2

* Mon Aug 31 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.51.1-1  
- Updated to 0.51.1

* Thu Jun 11 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.51.0-1  
- Updated to 0.51.0

* Tue Oct 08 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.50.2-1  
- Updated to 0.50.2

* Wed Aug 21 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.50.0-1  
- Updated to 0.50.0

* Wed Sep 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.49.0-1  
- Updated to 0.49.0

* Wed May 23 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.48.2-1  
- Updated to 0.48.2

* Wed May 23 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.48.1-2  
- Updated to current commit

* Tue May 22 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.48.1-1  
- Updated to 0.48.1

* Thu May 17 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 0.48-1  
- Initial build

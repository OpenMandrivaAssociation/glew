# glew is used by mesa-demos - and we want 32-bit glxinfo for debugging
%ifarch %{x86_64}
%bcond_without compat32
%endif

%define	major	2.2
%define	libname	%mklibname %{name} %{major}
#define	libmx	%mklibname %{name}mx %{major}
%define	devname	%mklibname %{name} -d
%define lib32name %mklib32name %{name} %{major}
%define dev32name %mklib32name %{name} -d
%define _disable_lto 1

Summary:	The OpenGL Extension Wrangler Library
Name:		glew
Version:	2.2.0
Release:	2
Group:		Development/C
License:	BSD and MIT
Url:		http://glew.sourceforge.net
Source0:	http://downloads.sourceforge.net/glew/%{name}-%{version}.tgz
Patch0:		glew-2.0.0-pkgconfig.patch

BuildRequires:	make
BuildRequires:	file
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xmu)

%if %{with compat32}
BuildRequires:	devel(libGLU)
BuildRequires:	devel(libX11)
BuildRequires:	devel(libXi)
BuildRequires:	devel(libXmu)
BuildRequires:	devel(libxcb)
BuildRequires:	devel(libXau)
BuildRequires:	devel(libXdmcp)
BuildRequires:	devel(libGL)
BUildRequires:	devel(libGLdispatch)
%endif

%description
The goal of the OpenGL Extension Wrangler Library (GLEW) is to assist C/C++
OpenGL developers with two tedious tasks: initializing and using extensions
and writing portable applications. GLEW provides an efficient run-time
mechanism to determine whether a certain extension is supported by the
driver or not. OpenGL core and extension functionality is exposed via a
single header file. GLEW currently supports a variety of platforms and
operating systems, including Windows, Linux, Darwin, Irix, and Solaris. 

%package -n %{libname}
Summary:	GLEW library
Group:		System/Libraries

%description -n %{libname}
This package contains a shared library for %{name}.

# Support for GLEWmx is dropped since GLEW 2.0 (Penguin) https://github.com/arrayfire/arrayfire/issues/1515
#package -n %{libmx}
#Summary:	GLEW library
#Group:		System/Libraries
#Conflicts:	%{_lib}glew1.9 < 1.9.0-3

#description -n %{libmx}
#This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Development files for using the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
#Requires:	%{libmx} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Development files for using the %{name} library.

%if %{with compat32}
%package -n %{lib32name}
Summary:	GLEW library (32-bit)
Group:		System/Libraries

%description -n %{lib32name}
This package contains a shared library for %{name}.

%package -n %{dev32name}
Summary:	Development files for using the %{name} library (32-bit)
Group:		Development/C
Requires:	%{devname} = %{version}-%{release}
Requires:	%{lib32name} = %{version}-%{release}

%description -n %{dev32name}
Development files for using the %{name} library.
%endif

%prep
%autosetup -p1

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

sed -i -e "s#-shared -soname#-shared -lc -soname#g" config/Makefile.linux

#fix txt/doc files permissions
chmod 0755 doc
chmod 0644 doc/* README.md

sed -i 's|cc|%{__cc}|g' config/Makefile.linux

%if %{with compat32}
mkdir -p build32
cp -a $(ls -1 |grep -v build32) build32/
%endif

%build
%before_configure
%if %{with compat32}
%make_build -C build32 CC="%{_bindir}/gcc -m32" LD="%{_bindir}/gcc -m32" CFLAGS.EXTRA="$(echo %{optflags} |sed -e 's,-m64,,g;s,-flto,,g') -fPIC -m32" STRIP= libdir=%{_prefix}/lib bindir=%{_bindir} includedir=%{_includedir} ARCH64=false LDFLAGS.EXTRA=""
%endif
%make_build CFLAGS.EXTRA="%{optflags} -fPIC -flto" STRIP= libdir=%{_libdir} bindir=%{_bindir} includedir=%{_includedir}

%install
%if %{with compat32}
make -C build32 install.all DESTDIR="%{buildroot}" CC="%{_bindir}/gcc -m32" LD="%{_bindir}/gcc -m32" LIBDIR=%{_prefix}/lib bindir=%{_bindir} includedir=%{_includedir}
rm -f %{buildroot}%{_prefix}/lib/*.a
%endif
make install.all DESTDIR="%{buildroot}" LIBDIR=%{_libdir} bindir=%{_bindir} includedir=%{_includedir}
rm -f %{buildroot}%{_libdir}/*.a

chmod 0755 %{buildroot}%{_libdir}/*.so*

%files
%doc README.md doc
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libGLEW.so.%{major}*

#files -n %{libmx}
#{_libdir}/libGLEWmx.so.%{major}*

%files -n %{devname}
%{_includedir}/GL/*.h
%{_libdir}/libGLEW*.so
%{_libdir}/pkgconfig/%{name}.pc

%if %{with compat32}
%files -n %{lib32name}
%{_prefix}/lib/libGLEW.so.%{major}*

%files -n %{dev32name}
%{_prefix}/lib/libGLEW*.so
%{_prefix}/lib/pkgconfig/%{name}.pc
%endif

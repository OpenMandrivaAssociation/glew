%define	major	1.10
%define	libname	%mklibname %{name} %{major}
%define	libmx	%mklibname %{name}mx %{major}
%define	devname	%mklibname %{name} -d

Summary:	The OpenGL Extension Wrangler Library
Name:		glew
Version:	1.10.0
Release:	4
Group:		Development/C
License:	BSD and MIT
Url:		http://glew.sourceforge.net
Source0:	http://downloads.sourceforge.net/glew/%{name}-%{version}.tgz

BuildRequires:	file
BuildRequires:	pkgconfig(glu)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xmu)

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

%package -n %{libmx}
Summary:	GLEW library
Group:		System/Libraries
Conflicts:	%{_lib}glew1.9 < 1.9.0-3

%description -n %{libmx}
This package contains a shared library for %{name}.

%package -n %{devname}
Summary:	Development files for using the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Requires:	%{libmx} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
Development files for using the %{name} library.

%prep
%setup -q

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

sed -i -e "s#-shared -soname#-shared -lc -soname#g" config/Makefile.linux

#fix txt/doc files permissions
chmod 0755 doc
chmod 0644 doc/* README.txt

%build
%make CFLAGS.EXTRA="%{optflags} -fPIC" GLEW_DEST= STRIP= libdir=%{_libdir} bindir=%{_bindir} includedir=%{_includedir}

%install
make install.all GLEW_DEST="%{buildroot}%{_usr}" bindir=%{buildroot}%{_bindir} libdir=%{buildroot}%{_libdir} includedir=%{buildroot}%{_includedir}/GL
rm -f %{buildroot}%{_libdir}/*.a

chmod 0755 %{buildroot}%{_libdir}/*.so*

%files
%doc README.txt doc
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libGLEW.so.%{major}*

%files -n %{libmx}
%{_libdir}/libGLEWmx.so.%{major}*

%files -n %{devname}
%{_includedir}/GL/*.h
%{_libdir}/libGLEW*.so
%{_libdir}/pkgconfig/*.pc


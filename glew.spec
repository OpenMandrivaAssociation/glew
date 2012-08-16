%define	major 1.9
%define	libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	The OpenGL Extension Wrangler Library
Name:		glew
Version:	1.9.0
Release:	%mkrel 1
Group:		Development/C
License:	BSD and MIT
URL:		http://glew.sourceforge.net
Source0:	http://downloads.sourceforge.net/glew/%{name}-%{version}.tgz
BuildRequires:	libx11-devel
BuildRequires:	mesaglu-devel
BuildRequires:	libxi-devel libxmu-devel
BuildRequires:	file

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
The goal of the OpenGL Extension Wrangler Library (GLEW) is to assist C/C++
OpenGL developers with two tedious tasks: initializing and using extensions
and writing portable applications. GLEW provides an efficient run-time
mechanism to determine whether a certain extension is supported by the
driver or not. OpenGL core and extension functionality is exposed via a
single header file. GLEW currently supports a variety of platforms and
operating systems, including Windows, Linux, Darwin, Irix, and Solaris.


%package -n %{develname}
Summary:	Development files for using the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1.3 -d
Provides:	%mklibname %{name} 1.3 -d

%description -n	%{develname}
Development files for using the %{name} library.


%prep

%setup -q

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

perl -pi -e "s#-shared -soname#-shared -lc -soname#g" config/Makefile.linux

#fix txt/doc files permissions
chmod 0755 doc
chmod 0644 doc/* README.txt

%build
%make CFLAGS.EXTRA="%{optflags} -fPIC" GLEW_DEST= libdir=%{_libdir} bindir=%{_bindir} includedir=%{_includedir}

%install
make install.all GLEW_DEST="%{buildroot}%{_usr}" bindir=%{buildroot}%{_bindir} libdir=%{buildroot}%{_libdir} includedir=%{buildroot}%{_includedir}/GL
rm -f %{buildroot}%{_libdir}/*.a

chmod 0755 %{buildroot}%{_libdir}/*.so*

%files
%doc README.txt doc
%{_bindir}/*

%files -n %{libname}
%{_libdir}/libGLEW*.so.%{major}*

%files -n %{develname}
%{_includedir}/GL/*.h
%{_libdir}/libGLEW*.so
%{_libdir}/pkgconfig/*.pc

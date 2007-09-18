%define	name	glew
%define	version	1.3.4
%define	release	%mkrel 4
%define	major	1.3
%define	libname	%mklibname %{name} %{major}

%define _requires_exceptions devel(/lib/libNoVersion)

Summary:	The OpenGL Extension Wrangler Library
Name:		%{name}
Version:	%{version}
Release:	%{release}
Group:		Development/C
License:	BSD
URL:		http://www.sourceforge.net/projects/glew/
Source0:	%{name}-%{version}-src.tar.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	X11-devel MesaGLU-devel

%description
The goal of the OpenGL Extension Wrangler Library (GLEW) is to assist C/C++
OpenGL developers with two tedious tasks: initializing and using extensions
and writing portable applications. GLEW provides an efficient run-time
mechanism to determine whether a certain extension is supported by the
driver or not. OpenGL core and extension functionality is exposed via a
single header file. GLEW currently supports a variety of platforms and
operating systems, including Windows, Linux, Darwin, Irix, and Solaris. 

%package -n	%{libname}
Summary:	GLEW library
Group:		System/Libraries

%description -n	%{libname}
The goal of the OpenGL Extension Wrangler Library (GLEW) is to assist C/C++
OpenGL developers with two tedious tasks: initializing and using extensions
and writing portable applications. GLEW provides an efficient run-time
mechanism to determine whether a certain extension is supported by the
driver or not. OpenGL core and extension functionality is exposed via a
single header file. GLEW currently supports a variety of platforms and
operating systems, including Windows, Linux, Darwin, Irix, and Solaris.


%package -n	%{libname}-devel
Summary:	Development files for using the %{name} library
Group:		Development/C
Requires:	%{libname} = %{version}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

%description -n	%{libname}-devel
Development files for using the %{name} library

%prep
%setup -q -n %{name}
perl -pi -e "s#-shared -soname#-shared -lc -soname#g" config/Makefile.linux

%build
make CFLAGS.EXTRA="$RPM_OPT_FLAGS -fPIC"

%install
rm -rf %{buildroot}
%makeinstall GLEW_DEST=%{buildroot}%{_prefix} LIBDIR=%{buildroot}%{_libdir} BINDIR=%{_bindir} includedir=%{_includedir}

%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt doc
%defattr(-,root,root)
%{_bindir}/glewinfo
%{_bindir}/visualinfo

%files -n %{libname}
%{_libdir}/libGLEW.so.%{major}*

%files -n %{libname}-devel
%{_includedir}/GL/*.h
%{_libdir}/libGLEW.a
%{_libdir}/libGLEW.so

%define	major 1.5
%define	libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	The OpenGL Extension Wrangler Library
Name:		glew
Version:	1.5.7
Release:	%mkrel 2
Group:		Development/C
License:	BSD
URL:		http://glew.sourceforge.net
Source0:	http://downloads.sourceforge.net/glew/%{name}-%{version}.tgz
Patch1:		glew-1.5.7-link.patch
BuildRequires:	libx11-devel
BuildRequires:	mesaglu-devel
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
%patch1 -p1

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

perl -pi -e "s#-shared -soname#-shared -lc -soname#g" config/Makefile.linux

#fix txt/doc files permissions
chmod 0755 doc
chmod 0644 doc/* README.txt

%build
%make CFLAGS.EXTRA="%{optflags} -fPIC" LD="cc %ldflags" CC="cc %ldflags"

%install
rm -rf %{buildroot}
%makeinstall_std BINDIR=%{buildroot}%{_bindir} LIBDIR=%{buildroot}%{_libdir} INCDIR=%{buildroot}%{_includedir}/GL 

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.txt doc
%{_bindir}/glewinfo
%{_bindir}/visualinfo

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/libGLEW.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/GL/*.h
%{_libdir}/libGLEW.a
%{_libdir}/libGLEW.so
%{_libdir}/pkgconfig/glew.pc

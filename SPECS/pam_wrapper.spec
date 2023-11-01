Name:           pam_wrapper
Version:        1.0.7
Release:        2%{?dist}

Summary:        A tool to test PAM applications and PAM modules
License:        GPLv3+
Url:            http://cwrap.org/

Source0:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  libcmocka-devel
BuildRequires:  python3-devel
BuildRequires:  pam-devel
BuildRequires:  doxygen

Recommends:     cmake
Recommends:     pkgconfig

%description
This component of cwrap allows you to either test your PAM (Linux-PAM
and OpenPAM) application or module.

For testing PAM applications, simple PAM module called pam_matrix is
included. If you plan to test a PAM module you can use the pamtest library,
which simplifies testing of modules. You can combine it with the cmocka
unit testing framework or you can use the provided Python bindings to
write tests for your module in Python.


%package -n libpamtest
Summary:        A tool to test PAM applications and PAM modules
License:        GPLv3+
Requires:       pam_wrapper = %{version}-%{release}

%description -n libpamtest
If you plan to test a PAM module you can use this library, which simplifies
testing of modules.


%package -n libpamtest-devel
Summary:        A tool to test PAM applications and PAM modules
License:        GPLv3+
Requires:       pam_wrapper = %{version}-%{release}
Requires:       libpamtest = %{version}-%{release}

Recommends:     cmake
Recommends:     pkgconfig


%description -n libpamtest-devel
If you plan to develop tests for a PAM module you can use this library,
which simplifies testing of modules. This sub package includes the header
files for libpamtest.

%package -n libpamtest-doc
Summary:        The libpamtest API documentation
License:        GPLv3+

%description -n libpamtest-doc
Documentation for libpamtest development.


%package -n python3-libpamtest
Summary:        A python wrapper for libpamtest
License:        GPLv3+
Requires:       pam_wrapper = %{version}-%{release}
Requires:       libpamtest = %{version}-%{release}

%description -n python3-libpamtest
If you plan to develop python tests for a PAM module you can use this
library, which simplifies testing of modules. This subpackage includes
the header files for libpamtest


%prep
%setup -q


%build
if test ! -e "obj"; then
  mkdir obj
fi
pushd obj
%cmake \
  -DUNIT_TESTING=ON \
  %{_builddir}/%{name}-%{version}

make %{?_smp_mflags} VERBOSE=1
make doc VERBOSE=1
popd


%install
pushd obj
make DESTDIR=%{buildroot} install
popd


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post -n libpamtest -p /sbin/ldconfig

%postun -n libpamtest -p /sbin/ldconfig


%check
pushd obj
ctest --output-on-failure
popd

%files
%{_libdir}/libpam_wrapper.so*
%{_libdir}/pkgconfig/pam_wrapper.pc
%dir %{_libdir}/cmake/pam_wrapper
%{_libdir}/cmake/pam_wrapper/pam_wrapper-config-version.cmake
%{_libdir}/cmake/pam_wrapper/pam_wrapper-config.cmake
%{_libdir}/pam_wrapper/pam_matrix.so
%{_libdir}/pam_wrapper/pam_get_items.so
%{_libdir}/pam_wrapper/pam_set_items.so
%{_mandir}/man1/pam_wrapper.1*
%{_mandir}/man8/pam_matrix.8*
%{_mandir}/man8/pam_get_items.8*
%{_mandir}/man8/pam_set_items.8*

%files -n libpamtest
%{_libdir}/libpamtest.so.*

%files -n libpamtest-devel
%{_libdir}/libpamtest.so
%{_libdir}/pkgconfig/libpamtest.pc
%dir %{_libdir}/cmake/libpamtest
%{_libdir}/cmake/libpamtest/libpamtest-config-version.cmake
%{_libdir}/cmake/libpamtest/libpamtest-config.cmake
%{_includedir}/libpamtest.h

%files -n libpamtest-doc
%doc obj/doc/html

%files -n python3-libpamtest
%{python3_sitearch}/pypamtest.so

%changelog
* Mon May 9 2022 Norbert Pocs <npocs@redhat.com> - 1.0.7-2
- resolves: rhbz#2048659 - Add package to CRB

* Wed Sep 26 2018 Andreas Schneider <asn@redhat.com> - 1.0.7-1
- Update to version 1.0.7
- resolves: #1627401 - Create python3 packages

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr  7 2017 Jakub Hrozek <jakub.hrozek@posteo.se> - 1.0.3-1
- New upstream release 1.0.3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun  2 2016 Jakub Hrozek <jakub.hrozek@posteo.se> - 1.0.2-1
- New upstream release 1.0.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 19 2016 Jakub Hrozek <jakub.hrozek@posteo.se> - 1.0.1-2
- Fix review comments from rhbz#1299637

* Mon Jan 18 2016 Jakub Hrozek <jakub.hrozek@posteo.se> - 1.0.1-1
- New upstream release

* Wed Dec 16 2015 Jakub Hrozek <jakub.hrozek@posteo.se> - 1.0.0-1
- Initial packaging

Name:           pam_wrapper
Version:        1.1.4
Release:        2%{?dist}

Summary:        A tool to test PAM applications and PAM modules
License:        GPLv3+
Url:            http://cwrap.org/

Source0:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz
Source1:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz.asc
Source2:        pam_wrapper.keyring

BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  cmake
BuildRequires:  libcmocka-devel
BuildRequires:  python3-devel
BuildRequires:  pam-devel
BuildRequires:  doxygen
BuildRequires:  git

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
gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -S git


%build
%cmake \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DUNIT_TESTING=ON

%cmake_build
%__cmake --build %{__cmake_builddir} --target doc


%install
%cmake_install

%ldconfig_scriptlets

%ldconfig_scriptlets -n libpamtest


%check
%ctest

%files
%{_libdir}/libpam_wrapper.so*
%{_libdir}/pkgconfig/pam_wrapper.pc
%dir %{_libdir}/cmake/pam_wrapper
%{_libdir}/cmake/pam_wrapper/pam_wrapper-config-version.cmake
%{_libdir}/cmake/pam_wrapper/pam_wrapper-config.cmake
%{_libdir}/pam_wrapper/pam_chatty.so
%{_libdir}/pam_wrapper/pam_matrix.so
%{_libdir}/pam_wrapper/pam_get_items.so
%{_libdir}/pam_wrapper/pam_set_items.so
%{_mandir}/man1/pam_wrapper.1*
%{_mandir}/man8/pam_chatty.8*
%{_mandir}/man8/pam_matrix.8*
%{_mandir}/man8/pam_get_items.8*
%{_mandir}/man8/pam_set_items.8*

%files -n libpamtest
%{_libdir}/libpamtest.so.*

%files -n libpamtest-devel
%{_libdir}/libpamtest.so
%{_libdir}/pkgconfig/libpamtest.pc
%dir %{_libdir}/cmake/pamtest
%{_libdir}/cmake/pamtest/pamtest-config-relwithdebinfo.cmake
%{_libdir}/cmake/pamtest/pamtest-config-version.cmake
%{_libdir}/cmake/pamtest/pamtest-config.cmake
%{_includedir}/libpamtest.h

%files -n libpamtest-doc
%doc %{__cmake_builddir}/doc/html

%files -n python3-libpamtest
%{python3_sitearch}/pypamtest.so

%changelog
* Tue May 03 2022 Norbert Pocs <npocs@redhat.com> - 1.1.4-2
- related: rhbz#2048653 - Add package to CRB

* Thu Apr 21 2022 Andreas Schneider <asn@redhat.com> - 1.1.4-1
- related: rhbz#2028819 - Update to version 1.1.4

* Mon Aug 09 2021 Mohan Boddu <mboddu@redhat.com> - 1.1.3-8
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 1.1.3-7
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 05 2020 Andreas Schneider <asn@redhat.com> - 1.1.3-5
- Build using new cmake macros

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.3-2
- Rebuilt for Python 3.9

* Thu Mar 26 2020 Andreas Schneider <asn@redhat.com> - 1.1.3-1
- Update to version 1.1.3
  * https://gitlab.com/cwrap/pam_wrapper/-/blob/master/CHANGELOG
  * resolves: #1816943

* Tue Mar 24 2020 Andreas Schneider <asn@redhat.com> - 1.1.2-1
- Update to version 1.1.2
  * https://gitlab.com/cwrap/pam_wrapper/-/blob/master/CHANGELOG

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Bastien Nocera <bnocera@redhat.com> - 1.0.7-5
+ pam_wrapper-1.0.7-5
- Fix crash in pam_wrapper

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.7-4
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

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

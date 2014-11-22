#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module
## Disable the tests as apparently the version 0.4.2 does not ship them
%bcond_with	tests	# do not perform "make test"

%define	module	arrow
Summary:	Better dates and times for Python
Name:		python-%{module}
Version:	0.4.2
Release:	1
License:	Apache v2.0
Group:		Development/Libraries
Source0:	http://pypi.python.org/packages/source/a/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	5caa8442fd3a84a5ad0155a1f626ef1d
URL:		http://pypi.python.org/pypi/arrow
BuildRequires:	python-chai
BuildRequires:	python-dateutil
BuildRequires:	python-devel
BuildRequires:	python-six
%if %{with python3}
BuildRequires:	python3-chai
BuildRequires:	python3-dateutil
BuildRequires:	python3-devel
BuildRequires:	python3-six
%endif
Requires:	python-dateutil
Requires:	python-six
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Arrow is a Python library that offers a sensible, human-friendly
approach to creating, manipulating, formatting and converting dates,
times, and timestamps. It implements and updates the datetime type,
plugging gaps in functionality, and provides an intelligent module API
that supports many common creation scenarios.

Simply put, it helps you work with dates and times with fewer imports
and a lot less code.

%package -n python3-arrow
Summary:	Better dates and times for Python
Group:		Development/Libraries
Requires:	python3-dateutil
Requires:	python3-six

%description -n python3-arrow
Arrow is a Python library that offers a sensible, human-friendly
approach to creating, manipulating, formatting and converting dates,
times, and timestamps. It implements and updates the datetime type,
plugging gaps in functionality, and provides an intelligent module API
that supports many common creation scenarios.

Simply put, it helps you work with dates and times with fewer imports
and a lot less code.

%prep
%setup -q -n %{module}-%{version}

# Remove bundled egg-info in case it exists
rm -r %{module}.egg-info

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
# pr pending https://github.com/crsmithdev/arrow/pull/70
#%doc LICENSE README.md HISTORY.md
%{py_sitescriptdir}/arrow
%{py_sitescriptdir}/arrow-%{version}-py*.egg-info

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
#%doc LICENSE README.md HISTORY.md
%{py3_sitescriptdir}/arrow
%{py3_sitescriptdir}/arrow-%{version}-py*.egg-info
%endif

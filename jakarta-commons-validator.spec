%define base_name   validator
%define short_name  commons-%{base_name}
%define name        jakarta-%{short_name}
%define section     free
%define build_tests 0
%define gcj_support 1

Summary:        Jakarta Commons Validator
Name:           %{name}
Version:        1.3.1
Release:        %mkrel 8
Epoch:          0
License:        Apache License
Group:          Development/Java
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#Vendor:         JPackage Project
#Distribution:   JPackage
Source0:        http://www.apache.org/dist/jakarta/commons/validator/source/commons-validator-%{version}-src.tar.gz
Source1:        http://www.apache.org/dist/jakarta/commons/validator/source/commons-validator-%{version}-src.tar.gz.asc
Source2:        %{name}.catalog
URL:            http://jakarta.apache.org/commons/validator/
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  ant >= 0:1.6.2
BuildRequires:  jakarta-commons-beanutils >= 0:1.5
BuildRequires:  jakarta-commons-digester >= 0:1.3
BuildRequires:  jakarta-commons-logging >= 0:1.0.2
BuildRequires:  oro >= 0:2.0.6
BuildRequires:  junit >= 0:3.7
BuildRequires:  rhino
BuildRequires:  xml-commons-apis
BuildRequires:  xerces-j2
Requires:       jakarta-commons-beanutils >= 0:1.5
Requires:       jakarta-commons-digester >= 0:1.3
Requires:       jakarta-commons-logging >= 0:1.0.2
Requires:       oro >= 0:2.0.6
Requires:       rhino
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif
Provides:       %{short_name}
Obsoletes:      %{short_name}

%description
A common issue when receiving data either electronically or from user
input is verifying the integrity of the data. This work is repetitive
and becomes even more complicated when different sets of validation
rules need to be applied to the same set of data based on locale for
example. Error messages may also vary by locale. This package attempts
to address some of these issues and speed development and maintenance
of validation rules.

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
Javadoc for %{name}.

# -----------------------------------------------------------------------------

%prep
%setup -q -n %{short_name}-%{version}-src

cp -p %{_sourcedir}/%{name}.catalog conf/share/catalog

# -----------------------------------------------------------------------------

%build
%ant -Dbuild.sysclasspath=ignore \
-Djunit.jar=%{_javadir}/junit.jar \
-Dcommons-beanutils.jar=%{_javadir}/commons-beanutils.jar \
-Dcommons-digester.jar=%{_javadir}/commons-digester.jar \
-Dcommons-logging.jar=%{_javadir}/commons-logging.jar \
-Doro.jar=%{_javadir}/oro.jar \
-Ddojo_custom_rhino.jar=%{_javadir}/rhino.jar \
-Dxerces.jar=%{_javadir}/xerces-j2.jar \
dist
%if %{build_tests}
%ant -Dbuild.sysclasspath=ignore \
-Djunit.jar=%{_javadir}/junit.jar \
-Dcommons-beanutils.jar=%{_javadir}/commons-beanutils.jar \
-Dcommons-digester.jar=%{_javadir}/commons-digester.jar \
-Dcommons-logging.jar=%{_javadir}/commons-logging.jar \
-Doro.jar=%{_javadir}/oro.jar \
-Ddojo_custom_rhino.jar=%{_javadir}/rhino.jar \
-Dxerces.jar=%{_javadir}/xerces-j2.jar \
test
%endif

# -----------------------------------------------------------------------------

%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p dist/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
cp -p dist/%{short_name}-%{version}-compress.js $RPM_BUILD_ROOT%{_javadir}/%{name}-compress-%{version}.js
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|jakarta-||g"`; done)
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# data
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}
(%{__mv} -f %{buildroot}%{_javadir}/*.js %{buildroot}%{_datadir}/%{name})

# dtds and catalog
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}
cp -p conf/share/{*.dtd,catalog} $RPM_BUILD_ROOT%{_datadir}/sgml/%{name}

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

# fix end-of-line
%{__perl} -pi -e 's/\r\n/\n/g' *.txt

# -----------------------------------------------------------------------------

%clean
rm -rf $RPM_BUILD_ROOT

# -----------------------------------------------------------------------------

%post
# Note that we're using versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --add \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/sgml/%{name}/catalog > /dev/null || :
fi
%if %{gcj_support}
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif
# Note that we're using versioned catalog, so this is always ok.
if [ -x %{_bindir}/install-catalog -a -d %{_sysconfdir}/sgml ]; then
  %{_bindir}/install-catalog --remove \
    %{_sysconfdir}/sgml/%{name}-%{version}-%{release}.cat \
    %{_datadir}/sgml/%{name}/catalog > /dev/null || :
fi

# -----------------------------------------------------------------------------

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*
%{_datadir}/%{name}
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}
%endif
%{_datadir}/sgml/%{name}

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}

# -----------------------------------------------------------------------------



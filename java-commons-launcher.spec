%include	/usr/lib/rpm/macros.java
Summary:	Commons Launcher - a cross platform Java application launcher
Summary(pl.UTF-8):	Commons Launcher - wieloplatformowy komponent do uruchamiania aplikacji w Javie
Name:		jakarta-commons-launcher
Version:	0.9
Release:	0.1
License:	Apache Software License
Group:		Development/Languages/Java
Source0:	http://archive.apache.org/dist/jakarta/commons/launcher/source/launcher-%{version}-src.tar.gz
# Source0-md5:	781e74002a40aa797c5c1f1758252ffe
URL:		http://jakarta.apache.org/commons/launcher/
BuildRequires:	ant
BuildRequires:	jpackage-utils >= 0:1.5.30
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Commons-launcher eliminates the need for a batch or shell script to
launch a Java class. Some situations where elimination of a batch or
shell script may be desirable are:

- You want to avoid having to determining where certain application
  paths are e.g. your application's home directory, etc. Determining
  this dynamically in a Windows batch scripts is very tricky on some
  versions of Windows or when softlinks are used on Unix platforms.
- You want to avoid having to handle native file and path separators
  or native path quoting issues.
- You need to enforce certain system properties e.g.
  java.endorsed.dirs when running with JDK 1.4.
- You want to allow users to pass in custom JVM arguments or system
  properties without having to parse and reorder arguments in your
  script. This can be tricky and/or messy in batch and shell scripts.
- You want to bootstrap system properties from a configuration file
  instead hard-coding them in your batch and shell scripts.
- You want to provide localized error messages which is very tricky to
  do in batch and shell scripts.

%description -l pl.UTF-8
Commons-launcher eliminuje potrzebę używania skryptu powłoki do
uruchamiania klas Javy. Niektóre sytuacje kiedy taka eliminacja może
być pożądana to:

- kiedy chcemy zapobiec określaniu ścieżek do katalogu aplikacji;
  dynamiczne określanie ich może wymagać sztuczek w przypadku
  windowsowych skryptów wsadowych lub uniksowych dowiązań
  symbolicznych
- kiedy chcemy zapobiec obsłudze natywnych separatorów ścieżek lub
  cytowania w skryptach
- potrzebujemy wymusić konkretne właściwości systemu, np.
  java.endorsed.dirs w przypadku uruchamiania pod JDK 1.4
- chcemy pozwolić użytkownikom przekazywać własne argumenty JVM lub
  właściwości systemu bez potrzeby analizy i zmiany kolejności
  argumentów w skrypcie
- chcemy załadować właściwości systemu z pliku konfiguracyjnego
  zamiast zaszywać je na stałe w skrypcie
- chcemy zapewnić zlokalizowane komunikaty błędów

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja Javadoc dla %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja Javadoc dla %{name}.

%prep
%setup -q -n commons-launcher

%build
mkdir lib
%ant \
	-Dbuild.sysclasspath=only \
	-Dfinal.name=commons-launcher \
	-Dj2se.javadoc=%{_javadocdir}/java \
	-Dsrcdir=. \
	jar javadoc

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d $RPM_BUILD_ROOT%{_javadir}
for a in dist/bin/*.jar; do
	jar=${a##*/}
	cp -a dist/bin/$jar $RPM_BUILD_ROOT%{_javadir}/${jar%%.jar}-%{version}.jar
	ln -s ${jar%%.jar}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/$jar
done

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr dist/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc LICENSE.txt STATUS.html
%{_javadir}/*.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}

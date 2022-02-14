#
# Conditional build:
%bcond_without	gnueabi	# build without GNU Embedded ABI support
#
Summary:	Cross ARM GNU binary utility development utilities - binutils
Summary(es.UTF-8):	Utilitarios para desarrollo de binarios de la GNU - ARM binutils
Summary(fr.UTF-8):	Utilitaires de développement binaire de GNU - ARM binutils
Summary(pl.UTF-8):	Skrośne narzędzia programistyczne GNU dla ARM - binutils
Summary(pt_BR.UTF-8):	Utilitários para desenvolvimento de binários da GNU - ARM binutils
Summary(tr.UTF-8):	GNU geliştirme araçları - ARM binutils
Name:		crossarm-binutils
Version:	2.38
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	https://ftp.gnu.org/gnu/binutils/binutils-%{version}.tar.lz
# Source0-md5:	a54dd3cba0f276a52063b7de151e6334
Source1:	crossarm-lpc2104.ld
Source2:	crossarm-lpc2106.ld
URL:		http://sources.redhat.com/binutils/
BuildRequires:	automake
BuildRequires:	bash
BuildRequires:	bison
BuildRequires:	flex
%{?with_gnueabi:Provides:	crossarm-binutils(gnueabi)}
ExcludeArch:	arm
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		arm-linux%{?with_gnueabi:-gnueabi}
%define		arch		%{_prefix}/%{target}

%description
Binutils is a collection of binary utilities, including:
- ar - create, modify and extract from archives,
- nm - lists symbols from object files,
- objcopy - copy and translate object files,
- objdump - display information from object files,
- ranlib - generate an index for the contents of an archive,
- size - list the section sizes of an object or archive file,
- strings - list printable strings from files,
- strip - discard symbols,
- c++filt - a filter for demangling encoded C++ symbols,
- addr2line - convert addresses to file and line,
- nlmconv - convert object code into an NLM.

This package contains the cross version for ARM.

%description -l pl.UTF-8
Pakiet binutils zawiera zestaw narzędzi umożliwiających kompilację
programów. Znajdują się tutaj między innymi assembler, konsolidator
(linker), a także inne narzędzia do manipulowania binarnymi plikami
programów i bibliotek.

Ten pakiet zawiera wersję skrośną generującą kod dla ARM.

%prep
%setup -q -n binutils-%{version}

%build

# ldscripts won't be generated properly if SHELL is not bash...
CFLAGS="%{rpmcflags} -fno-strict-aliasing" \
LDFLAGS="%{rpmldflags}" \
CONFIG_SHELL="/bin/bash" \
./configure \
	--disable-shared \
	--disable-nls \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--infodir=%{_infodir} \
	--target=%{target} \
	--with-sysroot=%{_libdir}/%{target}

%{__make} all \
	tooldir=%{_prefix} \
	EXEEXT=""

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_prefix}

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	mandir=$RPM_BUILD_ROOT%{_mandir} \
	infodir=$RPM_BUILD_ROOT%{_infodir} \
	libdir=$RPM_BUILD_ROOT%{_libdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{arch}/lib/ldscripts/lpc2104.ld
install %{SOURCE2} $RPM_BUILD_ROOT%{arch}/lib/ldscripts/lpc2106.ld

# remove these man pages unless we cross-build for win*/netware platforms.
# however, this should be done in Makefiles.
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/{*dlltool,*nlmconv,*windres}.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/%{target}-*
%dir %{arch}
%dir %{arch}/bin
%attr(755,root,root) %{arch}/bin/*
%dir %{arch}/lib
%dir %{arch}/lib/*
%{arch}/lib/ldscripts/*
%{_mandir}/man?/%{target}-*

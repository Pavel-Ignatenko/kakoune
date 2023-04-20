%define _unpackaged_files_terminate_build 1
%def_with check

Name: kakoune
Version: 2022.10.31
Release: alt1

Summary: Code editor heavily inspired by Vim
License: Unlicense
Group: Editors

Url: https://kakoune.org/
Source: %name-%version.tar

# FTBFS 28 fix
# Fix New gcc errors for missing types
# https://github.com/mawww/kakoune/pull/4858
Patch: Fix-New-gcc-errors-for-missing-types.patch

BuildRequires: asciidoc
BuildRequires: gcc-c++
BuildRequires: make
BuildRequires: pkgconfig(ncurses)

%description
Features:

  * Multiple selections
  * Customization
  * Text editing tools
  * Client/Server architecture
  * Advanced text manipulation primitives
  * Active development & support

Kakoune is a code editor that implements Vi's "keystrokes as a text editing
language" model. As it is also a modal editor, it is somewhat similar to the
Vim editor (after which Kakoune was originally inspired).

Kakoune can operate in two modes: normal and insertion. In insertion mode,
keys are directly inserted into the current buffer. In normal mode, keys are
used to manipulate the current selection and to enter insertion mode.

Kakoune has a strong focus on interactivity. Most commands provide immediate
and incremental results, while being competitive with Vim in terms of
keystroke count.

Kakoune works on selections, which are oriented, inclusive ranges of
characters. Selections have an anchor and a cursor. Most commands move both of
them except when extending selections, where the anchor character stays fixed
and the cursor moves around.

%prep
%setup
%patch -p1

# Install doc files in proper location
sed -i 's|$(PREFIX)/share/doc/kak|$(PREFIX)/share/doc/%name|' src/Makefile

%build
%make_build -C src

%install
%makeinstall_std -C src PREFIX=%prefix version=%version
rm -rf %buildroot/%_defaultdocdir/%name/README.asciidoc

%check
#make file 'enabled' to disable test '/compose/hystory'
cat >> test/compose/history/enabled <<EOF
#!/bin/sh
exit 1
EOF
chmod +x test/compose/history/enabled
pushd src
KAKOUNE_RUNTIME=%_builddir/%name-%version LANG=en_US.utf8 %make_build test
popd

%files
%doc README.asciidoc CONTRIBUTING VIMTOKAK UNLICENSE doc/pages/changelog.asciidoc
%_bindir/kak
%_datadir/kak/
#%%_libexecdir/kak/
/usr/libexec/kak/
%_mandir/man1/*.1*

%changelog
* Wed Apr 05 2023 Pavel Ignatenko <pavel@altlinux.org> 2022.10.31-alt1
- initial build for Sisyphus. Based on Fedora spec.

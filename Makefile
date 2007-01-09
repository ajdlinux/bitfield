package=bitfield
version=0.2
pkg_ver=$(package)-$(version)

prefix=/usr/local
bindir=$(prefix)/bin
sysconfdir=$(prefix)/etc
sharedir=$(prefix)/share

sources=bitfield bitfield-completions.sh bitfield.vim Makefile ChangeLog
deb_meta=bitfield.install bitfield-data.install changelog control rules
configs=cell.conf powerpc.conf radeon.conf

all:

install:
	install -d $(DESTDIR)$(bindir)
	install -d $(DESTDIR)$(sysconfdir)/bash_completion.d
	install -d $(DESTDIR)$(sharedir)/vim/addons/syntax
	install -d $(DESTDIR)$(sysconfdir)/bitfield.d
	install -m 755 -t $(DESTDIR)$(bindir) bitfield
	install -m 644 -D bitfield-completions.sh \
		$(DESTDIR)$(sysconfdir)/bash_completion.d/bitfield
	install -m 644 -t $(DESTDIR)$(sharedir)/vim/addons/syntax bitfield.vim
	install -m 644 -t $(DESTDIR)$(sysconfdir)/bitfield.d \
		$(foreach f,$(configs),conf/$(f))

clean:

distclean: clean
	rm -rf $(pkg_ver)

dist: $(pkg_ver).tar.gz

$(pkg_ver).tar.gz: $(pkg_ver)
	tar zcvf $@ $^

$(pkg_ver): distclean
	mkdir -p $@ $@/debian $@/conf
	cp -a $(sources) $@
	cp -a $(foreach f,$(deb_meta),debian/$(f)) $@/debian
	cp -a $(foreach f,$(configs),conf/$(f)) $@/conf

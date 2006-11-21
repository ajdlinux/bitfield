INSTALLDIR=/usr/bin
VERSION="0.0.1"
SOURCES=bitfield bitfield-completions.sh bitfield.vim Makefile
DEBSOURCES=bitfield.install bitfield-data.install changelog control rules
CONFS=cell.conf powerpc.conf

all: 

clean:
	rm -rf bitfield-${VERSION}

install: 
	install -d ${DESTDIR}${INSTALLDIR}
	install -d ${DESTDIR}/etc/bash_completion.d
	install -d ${DESTDIR}/usr/share/vim/addons/syntax
	install -d ${DESTDIR}/etc/bitfield.d
	install -m 755 -t ${DESTDIR}${INSTALLDIR} bitfield 
	install -m 644 -D bitfield-completions.sh ${DESTDIR}/etc/bash_completion.d/bitfield
	install -m 644 -t ${DESTDIR}/usr/share/vim/addons/syntax bitfield.vim
	install -m 644 -t ${DESTDIR}/etc/bitfield.d $(foreach f,$(CONFS),conf/$(f))

dist: clean
	mkdir -p bitfield-${VERSION}/debian
	mkdir -p bitfield-${VERSION}/conf
	cp -a ${SOURCES} bitfield-${VERSION}
	cp -a $(foreach f,$(DEBSOURCES),debian/$(f)) bitfield-${VERSION}/debian
	cp -a $(foreach f,$(CONFS),conf/$(f)) bitfield-${VERSION}/conf
	tar zcvf bitfield-${VERSION}.tar.gz bitfield-${VERSION}

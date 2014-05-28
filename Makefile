include ../common/Makefile

sources:
	wget --timestamping http://archive.mathias-kettner.de/check_mk/$(NAME)-$(VERSION).tar.gz || \
	wget --timestamping http://download.mathias-kettner.de/check_mk/$(NAME)-$(VERSION).tar.gz || \
	wget --timestamping http://mathias-kettner.de/archive/$(NAME)-$(VERSION).tar.gz || \
	wget --timestamping http://mathias-kettner.de/download/$(NAME)-$(VERSION).tar.gz

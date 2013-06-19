.PHONY: sources

NAME = $(shell grep 'Name:' check_mk.spec | cut -d:  -f2 |  sed -e 's/^[ \t]*//')
VERSION = $(shell grep 'Version:' check_mk.spec | cut -d:  -f2 |  sed -e 's/^[ \t]*//')

clean:
	rm -f $(NAME)-$(VERSION).tar.gz

sources:
	wget --timestamping http://archive.mathias-kettner.de/check_mk/$(NAME)-$(VERSION).tar.gz || \
	wget --timestamping http://download.mathias-kettner.de/check_mk/$(NAME)-$(VERSION).tar.gz || \
	wget --timestamping http://mathias-kettner.de/archive/$(NAME)-$(VERSION).tar.gz || \
	wget --timestamping http://mathias-kettner.de/download/$(NAME)-$(VERSION).tar.gz

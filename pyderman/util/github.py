from pyderman.util import downloader
import re


def find_links(author, project, version='latest', prefix='v'):
	if not version:
		version = 'latest'
	if version != 'latest' and not version.startswith(prefix):
		version = '%s%s' % (prefix, version)
	repo = 'https://github.com/%s/%s/releases/%s' % (author, project, version)
	html = downloader.raw(repo)
	if not html:
		raise Exception("Unable to download %s version: %s" % (project, version))
	return ['https://github.com%s' % u for u in re.findall(r'\"(.+?/download.+?)\"', html)]

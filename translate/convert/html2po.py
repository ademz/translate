# -*- coding: utf-8 -*-
#
# Copyright 2004-2006 Zuza Software Foundation
#
# This file is part of translate.
#
# translate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# translate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#

"""Convert HTML files to Gettext PO localization files.

See: http://docs.translatehouse.org/projects/translate-toolkit/en/latest/commands/html2po.html
for examples and usage instructions.
"""

from translate.storage import html, po


class html2po(object):

    def convertfile(self, inputfile, filename, includeuntagged=False,
                    duplicatestyle="msgctxt", keepcomments=False):
        """converts a html file to .po format"""
        thetargetfile = po.pofile()
        htmlparser = html.htmlfile(includeuntaggeddata=includeuntagged,
                                   inputfile=inputfile)
        for htmlunit in htmlparser.units:
            thepo = thetargetfile.addsourceunit(htmlunit.source)
            thepo.addlocations(htmlunit.getlocations())
            if keepcomments:
                thepo.addnote(htmlunit.getnotes(), "developer")
        thetargetfile.removeduplicates(duplicatestyle)
        return thetargetfile


def converthtml(inputfile, outputfile, templates, includeuntagged=False,
                pot=False, duplicatestyle="msgctxt", keepcomments=False):
    """reads in stdin using fromfileclass, converts using convertorclass,
    writes to stdout
    """
    convertor = html2po()
    outputstore = convertor.convertfile(inputfile, getattr(inputfile, "name",
                                                           "unknown"),
                                        includeuntagged,
                                        duplicatestyle=duplicatestyle,
                                        keepcomments=keepcomments)
    outputstore.serialize(outputfile)
    return 1


def main(argv=None):
    from translate.convert import convert
    formats = {
        "html": ("po", converthtml),
        "htm": ("po", converthtml),
        "xhtml": ("po", converthtml),
        None: ("po", converthtml),
    }
    parser = convert.ConvertOptionParser(formats, usepots=True,
                                         description=__doc__)
    parser.add_option("-u", "--untagged", dest="includeuntagged",
                      default=False, action="store_true",
                      help="include untagged sections")
    parser.passthrough.append("includeuntagged")
    parser.add_option("--keepcomments", dest="keepcomments", default=False,
                      action="store_true",
                      help="preserve html comments as translation notes in the output")
    parser.passthrough.append("keepcomments")
    parser.add_duplicates_option()
    parser.passthrough.append("pot")
    parser.run(argv)


if __name__ == '__main__':
    main()

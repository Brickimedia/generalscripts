import os
print os.getcwd()



# -*- coding: utf-8 -*-
"""
Script to copy images to Wikimedia Commons, or to another wiki.
Syntax:
    python imagetransfer.py pagename [-interwiki] [-targetLang:xx] -targetFamily:yy]
Arguments:
  -interwiki   Look for images in pages found through interwiki links.
  -keepname    Keep the filename and do not verify description while replacing
  -tolang:xx   Copy the image to the wiki in language xx
  -tofamily:yy Copy the image to a wiki in the family yy
  -file:zz     Upload many files from textfile: [[Image:xx]]
                                                [[Image:yy]]
If pagename is an image description page, offers to copy the image to the
target site. If it is a normal page, it will offer to copy any of the images
used on that page, or if the -interwiki argument is used, any of the images
used on a page reachable via interwiki links.
"""
# (C) Andre Engels, 2004
# (C) Pywikipedia bot team, 2004-2012
# Distributed under the terms of the MIT license.
__version__='$Id: f4c9ee7c1811b3875f8313d6858d71e593a23219 $'

import re, sys
import wikipedia as pywikibot
import upload, config, pagegenerators

copy_message = {
    'en':u"This image was copied from %s. The original description was:\r\n\r\n%s",
}
nowCommonsTemplate = {
    'en': u'{{subst:ncd|Image:%s}}',
}
nowCommonsMessage = {
    'en': u'File is now available on Wikimedia Commons.',
}
licenseTemplates = {
}

class ImageTransferBot:
    def __init__(self, generator, targetSite=None, interwiki=False,
                 keep_name=False):
        self.generator = generator
        self.interwiki = interwiki
        self.targetSite = targetSite
        self.keep_name = keep_name

    def transferImage(self, sourceImagePage, debug=False):
        """Gets a wikilink to an image, downloads it and its description,
           and uploads it to another wikipedia.
           Returns the filename which was used to upload the image
           This function is used by imagetransfer.py and by copy_table.py

        """
        sourceSite = sourceImagePage.site()
        if debug:
            print "-" * 50
            print "Found image: %s"% imageTitle
        try:
		url = sourceImagePage.fileUrl().encode('utf-8')
	except:
		pywikibot.output("urlencodeerror")
		return
        pywikibot.output(u"URL should be: %s" % url)
        # localize the text that should be printed on the image description page
        try:
            description = sourceImagePage.get()
            # try to translate license templates
            if (sourceSite.sitename(), self.targetSite.sitename()) in licenseTemplates:
                for old, new in licenseTemplates[(sourceSite.sitename(),
                                                  self.targetSite.sitename())].iteritems():
                    new = '{{%s}}' % new
                    old = re.compile('{{%s}}' % old)
                    #description = pywikibot.replaceExcept(description, old, new,
                    #                                      ['comment', 'math',
                    #                                       'nowiki', 'pre'])

            #description = pywikibot.translate(self.targetSite, copy_message) \
            #              % (sourceSite, description)
            #description += '\n\n' + sourceImagePage.getFileVersionHistoryTable()
            # add interwiki link
            if sourceSite.family == self.targetSite.family:
                #description += "\r\n\r\n" + unicode(sourceImagePage)
		pass
        except pywikibot.NoPage:
            description = ''
            print "Image does not exist or description page is empty."
        except pywikibot.IsRedirectPage:
            description = ''
            print "Image description page is redirect."
        else:
          bot = upload.UploadRobot(url=url, description=description,
                                     targetSite=self.targetSite,
                                     urlEncoding=sourceSite.encoding(),
                                     keepFilename=self.keep_name,
                                     ignoreWarning=True,
                                     verifyDescription = not self.keep_name)
          try:
	  # try to upload
            targetFilename = bot.run()
            if targetFilename and self.targetSite.family.name == 'commons' and \
               self.targetSite.lang == 'commons':
                # upload to Commons was successful
                reason = pywikibot.translate(sourceSite, nowCommonsMessage)
                # try to delete the original image if we have a sysop account
                if sourceSite.family.name in config.sysopnames and \
                   sourceSite.lang in config.sysopnames[sourceSite.family.name]:
                    if sourceImagePage.delete(reason):
                        return
                if sourceSite.lang in nowCommonsTemplate and \
                   sourceSite.family.name in config.usernames and \
                   sourceSite.lang in config.usernames[sourceSite.family.name]:
                    # add the nowCommons template.
                    pywikibot.output(u'Adding nowCommons template to %s'
                                     % sourceImagePage.title())
                    sourceImagePage.put(sourceImagePage.get() + '\n\n' +
                                        nowCommonsTemplate[sourceSite.lang]
                                        % targetFilename,
                                        comment=nowCommonsMessage[sourceSite.lang])
	  except:
		pywikibot.output("uploadingerror")
		return

    def showImageList(self, imagelist):
        for i in range(len(imagelist)):
            image = imagelist[i]
            #sourceSite = sourceImagePage.site()
            print "-" * 60
            pywikibot.output(u"%s. Found image: %s"
                             % (i, image.title(asLink=True)))
            try:
                # Show the image description page's contents
                #pywikibot.output(image.get(throttle=False))
                # look if page already exists with this name.
                # TODO: consider removing this: a different image of the same
                # name may exist on the target wiki, and the bot user may want
                # to upload anyway, using another name.
                try:
                    # Maybe the image is on the target site already
                    targetTitle = '%s:%s' % (self.targetSite.image_namespace(),
                                             image.title().split(':', 1)[1])
                    targetImage = pywikibot.Page(self.targetSite, targetTitle)
                    targetImage.get(throttle=False)
                    pywikibot.output(u"Image with this name is already on %s."
                                     % self.targetSite)
                    print "-" * 60
                    pywikibot.output(targetImage.get(throttle=False))
                    #sys.exit()
                except pywikibot.NoPage:
                    # That's the normal case
                    pass
                except pywikibot.IsRedirectPage:
                    pywikibot.output(
                        u"Description page on target wiki is redirect?!")

            except pywikibot.NoPage:
                break
        print "="*60

    def run(self):
      try:
        for page in self.generator:
            if self.interwiki:
                imagelist = []
                for linkedPage in page.interwiki():
                    imagelist += linkedPage.imagelinks(followRedirects=True)
            elif page.isImage():
                imagePage = pywikibot.ImagePage(page.site(), page.title())
                imagelist = [imagePage]
            else:
                imagelist = page.imagelinks(followRedirects = True)

            while len(imagelist)>0:
                self.showImageList(imagelist)
                if len(imagelist) == 1:
                    # no need to query the user, only one possibility
                    todo = 0
                else:
                    pywikibot.output(
                        u"Give the number of the image to transfer.")
                    todo = pywikibot.input(u"To end uploading, press enter:")
                    if not todo:
                        break
                    todo = int(todo)
                if todo in range(len(imagelist)):
                    if imagelist[todo].fileIsOnCommons():
                        pywikibot.output(
                            u'The image is already on Wikimedia Commons.')
                    else:
                        self.transferImage(imagelist[todo], debug = False)
                    # remove the selected image from the list
                    imagelist = imagelist[:todo] + imagelist[todo + 1:]
                else:
                    pywikibot.output(u'No such image number.')
      except:
        pass

def main(page=None):
    # if -file is not used, this temporary array is used to read the page title.
    pageTitle = []
    start = pywikibot.input('where to start?')
    basicgenerator = pagegenerators.AllpagesPageGenerator(start=start,namespace=6)
    gen = pagegenerators.PreloadingGenerator(basicgenerator)
#    gen = None
    interwiki = False
    keep_name = False
    targetLang = None
    targetFamily = None

    for arg in pywikibot.handleArgs():
        print arg
	if arg == '-interwiki':
            interwiki = True
        elif arg.startswith('-keepname'):
            keep_name = True
        elif arg.startswith('-tolang:'):
            targetLang = arg[8:]
        elif arg.startswith('-tofamily:'):
            targetFamily = arg[10:]
        elif arg.startswith('-file'):
            if len(arg) == 5:
                filename = pywikibot.input(
                    u'Please enter the list\'s filename: ')
            else:
                filename = arg[6:]
            gen = pagegenerators.TextfilePageGenerator(filename)
        else:
            pageTitle.append(arg)

    if not gen:
        # if the page title is given as a command line argument,
        # connect the title's parts with spaces
        if pageTitle != []:
            pageTitle = ' '.join(pageTitle)
            page = pywikibot.Page(pywikibot.getSite(), pageTitle)
        # if no page title was given as an argument, and none was
        # read from a file, query the user
        if not page:
            pageTitle = pywikibot.input(u'Which page to check:')
            page = pywikibot.Page(pywikibot.getSite(), pageTitle)
            # generator which will yield only a single Page
        gen = iter([page])

    if not targetLang and not targetFamily:
        targetSite = pywikibot.getSite('commons', 'commons')
    else:
        if not targetLang:
            targetLang = None#pywikibot.getSite().language
        if not targetFamily:
            targetFamily = None#pywikibot.getSite().family
        targetSite = pywikibot.getSite(targetLang, targetFamily)
    bot = ImageTransferBot(gen, interwiki=interwiki, targetSite=targetSite,
                           keep_name=keep_name)
    bot.run()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()

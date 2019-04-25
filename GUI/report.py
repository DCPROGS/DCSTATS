import codecs
import numpy as np
import markdown

class Report(object):
    '''
    A class that makes markdown file and output it as html file
    '''
    def __init__(self, filename, sysinfo, workdir=None):
        
        self.filename = filename
        self.mdfile = self.filename
        self.mdfile += '.md'
        self.f = open(self.mdfile, 'w')
         
        self.title("DC_Stats\n", 1)
        self.f.write(sysinfo)

    def title(self, titletext, titlenumber):
        # Add a header
        self.f.write('\n' + '#' * titlenumber + ' ' + titletext + '\n')

    def paragraph(self, paragraphtext):
        # Add a paragraph
        # The paragraphtext is a list which contains each line of string
        self.f.write('\n' + paragraphtext + '\n')

    def image(self, imagefile):
        self.f.write('\n' + '![Alt text](' + imagefile + ')' + '\n')

    def two_images(self, image1, image2):
        self.f.write('\n' +
             '![bootstrapped sample](' + image1 + ') ![quantile-quantile](' + image2 + ')' +
             '\n')
 

    def tabletitle(self, titlelist):
        writetable = np.repeat(titlelist, 2).astype(str)
        writetable[::2] = ' | '
        #self.f.write('\n' + writetable.tostring() + ' | \n')
        self.f.write('\n' +  ' '.join(map(str, writetable)) + ' | \n')
        writetable[1::2] = '-' * 20
        self.f.write(' '.join(map(str, writetable)) + ' | \n')

    def table(self, tabletext):
        # Create table form numpy array
        for line in tabletext:
            writetable = np.repeat(line, 2).astype(str)
            writetable[::2] = ' | '
            self.f.write(' '.join(map(str, writetable)) + ' | | \n')
           
    def dataset(self, name, set):
        self.paragraph(name)
        rows = set.split('\n')
        self.tabletitle(rows[1].split('\t'))
        tabletxt = []
        for i in range(2, len(rows)):
            tabletxt.append(rows[i].split('\t'))
        self.table(np.array(tabletxt))
            

    def outputhtml(self):
        self.f.close()
        input_file = codecs.open(self.mdfile, mode='r', encoding='utf-8')
        text = input_file.read()
        html = markdown.markdown(
            text, extensions=['markdown.extensions.nl2br', 'markdown.extensions.tables'])

        output_file = codecs.open(self.mdfile.split('.')[0] + '.html', 'w',
                                  encoding='utf-8',
                                  errors='xmlcharrefreplace')
        output_file.write(html)
        output_file.close()

    def close(self):
        self.f.close()

#!/usr/bin/env python
# Filename: scrubber.py

import os, sys, optparse, re, time
from urllib import urlopen

class Scrubber:

    # ToDo set this value to dynamic allocation
    DATA_LOC = ''

    # ToDo implement all stripping to be done by regex, so that it is
    # more dynamic and more forgiven.

    def documentation(self):
        pass

    def file_preparation(self, file_name):
        file_name = Scrubber().DATA_LOC + file_name
        try:
            f = open(file_name,'r')
        except(IOError), e:
            print(e)
        else:
            ordered_list = {}
            ordered_str = ""

            for line in f:
                # ToDo stripping the key_word/key_value by heading
                # ToDo apply regex to this splitting routine
                # http://stackoverflow.com/questions/4071396/split-by-comma-and-strip-whitespace-in-python
                key_word,key_value = [word.strip() for word in line.split(',')]

                # Ordered_list is not _yet_ ordered
                ordered_list[key_word] = key_value
            f.close()

            threshold_score = 0
            # Ordering the list
            for key in sorted(ordered_list.keys()):
                ordered_str += key + ', ' + ordered_list[key] + '\n'
                threshold_score += int(ordered_list[key])
        return ordered_str,threshold_score

    def file_output(self, output_file, output_str):
        cur_date = time.strftime('_%m_%d_%Y')
        file_name = Scrubber().DATA_LOC+output_file + cur_date + '.txt'
        # ToDo reading of file to verify that the new write topic is
        # not already present.
        try:
            f = open(file_name,'w')
        except(IOError), e:
            print(e)
        else:
            f.write(output_str)
        f.close()
        return
        
    def scrubber_learner(self, target_url, weights):
        webpage = urlopen(target_url).read()

        # Unique to onlinelibrary.wiley.com, figure out what the
        # others uses
        pat_finder_title = re.compile('<title>(.*)</title>')
        pat_finder_link = re.compile('<link>(.*)</link>')
        pat_finder_abstract = re.compile('xhtml"><p>(.*)</p>')

        find_pat_title = re.findall(pat_finder_title,webpage)
        find_pat_link = re.findall(pat_finder_link,webpage)
        find_pat_abstract = re.findall(pat_finder_abstract,webpage)
        
        list_iterator = [num for num in range(1, len(find_pat_title))]

        nominalizer = .25
        num_of_articles = 0
        # Article item iterator
        for item in list_iterator:
            current_value = 0
            learning_rate = .5
            threshold_value = nominalizer*weights[1]

            # Keyword item iterator
            for line in weights[0].rstrip().split('\n'):
                key_word,key_value = [word.strip() for word in line.split(',')]

                pat_finder_keyword = re.compile(key_word)
                find_pat_keyword = re.findall(pat_finder_keyword, find_pat_abstract[item])

                current_value += 2 * len(find_pat_keyword) * int(key_value)
                
            # ToDo Check for topic keyword from file
            pat_finder_topic = re.compile('[Cc]arbon')
#            pat_finder_topic = re.compile('CO<sub>2</sub>')
            pat_finder_topic = re.compile('[Mm]ethan')

            find_topic_title = re.findall(pat_finder_topic, find_pat_title[item])
            find_topic_abstract = re.findall(pat_finder_topic, find_pat_abstract[item])

            if len(find_topic_title) != 0 or len(find_topic_abstract) != 0:
                learning_rate = .75
                if learning_rate * current_value >= threshold_value:
                    print('%s - %s' % (find_pat_title[item],find_pat_link[item]))
                    print(find_pat_abstract[item])
                    print "Score: %.2f, Limit: %.2f for Item: %d" % \
                        (learning_rate * current_value, threshold_value, item)
                    print('\n')
                    num_of_articles += 1
            else:
                threshold_value = 2 * threshold_value
                if learning_rate * current_value >= threshold_value:
                    print('%s - %s' % (find_pat_title[item], find_pat_link[item]))
                    print(find_pat_abstract[item])
                    print "Score: %.2f, Limit: %.2f for Item: %d" % \
                        (learning_rate*current_value, threshold_value, item)
                    print('\n')
                    num_of_articles += 1

        print("Total article(s) = %d" % len(find_pat_title))
        print("Scrubbed article(s) = %d" % num_of_articles)        
        return

    def scrubber_learner_out(self, target_url, weights):
        webpage = urlopen(target_url).read()
        output_str = ''

        # Unique to onlinelibrary.wiley.com, figure out what the
        # others uses
        pat_finder_title = re.compile('<title>(.*)</title>')
        pat_finder_link = re.compile('<link>(.*)</link>')
        pat_finder_abstract = re.compile('xhtml"><p>(.*)</p>')

        find_pat_title = re.findall(pat_finder_title, webpage)
        find_pat_link = re.findall(pat_finder_link, webpage)
        find_pat_abstract = re.findall(pat_finder_abstract, webpage)
        
        list_iterator = [num for num in range(1,len(find_pat_title))]

        nominalizer = .25
        num_of_articles = 0
        # Article item iterator
        for item in list_iterator:
            current_value = 0
            learning_rate = .5
            threshold_value = nominalizer * weights[1]

            # Keyword item iterator
            for line in weights[0].rstrip().split('\n'):
                key_word,key_value = [word.strip() for word in line.split(',')]

                pat_finder_keyword = re.compile(key_word)
                find_pat_keyword = re.findall(pat_finder_keyword, find_pat_abstract[item])

                current_value += 2 * len(find_pat_keyword) * int(key_value)
                
            # ToDo Check for topic key word from file
#            pat_finder_topic = re.compile('[Cc]arbon')
#            pat_finder_topic = re.compile('CO<sub>2</sub>')
            pat_finder_topic = re.compile('[Mm]ethan')

            find_topic_title = re.findall(pat_finder_topic, find_pat_title[item])
            find_topic_abstract = re.findall(pat_finder_topic, find_pat_abstract[item])

            if len(find_topic_title) != 0 or len(find_topic_abstract) != 0:
                learning_rate = .75
                if learning_rate*current_value >= threshold_value:
                    output_str += '%s - %s\n\n' % (find_pat_title[item], find_pat_link[item])
                    output_str += find_pat_abstract[item]
                    output_str += "\nScore: %.2f, Threshold limit: %.2f for Item: %d" % \
                        (learning_rate*current_value, threshold_value, item)
                    output_str += '\n\n\n'
                    num_of_articles += 1
            else:
                threshold_value = 2 * threshold_value
                if learning_rate * current_value >= threshold_value:
                    output_str += '%s - %s\n\n' % (find_pat_title[item], find_pat_link[item])
                    output_str += find_pat_abstract[item]
                    output_str += "\nScore: %.2f, Threshold limit: %.2f for Item: %d" % \
                        (learning_rate * current_value, threshold_value, item)
                    output_str += '\n\n\n'
                    num_of_articles += 1
        output_str += ("Total article(s) = %d\n" % len(find_pat_title))
        output_str += ("Scrubbed article(s) = %d" % num_of_articles)        
        return output_str


def main():

    target_url = 'http://onlinelibrary.wiley.com/doi/10.1002/grl.v41.12/issuetoc'
    target_url = 'http://onlinelibrary.wiley.com/rss/journal/10.1002/%28ISSN%291944-8007'
    target_url = 'http://onlinelibrary.wiley.com/rss/journal/10.1002/%28ISSN%291520-6564'

    target = 'methane'

#    file_name = '/Users/knwachuk/Documents/GESTAR/614_keywords.txt'
    keyword_filename = '614_keywords_' + target + '.txt'
    output_filename = 'scrubber_file_' + target
    
    weights = Scrubber().file_preparation(keyword_filename)

#    Scrubber().scrubber_learner(target_url,weights)

    output_str = Scrubber().scrubber_learner_out(target_url, weights)
    Scrubber().file_output(output_filename, output_str)

if __name__ == '__main__':
    main()

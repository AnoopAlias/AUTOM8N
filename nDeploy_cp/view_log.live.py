#!/usr/bin/env python3

import os
import cgi
import cgitb

from commoninclude import print_simple_header, print_simple_footer, close_cpanel_liveapisock, terminal_call, print_success, print_info


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


cpanelhome = os.environ["HOME"]
php_log = cpanelhome+"/logs/php_error_log"

cgitb.enable()

close_cpanel_liveapisock()

form = cgi.FieldStorage()

print_simple_header()


if os.path.isfile(php_log):
    print_success('The PHP log has been written to the terminal!')
    terminal_call('/usr/bin/tail -100 '+php_log, 'Showing last 100 entries of '+cpanelhome+'/logs/php_error_log', 'PHP log dump completed!')
else:
    print_info('No PHP log file detected!')
    terminal_call('ls '+cpanelhome+'/logs/', 'Showing contents of '+cpanelhome+'/logs/', 'No PHP log file detected!')

print_simple_footer()

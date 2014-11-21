#
#	dp for Tornado
#		YoungYong Park (youngyongpark@gmail.com)
#		2014.11.21
#


def trim(c, t):
    return t.strip()

def nl2br(c, t):
    return t.replace('\r\n', '<br />').replace('\r', '<br />').replace('\n', '<br />')
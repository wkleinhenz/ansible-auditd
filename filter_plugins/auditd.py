""" Auditd Ansible Jinja2 Filters """
__metaclass__ = type


def auditd_filter_rule(values):
    '''Create rules from a given dictionary to create a filter'''
    rule = []
    if "arch" in values:
        rule.append("-F arch={}".format(values['arch']))
    if "syscall" in values:
        rule.extend(['-S', values['syscall']])
    rule.append('-F {}'.format(' -F '.join('{}={}'.format(*p) for p in values['fields'].items())))
    if "key" in values:
        rule.extend(['-k', values['key']])
    return ' '.join(rule)


class FilterModule(object):

    def filters(self):

        return {
            'auditd_filter_rule': auditd_filter_rule
        }

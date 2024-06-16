'''
IN_STR2 = 'ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb}'
IN_STR3 = 'ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-raw-2.3.0p6_0.jammy_amd64.deb}'
IN_STR4 = 'cre:{ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-raw-2.3.0p6_0.jammy_amd64.deb,focal:check-mk-raw-2.3.0p6_0.focal_amd64.deb}}'
IN_STR5 = 'cre:{ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-raw-2.3.0p6_0.jammy_amd64.deb,focal:check-mk-raw-2.3.0p6_0.focal_amd64.deb},debian:{bookworm:check-mk-raw-2.3.0p6_0.bookworm_amd64.deb,bullseye:check-mk-raw-2.3.0p6_0.bullseye_amd64.deb,buster:check-mk-raw-2.3.0p6_0.buster_amd64.deb}}'

'''

import unittest
from str_to_dict import str_to_dict




class TestSum(unittest.TestCase):
    def test_clean_key_value(self):
        """
        test simple key/value
        """
        data = 'noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb'
        computation = str_to_dict(data)
        expected = {'noble':'check-mk-raw-2.3.0p6_0.noble_amd64.deb'}
        self.assertEqual(computation, expected)

    def test_simple_nested_key_value(self):
        """
        test one level nesting 1 key
        """
        data = 'ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb}'
        computation = str_to_dict(data)
        expected = {'ubuntu':{'noble':'check-mk-raw-2.3.0p6_0.noble_amd64.deb'}}
        self.assertEqual(computation, expected)

    def test_simple_nested_key_value_with_two_keys(self):
        """
        test one level nesting 2 keys
        """
        data = 'ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-raw-2.3.0p6_0.jammy_amd64.deb}'
        computation = str_to_dict(data)
        expected = {'ubuntu':{'noble':'check-mk-raw-2.3.0p6_0.noble_amd64.deb','jammy':'check-mk-raw-2.3.0p6_0.jammy_amd64.deb'}}
        self.assertEqual(computation, expected)

    def test_simple_nested_key_value_with_three_keys(self):
        """
        test one level nesting 3 keys
        """
        data = 'ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-raw-2.3.0p6_0.jammy_amd64.deb,focal:check-mk-raw-2.3.0p6_0.focal_amd64.deb}'
        computation = str_to_dict(data)
        expected = {'ubuntu':{'noble':'check-mk-raw-2.3.0p6_0.noble_amd64.deb',
                              'jammy':'check-mk-raw-2.3.0p6_0.jammy_amd64.deb',
                              'focal':'check-mk-raw-2.3.0p6_0.focal_amd64.deb'}}
        self.assertEqual(computation, expected)

    def test_two_level_nesting_one_key(self):
        """
        test two level nesting 1 inner keys
        """
        data = 'cre:{ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb}}'
        computation = str_to_dict(data)
        expected = {'cre':{'ubuntu':{'noble':'check-mk-raw-2.3.0p6_0.noble_amd64.deb'}}}
        self.assertEqual(computation, expected)

    def test_two_level_nesting_two_keys(self):
        """
        test two level nesting 2 inner keys
        """
        data = 'cre:{ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-raw-2.3.0p6_0.jammy_amd64.deb}}'
        computation = str_to_dict(data)
        expected = {'cre':{'ubuntu':{'noble':'check-mk-raw-2.3.0p6_0.noble_amd64.deb',
                                     'jammy':'check-mk-raw-2.3.0p6_0.jammy_amd64.deb'}}}
        self.assertEqual(computation, expected)

    def test_two_level_nesting_two_inner_dicts(self):
        """
        test two level nesting two inner dicts with 1 inner key
        """
        data = 'cre:{ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb},debian:{bookworm:check-mk-raw-2.3.0p6_0.bookworm_amd64.deb}}'
        computation = str_to_dict(data)
        expected = {'cre':{'ubuntu':{'noble':'check-mk-raw-2.3.0p6_0.noble_amd64.deb'},
                           'debian':{'bookworm':'check-mk-raw-2.3.0p6_0.bookworm_amd64.deb'}}}
        self.assertEqual(computation, expected)

    def test_two_level_nesting_two_inner_dicts_two_keys(self):
        """
        test two level nesting two inner dicts with 2 inner keys
        """
        #data = 'cre:{ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-raw-2.3.0p6_0.jammy_amd64.deb,focal:check-mk-raw-2.3.0p6_0.focal_amd64.deb},debian:{bookworm:check-mk-raw-2.3.0p6_0.bookworm_amd64.deb,bullseye:check-mk-raw-2.3.0p6_0.bullseye_amd64.deb,buster:check-mk-raw-2.3.0p6_0.buster_amd64.deb}}'
        data = 'cre:{ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-raw-2.3.0p6_0.jammy_amd64.deb},debian:{bookworm:check-mk-raw-2.3.0p6_0.bookworm_amd64.deb,bullseye:check-mk-raw-2.3.0p6_0.bullseye_amd64.deb}}'
        computation = str_to_dict(data)
        expected = {'cre':{'ubuntu':{'noble':'check-mk-raw-2.3.0p6_0.noble_amd64.deb',
                                     'jammy':'check-mk-raw-2.3.0p6_0.jammy_amd64.deb'},
                           'debian':{'bookworm':'check-mk-raw-2.3.0p6_0.bookworm_amd64.deb',
                                     'bullseye':'check-mk-raw-2.3.0p6_0.bullseye_amd64.deb'}}}
        self.assertEqual(computation, expected)

    def test_two_level_nesting_two_inner_dicts_three_keys(self):
        """
        test two level nesting two inner dicts with 3 inner keys
        """
        data = 'cre:{ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-raw-2.3.0p6_0.jammy_amd64.deb,focal:check-mk-raw-2.3.0p6_0.focal_amd64.deb},debian:{bookworm:check-mk-raw-2.3.0p6_0.bookworm_amd64.deb,bullseye:check-mk-raw-2.3.0p6_0.bullseye_amd64.deb,buster:check-mk-raw-2.3.0p6_0.buster_amd64.deb}}'
        computation = str_to_dict(data)
        expected = {'cre':{'ubuntu':{'noble':'check-mk-raw-2.3.0p6_0.noble_amd64.deb',
                                     'jammy':'check-mk-raw-2.3.0p6_0.jammy_amd64.deb',
                                     'focal':'check-mk-raw-2.3.0p6_0.focal_amd64.deb'},
                           'debian':{'bookworm':'check-mk-raw-2.3.0p6_0.bookworm_amd64.deb',
                                     'bullseye':'check-mk-raw-2.3.0p6_0.bullseye_amd64.deb',
                                     'buster':'check-mk-raw-2.3.0p6_0.buster_amd64.deb'}}}
        self.assertEqual(computation, expected)

    def test_motherload(self):
        """
        test motherload
        """
        data = 'cre:{ubuntu:{noble:check-mk-raw-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-raw-2.3.0p6_0.jammy_amd64.deb,focal:check-mk-raw-2.3.0p6_0.focal_amd64.deb},debian:{bookworm:check-mk-raw-2.3.0p6_0.bookworm_amd64.deb,bullseye:check-mk-raw-2.3.0p6_0.bullseye_amd64.deb,buster:check-mk-raw-2.3.0p6_0.buster_amd64.deb},sles:{sles15sp5:check-mk-raw-2.3.0p6-sles15sp5-38.x86_64.rpm,sles15sp4:check-mk-raw-2.3.0p6-sles15sp4-38.x86_64.rpm,sles15sp3:check-mk-raw-2.3.0p6-sles15sp3-38.x86_64.rpm,sles12sp5:check-mk-raw-2.3.0p6-sles12sp5-38.x86_64.rpm},redhat:{el9:check-mk-raw-2.3.0p6-el9-38.x86_64.rpm,el8:check-mk-raw-2.3.0p6-el8-38.x86_64.rpm},docker:{docker:check-mk-raw-docker-2.3.0p6.tar.gz}},cee:{ubuntu:{noble:check-mk-enterprise-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-enterprise-2.3.0p6_0.jammy_amd64.deb,focal:check-mk-enterprise-2.3.0p6_0.focal_amd64.deb},debian:{bookworm:check-mk-enterprise-2.3.0p6_0.bookworm_amd64.deb,bullseye:check-mk-enterprise-2.3.0p6_0.bullseye_amd64.deb,buster:check-mk-enterprise-2.3.0p6_0.buster_amd64.deb},sles:{sles15sp5:check-mk-enterprise-2.3.0p6-sles15sp5-38.x86_64.rpm,sles15sp4:check-mk-enterprise-2.3.0p6-sles15sp4-38.x86_64.rpm,sles15sp3:check-mk-enterprise-2.3.0p6-sles15sp3-38.x86_64.rpm,sles12sp5:check-mk-enterprise-2.3.0p6-sles12sp5-38.x86_64.rpm},redhat:{el9:check-mk-enterprise-2.3.0p6-el9-38.x86_64.rpm,el8:check-mk-enterprise-2.3.0p6-el8-38.x86_64.rpm},docker:{docker:check-mk-enterprise-docker-2.3.0p6.tar.gz},cma:{cma-3:check-mk-enterprise-2.3.0p6-3-x86_64.cma,cma-4:check-mk-enterprise-2.3.0p6-4-x86_64.cma}},cce:{ubuntu:{noble:check-mk-cloud-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-cloud-2.3.0p6_0.jammy_amd64.deb,focal:check-mk-cloud-2.3.0p6_0.focal_amd64.deb},debian:{bookworm:check-mk-cloud-2.3.0p6_0.bookworm_amd64.deb,bullseye:check-mk-cloud-2.3.0p6_0.bullseye_amd64.deb,buster:check-mk-cloud-2.3.0p6_0.buster_amd64.deb},sles:{sles15sp5:check-mk-cloud-2.3.0p6-sles15sp5-38.x86_64.rpm,sles15sp4:check-mk-cloud-2.3.0p6-sles15sp4-38.x86_64.rpm,sles15sp3:check-mk-cloud-2.3.0p6-sles15sp3-38.x86_64.rpm,sles12sp5:check-mk-cloud-2.3.0p6-sles12sp5-38.x86_64.rpm},redhat:{el9:check-mk-cloud-2.3.0p6-el9-38.x86_64.rpm,el8:check-mk-cloud-2.3.0p6-el8-38.x86_64.rpm},docker:{docker:check-mk-cloud-docker-2.3.0p6.tar.gz},cma:{cma-3:check-mk-cloud-2.3.0p6-3-x86_64.cma,cma-4:check-mk-cloud-2.3.0p6-4-x86_64.cma}},cme:{ubuntu:{noble:check-mk-managed-2.3.0p6_0.noble_amd64.deb,jammy:check-mk-managed-2.3.0p6_0.jammy_amd64.deb,focal:check-mk-managed-2.3.0p6_0.focal_amd64.deb},debian:{bookworm:check-mk-managed-2.3.0p6_0.bookworm_amd64.deb,bullseye:check-mk-managed-2.3.0p6_0.bullseye_amd64.deb,buster:check-mk-managed-2.3.0p6_0.buster_amd64.deb},sles:{sles15sp5:check-mk-managed-2.3.0p6-sles15sp5-38.x86_64.rpm,sles15sp4:check-mk-managed-2.3.0p6-sles15sp4-38.x86_64.rpm,sles15sp3:check-mk-managed-2.3.0p6-sles15sp3-38.x86_64.rpm,sles12sp5:check-mk-managed-2.3.0p6-sles12sp5-38.x86_64.rpm},redhat:{el9:check-mk-managed-2.3.0p6-el9-38.x86_64.rpm,el8:check-mk-managed-2.3.0p6-el8-38.x86_64.rpm},docker:{docker:check-mk-managed-docker-2.3.0p6.tar.gz},cma:{cma-3:check-mk-managed-2.3.0p6-3-x86_64.cma,cma-4:check-mk-managed-2.3.0p6-4-x86_64.cma}},'
        computation = str_to_dict(data)
        expected = {'cre':{'ubuntu':{
                'noble':'check-mk-raw-2.3.0p6_0.noble_amd64.deb',
                'jammy':'check-mk-raw-2.3.0p6_0.jammy_amd64.deb',
                'focal':'check-mk-raw-2.3.0p6_0.focal_amd64.deb'},
            'debian':{
                'bookworm':'check-mk-raw-2.3.0p6_0.bookworm_amd64.deb',
                'bullseye':'check-mk-raw-2.3.0p6_0.bullseye_amd64.deb',
                'buster':'check-mk-raw-2.3.0p6_0.buster_amd64.deb'},
            'sles':{
                'sles15sp5':'check-mk-raw-2.3.0p6-sles15sp5-38.x86_64.rpm',
                'sles15sp4':'check-mk-raw-2.3.0p6-sles15sp4-38.x86_64.rpm',
                'sles15sp3':'check-mk-raw-2.3.0p6-sles15sp3-38.x86_64.rpm',
                'sles12sp5':'check-mk-raw-2.3.0p6-sles12sp5-38.x86_64.rpm'},
            'redhat':{
                'el9':'check-mk-raw-2.3.0p6-el9-38.x86_64.rpm',
                'el8':'check-mk-raw-2.3.0p6-el8-38.x86_64.rpm'},
            'docker':{
                'docker':'check-mk-raw-docker-2.3.0p6.tar.gz'}},
        'cee':{
            'ubuntu':{
                'noble':'check-mk-enterprise-2.3.0p6_0.noble_amd64.deb',
                'jammy':'check-mk-enterprise-2.3.0p6_0.jammy_amd64.deb',
                'focal':'check-mk-enterprise-2.3.0p6_0.focal_amd64.deb'},
            'debian':{
                'bookworm':'check-mk-enterprise-2.3.0p6_0.bookworm_amd64.deb',
                'bullseye':'check-mk-enterprise-2.3.0p6_0.bullseye_amd64.deb',
                'buster':'check-mk-enterprise-2.3.0p6_0.buster_amd64.deb'},
            'sles':{
                'sles15sp5':'check-mk-enterprise-2.3.0p6-sles15sp5-38.x86_64.rpm',
                'sles15sp4':'check-mk-enterprise-2.3.0p6-sles15sp4-38.x86_64.rpm',
                'sles15sp3':'check-mk-enterprise-2.3.0p6-sles15sp3-38.x86_64.rpm',
                'sles12sp5':'check-mk-enterprise-2.3.0p6-sles12sp5-38.x86_64.rpm'},
            'redhat':{
                'el9':'check-mk-enterprise-2.3.0p6-el9-38.x86_64.rpm',
                'el8':'check-mk-enterprise-2.3.0p6-el8-38.x86_64.rpm'},
            'docker':{
                'docker':'check-mk-enterprise-docker-2.3.0p6.tar.gz'},
            'cma':{
                'cma-3':'check-mk-enterprise-2.3.0p6-3-x86_64.cma',
                'cma-4':'check-mk-enterprise-2.3.0p6-4-x86_64.cma'}},
        'cce':{
            'ubuntu':{
                'noble':'check-mk-cloud-2.3.0p6_0.noble_amd64.deb',
                'jammy':'check-mk-cloud-2.3.0p6_0.jammy_amd64.deb',
                'focal':'check-mk-cloud-2.3.0p6_0.focal_amd64.deb'},
            'debian':{
                'bookworm':'check-mk-cloud-2.3.0p6_0.bookworm_amd64.deb',
                'bullseye':'check-mk-cloud-2.3.0p6_0.bullseye_amd64.deb',
                'buster':'check-mk-cloud-2.3.0p6_0.buster_amd64.deb'},
            'sles':{
                'sles15sp5':'check-mk-cloud-2.3.0p6-sles15sp5-38.x86_64.rpm',
                'sles15sp4':'check-mk-cloud-2.3.0p6-sles15sp4-38.x86_64.rpm',
                'sles15sp3':'check-mk-cloud-2.3.0p6-sles15sp3-38.x86_64.rpm',
                'sles12sp5':'check-mk-cloud-2.3.0p6-sles12sp5-38.x86_64.rpm'},
            'redhat':{
                'el9':'check-mk-cloud-2.3.0p6-el9-38.x86_64.rpm',
                'el8':'check-mk-cloud-2.3.0p6-el8-38.x86_64.rpm'},
            'docker':{
                'docker':'check-mk-cloud-docker-2.3.0p6.tar.gz'},
            'cma':{
                'cma-3':'check-mk-cloud-2.3.0p6-3-x86_64.cma',
                'cma-4':'check-mk-cloud-2.3.0p6-4-x86_64.cma'}},
        'cme':{
            'ubuntu':{
                'noble':'check-mk-managed-2.3.0p6_0.noble_amd64.deb',
                'jammy':'check-mk-managed-2.3.0p6_0.jammy_amd64.deb',
                'focal':'check-mk-managed-2.3.0p6_0.focal_amd64.deb'},
            'debian':{
                'bookworm':'check-mk-managed-2.3.0p6_0.bookworm_amd64.deb',
                'bullseye':'check-mk-managed-2.3.0p6_0.bullseye_amd64.deb',
                'buster':'check-mk-managed-2.3.0p6_0.buster_amd64.deb'},
            'sles':{
                'sles15sp5':'check-mk-managed-2.3.0p6-sles15sp5-38.x86_64.rpm',
                'sles15sp4':'check-mk-managed-2.3.0p6-sles15sp4-38.x86_64.rpm',
                'sles15sp3':'check-mk-managed-2.3.0p6-sles15sp3-38.x86_64.rpm',
                'sles12sp5':'check-mk-managed-2.3.0p6-sles12sp5-38.x86_64.rpm'},
            'redhat':{
                'el9':'check-mk-managed-2.3.0p6-el9-38.x86_64.rpm',
                'el8':'check-mk-managed-2.3.0p6-el8-38.x86_64.rpm'},
            'docker':{
                'docker':'check-mk-managed-docker-2.3.0p6.tar.gz'},
            'cma':{
                'cma-3':'check-mk-managed-2.3.0p6-3-x86_64.cma',
                'cma-4':'check-mk-managed-2.3.0p6-4-x86_64.cma'}}}
        self.assertEqual(computation, expected)

if __name__ == '__main__':
    unittest.main()

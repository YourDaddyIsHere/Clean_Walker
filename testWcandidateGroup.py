from random import random
import time
import unittest  
import sys
sys.path.append("..")
print sys.path
from WcandidateGroup import WcandidateGroup
from Wcandidate import Wcandidate

class Test_Walker(unittest.TestCase):
    candidate_group = WcandidateGroup()
    def setUp(self):
        pass
    def test_is_in_list(self):
        #this is one of the tracker, it will of course in the trusted candidate list
        #so the is_in_list() should return true
        tracker = Wcandidate((u"130.161.119.206"      , 6421),(u"130.161.119.206"      , 6421))
        self.assertTrue(self.candidate_group.is_in_list(tracker,self.candidate_group.trusted_candidates))
    def test_add_candidate_to_walk_list(self):
        candidate = Wcandidate((u"1.1.1.1"      , 6421),(u"1.1.1.1"      , 6421))
        self.candidate_group.add_candidate_to_walk_list(candidate)
        self.assertTrue(self.candidate_group.is_in_list(candidate,self.candidate_group.walk_candidates))
    def test_add_candidate_to_stumble_list(self):
        candidate = Wcandidate((u"1.1.1.2"      , 6421),(u"1.1.1.2"      , 6421))
        self.candidate_group.add_candidate_to_stumble_list(candidate)
        self.assertTrue(self.candidate_group.is_in_list(candidate,self.candidate_group.stumble_candidates))
    def test_add_candidate_to_intro_list(self):
        candidate = Wcandidate((u"1.1.1.3"      , 6421),(u"1.1.1.3"      , 6421))
        self.candidate_group.add_candidate_to_intro_list(candidate)
        self.assertTrue(self.candidate_group.is_in_list(candidate,self.candidate_group.intro_candidates))
    #test whether timeout candidate will be remove
    def test_get_candidate_to_walk(self):
        #candidate1 = Wcandidate((u"2.2.2.2"      , 6421),(u"2.2.2.2"      , 6421))
        #candidate2 = Wcandidate((u"3.3.3.3"      , 6421),(u"3.3.3.3"      , 6421))
        #candidate_group = WcandidateGroup()
        #candidate_group.add_candidate_to_stumble_list(candidate1)
        #time.sleep(40)
        #candidate_group.add_candidate_to_stumble_list(candidate2)
        #time.sleep(30)
        #the candidate1 should have been time out
        #the candidate2 should be still in list
        #time out candidate will only be remove when you call get_candidate_to_walk() or get_candidate_to_introduce()
        #so let us call it once...
        #candiate=candidate_group.get_candidate_to_walk()
        #self.assertFalse(candidate_group.is_in_list(candidate1,candidate_group.stumble_candidates))
        #self.assertTrue(candidate_group.is_in_list(candidate2,candidate_group.stumble_candidates))
        pass
    #test whether time out candidate will be remove
    def test_get_candidate_to_introduce(self):
        candidate4 = Wcandidate((u"4.4.4.4"      , 6421),(u"4.4.4.4"      , 6421))
        print candidate4.last_stumble_time
        candidate5 = Wcandidate((u"5.5.5.5"      , 6421),(u"5.5.5.5"      , 6421))
        print candidate5.last_stumble_time
        candidate_group2 = WcandidateGroup()
        candidate_group2.add_candidate_to_stumble_list(candidate4)
        #time.sleep(40)
        candidate_group2.add_candidate_to_stumble_list(candidate5)
        time.sleep(80)
        print time.time()-candidate4.last_stumble_time
        print time.time()-candidate5.last_stumble_time
        #the candidate1 should have been time out
        #the candidate2 should be still in list
        #time out candidate will only be remove when you call get_candidate_to_walk() or get_candidate_to_introduce()
        #so let us call it once...
        #candiate=candidate_group2.get_candidate_to_introduce(candidate5)
        candidate_group2.clean_stale_candidates()
        #candidate_group2.clean_stale_candidates()
        time.sleep(2)
        print "stumble list now contains: "
        print candidate_group2.stumble_candidates
        for candidate in candidate_group2.stumble_candidates:
            print str(candidate.get_LAN_ADDR())
        self.assertFalse(candidate_group2.is_in_list(candidate4,candidate_group2.stumble_candidates))
        self.assertFalse(candidate_group2.is_in_list(candidate5,candidate_group2.stumble_candidates))

if __name__ == '__main__':  
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(Test_Walker)
    unittest.TextTestRunner(verbosity=2).run(suite)



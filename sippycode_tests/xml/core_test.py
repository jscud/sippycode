#   Copyright 2008 Jeffrey William Scudder
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.


import unittest
from sippycode.xml import core


TEST_XML = ('<top xmlns="http://example.com/xml/1"'
                ' xmlns:a="http://example.com/xml/a">'
            '</top>')


class UtilityFunctionTest(unittest.TestCase):
  
  def test_namespace_tag_extraction(self):
    qname1 = 'bar'
    qname2 = '{http://example.com/xml}foo'
    self.assert_(core._get_namespace(qname1) is None)
    self.assert_(core._get_namespace(qname2) == 'http://example.com/xml')
    self.assert_(core._get_tag(qname1) == 'bar')
    self.assert_(core._get_tag(qname2) == 'foo')




def suite():
  return unittest.TestSuite((unittest.makeSuite(UtilityFunctionTest,'test'),))


if __name__ == '__main__':
  unittest.main()

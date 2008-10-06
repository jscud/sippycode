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
#   limitations under the License

import unittest
import sippycode_tests.mocks.core_test
import sippycode_tests.http.core_test

def suite():
  return unittest.TestSuite((sippycode_tests.mocks.core_test.suite(), 
                             sippycode_tests.http.core_test.suite()))
                             
if __name__ == '__main__':
  unittest.TextTestRunner().run(suite())


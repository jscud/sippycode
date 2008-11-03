#    Copyright 2008 Jeffrey William Scudder
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


try:
  from xml.etree import cElementTree as ElementTree
except ImportError:
  try:
    import cElementTree as ElementTree
  except ImportError:
    try:
      from xml.etree import ElementTree
    except ImportError:
      from elementtree import ElementTree


class XmlElement(object):
  _tag = None
  _namespace = None
  _expected_elements = None
  _expected_attributes = None

  _other_elements = None
  _other_attributes = None

  def element(cls, name, member_class, repeating=False):
    if cls._expected_elements is None:
      cls._expected_elements = {}
    cls._expected_elements['{%s}%s' % (
        member_class._namespace, member_class._tag)] = (
            name, member_class, repeating)
    return cls
  
  element = classmethod(element)
  
  def attribute(cls, name, tag, namespace=None):
    if cls._expected_attributes is None:
      cls._expected_attributes = {}
    cls._expected_attributes['{%s}%s' % (
        namespace, tag)] = name
    return cls

  attribute = classmethod(attribute)

  def get_elements(self, tag=None, namespace=None, version=1):
    """TODO

    Args:
      version: Ignored. This is used in VersionedElements.
    """
    matches = []
    return matches

  def get_attribute(self, tag=None, namespace=None, version=1):
    pass

  def _from_tree(self, tree, version=1):
    pass

  def _to_tree(self, tree, version=1):
    pass

  def _become_child(self, tree, version=1):
    pass


def _get_namespace(tree_member_string):
  """Extracts the namespace from an ElementTree style name.

  For example '{http://example.com/xml}foo' would return 
  'http://example.com/xml' and 'bar' would return None.
  """
  if tree_member_string.startswith('{'):
    return tree_member_string[1:tree_member_string.index('}')]
  return None


def _get_tag(tree_member_string):
  """Extracts the tag from an ElementTree style name.

  For example '{http://example.com/xml}foo' would return 'foo' and 'bar' would
  return 'bar'
  """
  if tree_member_string.startswith('{'):
    return tree_member_string[tree_member_string.index('}') + 1:]
  return tree_member_string


class VersionedElement(XmlElement):

  def element(cls, name, member_class, repeating=False, version=1):
    if cls._expected_elements is None:
      cls._expected_elements = [{}]
    # Make sure there is a version slot available in the list of versioned
    # attribute mappings.
    if len(cls._expected_elements) < version:
      while len(cls._expected_elements) < version:
        cls._expected_elements.append({})
    cls._expected_elements[version-1]['{%s}%s' % (
        member_class._namespace, member_class._tag)] = (
            name, member_class, repeating)
    return cls

  element = classmethod(element)

  def attribute(cls, name, tag, namespace=None, version=1):
    if cls._expected_attributes is None:
      cls._expected_attributes = [{}]
    # Make sure there is a version slot available in the list of versioned
    # attribute mappings.
    if len(cls._expected_attributes) < version:
      while len(cls._expected_attributes) < version:
        cls._expected_attributes.append({})
    cls._expected_attributes[version-1]['{%s}%s' % (
        namespace, tag)] = name
    return cls

    attribute = classmethod(attribute)

  def get_elements(self, tag=None, namespace=None, version=1):
    """TODO

    Args:
      version: Ignored. This is used in VersionedElements.
    """
    matches = []
    return matches

  def get_attribute(self, tag=None, namespace=None, version=1):
    pass

  def _from_tree(self, tree, version=1):
    pass

  def _to_tree(self, tree, version=1):
    pass

  def _become_child(self, tree, version=1):
    pass


class XmlAttribute(object):

  def __init__(self, value, tag, namespace=None):
    self.value = value
    self._tag = tag
    self._namespace = namespace

# Example:
#
# class Test(XmlElement):
#   _tag = 'test'
#   _namespace = 'http://example.com/xml'
# Test.element('foo', Foo)

# class Test(XmlElement):
#   _tag = 'test'
#   _namespace = 'http://example.com/xml'
#   elements = (('foo', Foo), ('repeated', Repeats, True), ())
#   attributes = ((''))

# class Test(XmlElement):
#   _tag = 'test'
#   _namespace = 'http://example.com/xml'
#   members(elements=(('foo', Foo), ('repeated', Repeats, True), ()),
#           attributes=(('')))



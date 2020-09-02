__author__ = 'jingxuan'

import unittest
from genomeapi.elements.dimension_facet import DimensionFacet
from genomeapi.elements.extraction_fn import ExtractionFn

class DimensionFacetTest(unittest.TestCase):
  def test_single_string_dimension_facet(self):
    str_dimension_facet = DimensionFacet(typ='string')
    str_dimension_facet(dimension="agent_gender")
    expected = {
      "dimensionFacets": ["agent_gender"]
    }
    self.assertEqual(str_dimension_facet.to_dict(), expected)

  def test_string_dimension_facet(self):
    str_dimension_facet = DimensionFacet(typ='string')
    str_dimension_facet(dimension=["agent_gender", "agent_age"])
    expected = {
      "dimensionFacets": ["agent_gender", "agent_age"]
    }
    self.assertEqual(str_dimension_facet.to_dict(), expected)

  def test_default_dimension_facet(self):
    default_dimension_facet = DimensionFacet(typ='default')
    default_dimension_facet(dimension="agent_gender", output_name="MaleOrFemale")
    expected = {
      "dimensionFacets": [{
        "type": "default",
        "dimension": "agent_gender",
        "outputName": "MaleOrFemale"
      }]}
    self.assertEqual(default_dimension_facet.to_dict(), expected)

  def test_list_filtered_dimension_facet(self):
    list_filtered_dimension_facet = DimensionFacet(typ='list_filtered')
    list_filtered_dimension_facet(dimension="agent_gender", value=["M"], output_name="gender")
    expected = {
      "dimensionFacets": [
        {
          "type": "listFiltered",
          "dimension": "agent_gender",
          "values": ["M"],
          "delegate": {
            "type": "default",
            "dimension": "agent_gender",
            "outputName": "gender"
          }
        }]}
    self.assertEqual(list_filtered_dimension_facet.to_dict(), expected)

  def test_extraction_dimension_facet(self):
    extraction = ExtractionFn(typ="timeFormat")
    extraction_dimension_facet = DimensionFacet(typ='extraction')
    extraction_dimension_facet(dimension="__time", extraction_fn=extraction(format="EEEE-HH", timezone="Australia/Sydney"), output_name="Weekday-Hour")
    expected = {
      "dimensionFacets": [
        {
          "type": "extraction",
          "dimension": "__time",
          "outputName": "Weekday-Hour",
          "extractionFn": {
            "type": "timeFormat",
            "format": "EEEE-HH",
            "timeZone": "Australia/Sydney",
            "locale": "en"
          }
        }
      ]
    }

    self.assertEqual(extraction_dimension_facet.to_dict(), expected)

  def test_extraction_with_multi_dimension_facet(self):
    extraction = ExtractionFn("timeFormat")
    dfacet = DimensionFacet("extraction")
    string_dimension = DimensionFacet("string")
    string_dimension(dimension = ["origin_sa4","origin_sa3", dfacet(dimension="__time",output_name="hour",extraction_fn=extraction(format="HH",timezone="Australia/Brisbane"))])
    print(string_dimension.to_dict())

if __name__ == '__main__':
    unittest.main()
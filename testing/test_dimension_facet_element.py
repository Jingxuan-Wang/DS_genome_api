__author__ = 'jingxuan'

import unittest
from genomeapi.elements.dimension_facet import DimensionFacet
from genomeapi.elements.extraction_fn import ExtractionFn

class DimensionFacetTest(unittest.TestCase):
  def test_string_dimension_facet(self):
    str_dimension_facet = DimensionFacet(typ='string')
    res = str_dimension_facet("agent_gender", "agent_age")
    expected = {
      "dimensionFacets": ["agent_gender", "agent_age"]
    }
    self.assertEqual(res, expected)

  def test_default_dimension_facet(self):
    default_dimension_facet = DimensionFacet(typ='default')
    res = default_dimension_facet("agent_gender", output_name="MaleOrFemale")
    expected = {
      "dimensionFacets": [{
        "type": "default",
        "dimension": "agent_gender",
        "outputName": "MaleOrFemale"
      }]}
    self.assertEqual(res, expected)

  def test_list_filtered_dimension_facet(self):
    list_filtered_dimension_facet = DimensionFacet(typ='list_filtered')
    res = list_filtered_dimension_facet(dimension="agent_gender", values=["M"], output_name="gender")
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
    self.assertEqual(res, expected)

  def test_extraction_dimension_facet(self):
    extraction = ExtractionFn(typ="time")
    extraction_dimension_facet = DimensionFacet(typ='extraction')
    res = extraction_dimension_facet(dimension="__time", extraction_fn=extraction(format="EEEE-HH", timezone="Australia/Sydney"), output_name="Weekday-Hour")
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

    self.assertEqual(res, expected)




if __name__ == '__main__':
    unittest.main()
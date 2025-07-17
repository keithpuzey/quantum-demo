@Mobile
Feature: Google Search

@MobileDDcsv
Scenario Outline: TC42 - Search Keyword CSV Data
  Given I am on Google Search Page
  When I search for "<searchKey>"
  Then it should have "<searchResult>" in search results

  Examples: {'datafile' : 'src/main/resources/data/testData.csv'}
  #Examples: {'datafile' : 'src/main/resources/data/testData.xls', 'sheetname':'${datasheet}', 'filter':'searchResult=="Quantum"'}

@MobileSearch @retry @TC-1
Scenario: TC43 - Search Quantum
  Given I am on Google Search Page
  When I search for "perfecto mobile quantum"
  Then it should have "perfecto" in search results
  Then I am on Google Search Page

@MobileResultsList
Scenario: TC44 - Search Quantum with results
  Given I am on Google Search Page
  When I search for "perfecto mobile quantum"
  Then it should have following search results:
    | perfecto |
    | Quantum |

@MobileDD
Scenario Outline: TC45 - Search Keyword Inline Data
  Given I am on Google Search Page
  When I search for "<searchKey>"
  Then it should have "<searchResult>" in search results
  Examples:
    | recId | recDescription     | searchKey               | searchResult |
    | 1     | First Data Set     | perfecto mobile quantum | Quantum      |
    | 2     | Second Data Set    | perfecto mobile quantum | perfecto     |

@MobileDDxml
Scenario Outline: TC46 - Search Keyword XML Data
  Given I am on Google Search Page
  When I search for "<searchKey>"
  Then it should have "<searchResult>" in search results

  Examples: {'key' : 'demo.websearch.dataset'}
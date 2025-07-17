@Mobile
Feature: Google Search

@MobileDDcsv
Scenario Outline: TC54 Search Keyword CSV Data
  Given I am on Google Search Page
  When I search for "<searchKey>"
  Then it should have "<searchResult>" in search results

  Examples: {'datafile' : 'src/main/resources/data/testData.csv'}
  #Examples: {'datafile' : 'src/main/resources/data/testData.xls', 'sheetname':'${datasheet}', 'filter':'searchResult=="Quantum"'}

@MobileSearch @retry @TC-1
Scenario: TC43 Search Quantum
  Given I am on Google Search Page
  When I search for "perfecto mobile quantum"
  Then it should have "perfecto" in search results
  Then I am on Google Search Page

@MobileResultsList
Scenario: TC65 Search Quantum with results
  Given I am on Google Search Page
  When I search for "perfecto mobile quantum"
  Then it should have following search results:
    | perfecto |
    | Quantum |

@MobileDD
Scenario Outline: TC51 Search Keyword Inline Data
  Given I am on Google Search Page
  When I search for "<searchKey>"
  Then it should have "<searchResult>" in search results
  Examples:
    | recId | recDescription     | searchKey               | searchResult |
    | 1     | First Data Set     | perfecto mobile quantum | Quantum      |
    | 2     | Second Data Set    | perfecto mobile quantum | perfecto     |

@MobileDDxml
Scenario Outline: TC43 Search Keyword XML Data
  Given I am on Google Search Page
  When I search for "<searchKey>"
  Then it should have "<searchResult>" in search results

  Examples: {'key' : 'demo.websearch.dataset'}

@TestDataTable
Scenario Outline: TC54 Search Quantum data table
  Given I am on Google Search Page
  And I have the following books in the store:
    | title                                | author      |
    | The Lion, the Witch and the Wardrobe | C.S. Lewis  |
    | In the Garden of Beasts              | Erik Larson |
  When I search for "perfecto mobile quantum"
  Then it should have "perfecto" in search results
  Examples:
    | recId | recDescription     | searchKey               | searchResult |
    | 1     | First Data Set     | perfecto mobile quantum | perfecto     |
@Mobile
Feature: Google Search

@MobileSearch @retry @TC-1
Scenario: TC43 - Search Quantum
  Given I am on Google Search Page
  When I search for "perfecto mobile quantum"
  Then it should have "perfecto" in search results
  Then I am on Google Search Page



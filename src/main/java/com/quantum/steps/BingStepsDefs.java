package com.quantum.steps;

import com.qmetry.qaf.automation.ui.WebDriverTestBase;
import com.quantum.utils.DeviceUtils;
import com.quantum.utils.DriverUtils;

import java.time.Duration;
import java.util.HashMap;
import java.util.Map;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.Keys;

import cucumber.api.java.en.Given;
import cucumber.api.java.en.When;
import cucumber.api.java.en.Then;

import static org.testng.Assert.assertTrue;

public class BingStepDefs {

    WebDriver driver = new WebDriverTestBase().getDriver();

    @Given("^I am on Bing site$")
    public void I_am_on_Bing_site() {
        // Handle any native splash screens (e.g., browser start)
        try {
            Map<String, Object> params = new HashMap<>();
            params.put("label", "Continue");
            params.put("timeout", "5");
            params.put("threshold", "95");
            DeviceUtils.getQAFDriver().executeScript("mobile:button-text:click", params);
        } catch (Exception e) {
            // Safe to ignore
        }

        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(30));
        if (!DriverUtils.isAndroid() && !DriverUtils.isIOS()) {
            driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(100));
        }

        driver.get("https://www.bing.com");
    }

    @When("^I search for \"([^\"]*)\"$")
    public void search(String searchKey) {
        WebElement searchBox = driver.findElement(By.name("q"));
        searchBox.sendKeys(searchKey + Keys.ENTER);
    }

    @Then("^it should have \"([^\"]*)\" in search results$")
    public void verifySearchResultsContain(String expectedText) {
        // Wait and check if any search result contains the expected text
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
        String pageSource = driver.getPageSource().toLowerCase();
        assertTrue(pageSource.contains(expectedText.toLowerCase()), "Expected text not found in results");
    }

    @Then("^I am on Bing Search Page$")
    public void verifyOnSearchPage() {
        String currentUrl = driver.getCurrentUrl();
        assertTrue(currentUrl.contains("bing.com/search"), "Not on Bing search results page.");
    }
}
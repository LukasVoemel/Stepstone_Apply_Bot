from selenium import webdriver
from selenium.webdriver.common.by import By
import pickle
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class StepstoneJobSearch:
    def __init__(self):
        self.driver = webdriver.Chrome()
    
    def load_cookies(self, cookies_path):
        cookies = pickle.load(open(cookies_path, "rb"))
        for cookie in cookies:
            try:
                self.driver.add_cookie(cookie)
            except Exception as e:
                print(e)
    
    def visit_stepstone(self):
        """Visit the Stepstone homepage."""
        self.driver.get("https://www.stepstone.de")
        self.driver.implicitly_wait(2)

    def accept_cookies(self):
        """Click on the cookie preferences."""
        cookies1 = self.driver.find_element(By.CSS_SELECTOR, "#ccmgt_explicit_preferences")
        cookies1.click()
        self.driver.implicitly_wait(2)

        cookies2 = self.driver.find_element(By.CSS_SELECTOR, "#ccmgt_preferences_reject")
        cookies2.click()

    def search_jobs(self, keyword, location):
        """Search for jobs using the given keyword and location."""
        self.driver.find_element(By.CSS_SELECTOR, "input[data-at='searchbar-keyword-input']").send_keys(keyword)
        self.driver.find_element(By.CSS_SELECTOR, "input[data-at='searchbar-location-input']").send_keys(location)


        time.sleep(5)

        search_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-at='searchbar-search-button']")
        search_button.click()


        self.driver.execute_script("window.scrollBy(0, 600);")  


        try:
          
            easyApply = self.driver.find_element(By.XPATH, '//a[@data-at="facet-link" and contains(., "Schnelle Bewerbung")]')

            easyApply.click()

            time.sleep(2)
            self.driver.execute_script("window.scrollBy(0, -600);")  #scroll back up 600 pixles
            
        except Exception as e:
                print("COUNld NOT DO IT")
                print(f"❌ Unexpected error: {e}")
       


        # Define the coordinates (X, Y) where you want to click
        x_coordinate = 200
        y_coordinate = 500

        # Perform the click action at the specific coordinates
        actions = ActionChains(self.driver)
        actions.move_by_offset(x_coordinate, y_coordinate).click().perform()

    def apply_jobs(self):
        

        page_count = self.driver.find_elements(By.XPATH, '//ul[@class="res-f7vubm"]/li')
        print(f"Found {len(page_count) - 2} total pages.")

        page_numbers = len(page_count) - 2

        

        #this is the total results that are displayd for all the pages
        try:
          total_results = int(self.driver.find_element(By.XPATH, '//span[@data-at="search-jobs-count"]'))
          print("TOTAL RESULTS: ", total_results.text)
        except Exception as e:
            print(e)
        


        #---------------------------------Outer loop to loop through the pages
        for i in range(1, page_numbers + 1): # the minus 2 is beucase of the arroes

          jobCardCounter = 0 #counts the number of jobs there are on that page
          main_window = self.driver.current_window_handle
          try:
            results = self.driver.find_elements(By.CLASS_NAME, "res-sfoyn7") # this is the amount of jobs on the page

          except Exception as e: 
            print(e)
          #-----------------------------------Loop for the jobs---------------------------------------------
          for result in results:
            
            print("JOBCARDCOUNTER ----- LEN(RESULTS)   ", jobCardCounter, '   ', len(results))

            if jobCardCounter == len(results) - 1:
                print("Next page button is visible, clicking...")
                next_page = self.driver.find_element(By.XPATH, '//a[contains(@class, "res-1thqtcl") and contains(@aria-label, "Nächste")]')
                next_page.click()
                time.sleep(2)  # Allow page to load
                break  # Restart loop for new page content
            else:
                print("Not yet time to click next page")

        
            hover = ActionChains(self.driver).move_to_element(result)
            hover.perform()
            result.click()

            while len(self.driver.window_handles) <= 1:  
              time.sleep(0.5)

            new_tabs = [tab for tab in self.driver.window_handles if tab != main_window]
            if new_tabs:
              self.driver.switch_to.window(new_tabs[0])

            
            #if you have to log in ------------------------------------------------------------------
            time.sleep(5)
            try: 
                
                self.driver.execute_script("window.scrollBy(0, 300);")  # Scroll down by 500 pixels
                login_button2 = self.driver.find_element(By.XPATH, "//button[@data-testid='login-link']")
                login_button2.click()
            
                time.sleep(5)
                self.driver.find_element(By.CSS_SELECTOR, "input[data-testid='email-input']").send_keys('Your UserName')
                self.driver.find_element(By.CSS_SELECTOR, "input[data-testid='password-input']").send_keys('Your Password')

                login_button3 = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='login-submit-btn']")
                login_button3.click()

                time.sleep(10)
                try: #if that pesky dismiss appears
                  dismiss_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-genesis-element='BUTTON'][aria-label='dismiss dialog']")
                  dismiss_button.click()
                except Exception as e:
                  print("NO DISMISS BUTTON")
                  print(e)
                

                time.sleep(5)
            except NoSuchElementException:
                print("Login button not found, skipping...")

            #this try catch is for the actual application process: the except should close the window and contiue to the next application
            try:

              #here is where we need logic to see if we have already applied because if so the button will dispaly that text
              apply_button = self.driver.find_element(By.XPATH, "//span[@class='job-ad-display-qmudqb']")
              button_text = apply_button.text

              if button_text == "Schon beworben":
                print("ALREADY APPLIED")
                self.driver.close()
                self.driver.switch_to.window(main_window) 
                jobCardCounter += 1
                continue #this should make it go 

              else:
                time.sleep(2)
                interessted_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='harmonised-apply-button']")
                interessted_button.click()

              try:
                print("Attempting the 3 step applicaotin ")
                dropdown = self.driver.find_element(By.ID, "stepstone-form-element-:r10:")
                select = Select(dropdown)
                select.select_by_visible_text("Herr")
                time.sleep(2)
                next_step_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='sectionSubmit']")
                next_step_button.click()

                time.sleep(4) 
                next_step_button2 = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='sectionSubmit']")
                next_step_button2.click()

                time.sleep(4)
                submit_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='dynamicFormSubmit']")
                submit_button.click()

                time.sleep(1)
                current_url = self.driver.current_url
                with open("applied_links.txt", "a") as file:
                  # Write the URL followed by a newline for better readability
                  file.write(current_url + "\n")

                print("URL has been written to the file.")

                #close the window, and this is where we have to add to a text file what job it applied to
                time.sleep(4)
                self.driver.close()
                self.driver.switch_to.window(main_window) 

              except:
                print("3 step application failed, trying other optins")
              
              try:
                #this is to make sure that only the application whihc is completed is written to teh file since that is how the logic works
                apply_button = self.driver.find_element(By.XPATH, "//span[@class='apply-application-process-renderer-qmudqb']")
                button_text = apply_button.text

                print("attempting simple applicatoin 1 click button if there are more imput fields then this does not apply :) ")
                self.driver.execute_script("window.scrollBy(0, 300);") 
                time.sleep(4)
                submit_button3 = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='sendApplication']")
                submit_button3.click()

                
                time.sleep(1)
                if button_text != "Bewerbung fortsetzen":   #to make sure only the right applications are written to the file
                    
                  current_url = self.driver.current_url
                  with open("applied_links.txt", "a") as file:
                    # Write the URL followed by a newline for better readability
                    file.write(current_url + "\n")

                  print("URL has been written to the file.")

                #close the window, and this is where we have to add to a text file what job it applied to
                time.sleep(4)
                self.driver.close()
                self.driver.switch_to.window(main_window) 

              except:
                print("The faster application did not work either")
            except:
              print("COULD NOT APPLY TO THIS ONE")
              self.driver.close()
              self.driver.switch_to.window(main_window)
              
            jobCardCounter += 1 # just to speed things up
          
    
    def close(self):
        """Close the driver."""
        self.driver.quit()


# Main execution
if __name__ == "__main__":
    job_search = StepstoneJobSearch()

    job_search.load_cookies("cookies.pkl")

    job_search.visit_stepstone()

    job_search.accept_cookies()

    job_search.search_jobs("Junior-Softwareentwickler/in", "Berlin")

    job_search.apply_jobs() 

    job_search.close()

# app/main.py
import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import logging
import time
from typing import Dict

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app instance
app = FastAPI(title="Attendance Automation API",
             description="API for automating attendance sign-in/sign-out",
             version="1.0.0")

class LoginCredentials(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    status: str
    message: str = ""

class LoginAutomation:
    def __init__(self):
        self.browser = None
        self.base_url = "https://invigo-software.greythr.com"
        self.setup_browser()

    def setup_browser(self) -> None:
        """Configure and initialize the Chrome browser"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        
        service = Service('/usr/bin/chromedriver')

        try:
            self.browser = webdriver.Chrome(service=service, options=options)
            logger.info("Browser setup successful")
        except Exception as e:
            logger.error(f"Failed to setup browser: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to setup browser")

    def _perform_login(self) -> None:
        """Common login functionality"""
        try:
            logger.info("Navigating to login page")
            self.browser.get(self.base_url)
            time.sleep(2)

            # Fill in username
            username_input = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_input.clear()
            username_input.send_keys(self.credentials.username)

            # Fill in password
            password_input = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_input.clear()
            password_input.send_keys(self.credentials.password)

            # Click login button
            login_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'bg-primary')]"))
            )
            login_button.click()
            logger.info("Login successful")
            
            # Wait for dashboard to load
            time.sleep(5)
            
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Login failed")

    def login_and_sign_in(self, username: str, password: str) -> Dict[str, str]:
        """Perform sign-in operation"""
        self.credentials = LoginCredentials(username=username, password=password)
        
        try:
            self._perform_login()
            
            # Click Sign-in button
            signin_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'p-1.5x h-18x widget-border bg-white')]//div[contains(@class, 'btn-container')]/gt-button[contains(@shade, 'primary')]"))
            )
            signin_button.click()
            logger.info("Sign-in button clicked")
            time.sleep(5)
            
            return {"status": "success", "message": "Sign-in successful"}
            
        except Exception as e:
            logger.error(f"Sign-in failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Sign-in failed")
        finally:
            if self.browser:
                self.browser.quit()
                logger.info("Browser closed")

    def login_and_sign_out(self, username: str, password: str) -> Dict[str, str]:
        """Perform sign-out operation"""
        self.credentials = LoginCredentials(username=username, password=password)
        
        try:
            self._perform_login()
            
            # Click Sign-out button
            signout_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'btn-container mt-3x flex flex-row-reverse justify-between ng-star-inserted')]/gt-button[contains(@shade, 'primary')]"))
            )
            signout_button.click()
            logger.info("Sign-out button clicked")
            time.sleep(5)
            
            return {"status": "success", "message": "Sign-out successful"}
            
        except Exception as e:
            logger.error(f"Sign-out failed: {str(e)}")
            raise HTTPException(status_code=500, detail="Sign-out failed")
        finally:
            if self.browser:
                self.browser.quit()
                logger.info("Browser closed")

def get_credentials() -> LoginCredentials:
    """Dependency to retrieve credentials from environment variables"""
    username = os.getenv("LOGIN_USERNAME")
    password = os.getenv("LOGIN_PASSWORD")
    
    if not username or not password:
        raise HTTPException(
            status_code=500,
            detail="Missing credentials in environment variables"
        )
    
    return LoginCredentials(username=username, password=password)

@app.post("/sign-in", response_model=LoginResponse)
async def perform_sign_in(credentials: LoginCredentials = Depends(get_credentials)) -> LoginResponse:
    """Endpoint to perform sign-in operation"""
    try:
        automation = LoginAutomation()
        result = automation.login_and_sign_in(credentials.username, credentials.password)
        return LoginResponse(**result)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Sign-in automation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Sign-in automation failed")

@app.post("/sign-out", response_model=LoginResponse)
async def perform_sign_out(credentials: LoginCredentials = Depends(get_credentials)) -> LoginResponse:
    """Endpoint to perform sign-out operation"""
    try:
        automation = LoginAutomation()
        result = automation.login_and_sign_out(credentials.username, credentials.password)
        return LoginResponse(**result)
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Sign-out automation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Sign-out automation failed")

import time
import random
import logging
from tkinter import Tk, messagebox

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Configurar el registro
logging.basicConfig(level=logging.INFO)

url = 'https://dragonbound.net/'
username = 'Username'
password = 'Password'
page_timeout = 2

# Configurar opciones de Chrome
chrome_options = Options()
chrome_options.add_argument('--kiosk')
chrome_options.add_argument('--no-sandbox')  # Añadir esta línea para evitar problemas de permisos

driver = webdriver.Chrome(options=chrome_options)

def log(message):
    logging.info(message)

def init():
    log("Navegando a la URL.")
    driver.get(url)
    wait_for_page_load()

def random_delay():
    return random.random() + 0.1

def wait_for_login_form():
    log("Esperando el formulario de inicio de sesión.")
    WebDriverWait(driver, page_timeout).until(
        EC.presence_of_element_located((By.ID, 'LoginPass'))
    )

def login():
    log("Iniciando el proceso de inicio de sesión.")
    try:
        user_div = driver.find_element(By.ID, 'LoginUsername')
        user_div.click()
        for letter in username:
            time.sleep(random_delay())
            user_div.send_keys(letter)
        
        password_div = driver.find_element(By.ID, 'LoginPass')
        password_div.click()
        for letter in password:
            time.sleep(random_delay())
            password_div.send_keys(letter)
        
        time.sleep(random_delay())
        driver.find_element(By.ID, 'LoginSubmit').click()
        log("Proceso de inicio de sesión completado.")
    except Exception as e:
        log(f"Error durante el inicio de sesión: {e}")

def wait_for_server():
    log("Esperando el elemento del servidor.")
    WebDriverWait(driver, page_timeout).until(
        EC.presence_of_element_located((By.ID, 'BrokerChannel2'))
    )

def scroll_to_element(element):
    driver.execute_script("arguments[0].scrollIntoView(true);", element)

def wait_for_and_click_element(element_id):
    try:
        log(f"Esperando a que el elemento con ID '{element_id}' sea clickeable.")
        element = WebDriverWait(driver, page_timeout).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        scroll_to_element(element)
        ActionChains(driver).move_to_element(element).click().perform()
        log(f"Haciendo clic en el elemento con ID '{element_id}'.")
    except TimeoutException:
        log(f"Elemento con ID '{element_id}' no clickeable o no encontrado.")
    except NoSuchElementException:
        log(f"Elemento con ID '{element_id}' no encontrado.")
    except Exception as e:
        log(f"Error en wait_for_and_click_element: {e}")

def pick_server():
    time.sleep(random_delay())
    wait_for_and_click_element('BrokerChannel2')  # Servidor para principiantes

def wait_for_event_button():
    log("Esperando el botón de evento.")
    WebDriverWait(driver, page_timeout).until(
        EC.presence_of_element_located((By.ID, 'event_button'))
    )

def click_event_button():
    log("Haciendo clic en el botón de evento.")
    try:
        time.sleep(random_delay())
        driver.find_element(By.ID, 'event_button').click()
        log("Botón de evento clickeado.")
    except Exception as e:
        log(f"Error durante el clic en el botón de evento: {e}")

def wait_for_page_load():
    WebDriverWait(driver, page_timeout).until(
        lambda driver: driver.execute_script('return document.readyState') == 'complete'
    )

def show_completion_message():
    root = Tk()
    root.withdraw()  # Oculta la ventana principal
    messagebox.showinfo("Información", "El Cash ha sido recolectado.")
    root.destroy()

if __name__ == '__main__':
    try:
        init()
        wait_for_login_form()
        login()
        wait_for_server()
        pick_server()
        wait_for_event_button()
        click_event_button()
    finally:
        show_completion_message()
        # Descomentar la siguiente línea si deseas cerrar el navegador después de la ejecución
        # driver.quit()

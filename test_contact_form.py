#!/usr/bin/env python3
"""
Test script for Contact Us page functionality
"""
import requests
import sys
from bs4 import BeautifulSoup

def test_contact_page():
    """Test the contact page functionality"""
    base_url = "http://127.0.0.1:8001"
    contact_url = f"{base_url}/contact/"
    
    print("🧪 Testing Contact Us Page Functionality")
    print("=" * 50)
    
    # Test 1: Page Access
    print("\n1. Testing Page Access...")
    try:
        response = requests.get(contact_url)
        if response.status_code == 200:
            print("✅ Contact page loads successfully (HTTP 200)")
        else:
            print(f"❌ Contact page failed to load (HTTP {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Django server. Make sure it's running on port 8001")
        return False
    
    # Test 2: Parse HTML and check elements
    print("\n2. Testing Page Elements...")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Check for contact form
    contact_form = soup.find('form', {'id': 'contact-form'})
    if contact_form:
        print("✅ Contact form found")
    else:
        print("❌ Contact form not found")
        return False
    
    # Check for required form fields
    required_fields = ['name', 'email', 'subject', 'message']
    for field in required_fields:
        field_element = soup.find('input', {'name': field}) or soup.find('textarea', {'name': field})
        if field_element:
            print(f"✅ {field.capitalize()} field found")
        else:
            print(f"❌ {field.capitalize()} field not found")
    
    # Check for CSRF token
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})
    if csrf_token:
        print("✅ CSRF token found")
        csrf_value = csrf_token.get('value')
    else:
        print("❌ CSRF token not found")
        return False
    
    # Test 3: Form Submission with Valid Data
    print("\n3. Testing Form Submission...")
    
    # Create session to maintain cookies
    session = requests.Session()
    
    # Get the page first to get CSRF token
    get_response = session.get(contact_url)
    soup = BeautifulSoup(get_response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    
    # Test data
    form_data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '+254700000000',
        'subject': 'Test Contact Form',
        'message': 'This is a test message from the automated test script.',
        'csrfmiddlewaretoken': csrf_value
    }
    
    try:
        post_response = session.post(contact_url, data=form_data)
        if post_response.status_code == 200:
            print("✅ Form submission successful (HTTP 200)")
            
            # Check for success message in response
            response_soup = BeautifulSoup(post_response.content, 'html.parser')
            messages = response_soup.find_all('div', class_='alert')
            if messages:
                for message in messages:
                    message_text = message.get_text().strip()
                    if 'success' in message_text.lower() or 'thank you' in message_text.lower():
                        print(f"✅ Success message displayed: {message_text}")
                    else:
                        print(f"⚠️  Message displayed: {message_text}")
            else:
                print("⚠️  No messages displayed after form submission")
        else:
            print(f"❌ Form submission failed (HTTP {post_response.status_code})")
    except Exception as e:
        print(f"❌ Form submission error: {str(e)}")
    
    # Test 4: Form Validation (Empty Fields)
    print("\n4. Testing Form Validation...")
    
    empty_form_data = {
        'name': '',
        'email': '',
        'subject': '',
        'message': '',
        'csrfmiddlewaretoken': csrf_value
    }
    
    try:
        validation_response = session.post(contact_url, data=empty_form_data)
        if validation_response.status_code == 200:
            response_soup = BeautifulSoup(validation_response.content, 'html.parser')
            messages = response_soup.find_all('div', class_='alert')
            if messages:
                for message in messages:
                    message_text = message.get_text().strip()
                    if 'error' in message_text.lower() or 'required' in message_text.lower():
                        print(f"✅ Validation error displayed: {message_text}")
                    else:
                        print(f"⚠️  Message displayed: {message_text}")
            else:
                print("⚠️  No validation messages displayed for empty form")
    except Exception as e:
        print(f"❌ Validation test error: {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Contact page testing completed!")
    return True

if __name__ == "__main__":
    test_contact_page()

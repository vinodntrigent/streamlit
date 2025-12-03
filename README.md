# Haystack AI Product Assistant - Streamlit App

A Streamlit application that matches the design of the Haystack AI Product Assistant interface.

## Features

- **Red Header**: Fixed header with haystack logo and navigation buttons
- **Chat Interface**: Clean chat UI with AI assistant and user messages
- **Message Bubbles**: 
  - AI messages in light beige bubbles with lightning bolt icon
  - User messages in light purple bubbles with user icon
- **Input Bar**: Fixed bottom input bar with microphone and send icons
- **Example Conversation**: Includes the example conversation from the design

## Installation

1. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running the App

Run the Streamlit app with:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Design Details

- **Header Color**: Crimson Red (#DC143C)
- **AI Message Bubble**: Light Beige (#F5F5DC)
- **User Message Bubble**: Light Purple/Lavender (#E6E6FA)
- **Logo**: White square with red border containing "H"
- **Icons**: Lightning bolt (⚡) for AI, User silhouette (👤) for user messages

## Customization

You can customize the AI responses by modifying the response logic in the `if user_input:` section of `app.py`. Connect it to your AI model or API as needed.




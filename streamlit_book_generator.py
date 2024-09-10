import streamlit as st
import pandas as pd

# Create a sidebar input for user text
input_text = st.sidebar.text_area("Enter your text:", "")

# Function to generate book pages
def generate_book_pages(text):
    # Split the text into paragraphs
    paragraphs = text.split("\n\n")

    # Initialize an empty list to store book pages
    book_pages = []

    # Loop through each paragraph
    for para in paragraphs:
        # Split the paragraph into sentences
        sentences = para.split("\n")

        # Loop through each sentence
        for sentence in sentences:
            # Check for specific keywords at the beginning of the sentence
            if sentence.startswith("Chapter"):
                # Add chapter heading and a new page
                book_pages.append("## " + sentence + "\n")
            elif sentence.startswith("Section"):
                # Add section heading
                book_pages[-1] += "### " + sentence + "\n"
            else:
                # Append the sentence to the current page
                book_pages[-1] += sentence + " "

            # Check if the current page exceeds 400 words
            if len(book_pages[-1].split()) > 400:
                # Create a new page if the word limit is reached
                book_pages.append("")

    return book_pages

# Create a Streamlit app
def app():
    st.title("Book Generator")

    # Check if input text is provided
    if not input_text:
        st.write("Please enter some text in the sidebar.")
        return

    # Generate book pages from the input text
    book_pages = generate_book_pages(input_text)

    # Display the generated book
    st.header("Generated Book")
    st.write(book_pages)

    # Allow downloading the book as a PDF
    st.download_button(
        label="Download Book as PDF",
        data=book_pages,
        file_name="my_book.pdf",
        mime="application/pdf",
    )

# Run the Streamlit app
if __name__ == "__main__":
    app()

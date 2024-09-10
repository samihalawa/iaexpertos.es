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

        # Initialize a set to store common tokens
        common_tokens = set(["token1", "token2", "token3"])
        context_established = False

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

            # Check for common tokens in the sentence
            sentence_tokens = set(sentence.lower().split())
            common_tokens &= sentence_tokens

            # Check if sufficient context is established
            if len(common_tokens) < 5:
                context_established = True

            # Check if the current page exceeds 400 words or context is established
            if len(book_pages[-1].split()) > 400 or context_established:
                # Create a new page or end the loop if context is established
                book_pages.append("")
                if context_established:
                    break

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

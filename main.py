import streamlit as st
from scraper import extract_body_content, clean_body_content, split_dom_content,scrape_website_undetect
from llms2 import call_with_openrouter,parse_with_gemini
from llms import parse_with_ollama,call_with_ollama
from vectorDB import score_chunks_by_query
import re
import pandas as pd
st.title("Web Scraper")

with st.sidebar:
    choice = st.radio("Select an option", ["Upload file", "Upload URL"])
    st.info("Upload a file or a URL to scrape data from")

if choice == "Upload file":
    file = st.file_uploader("Upload an HTML file", type=["html"])

    if file is not None:
        try:
            body_content = extract_body_content(file)
            cleaned_body_content = clean_body_content(body_content)

            with st.expander("Content"):
                st.text_area("Body content", cleaned_body_content, height=400)

            st.session_state.body_content = cleaned_body_content

            # Description input
            parse_description = st.text_input("Enter the description of the data you want to scrape", key="parse_description")

            # User selects action
            choice2 = st.radio("Select an option", ["Get Data", "Parse Data"])

            # Single scrape button for both choices
            if st.button("Scrape Data"):
                st.write("Scraping data...")

                if choice2 == "Get Data":
                    result = parse_with_gemini(cleaned_body_content, parse_description=parse_description)
                    with open("./files/copy.csv", "w") as file:
                        file.write(result)
                    df=pd.read_csv("./files/copy.csv")
                    st.dataframe(df)
                    st.download_button(
                    label="Download CSV",
                    data=result,
                    file_name="data.csv",
                    mime="text/csv"
                )
                    
                else:  # "Parse Data"
                    print(len(cleaned_body_content))
                    print(type(cleaned_body_content))
                    chunks=split_dom_content(cleaned_body_content), 
                    result = call_with_openrouter(chunks, parse_description=parse_description)

                    st.text_area("Extracted Data", result, height=300)
        except Exception as e:
            st.error(f"Error processing file: {e}")
    else:
        st.info("Please upload a file to proceed.")


            #st.session_state.result=parse_with_ollama(chunks,st.session_state.parse_description)
            #print(st.session_state.result)
        #""" if st.session_state.result:
        #        file=re.findall(r'</think>\s*```csv\n(.*?)```',st.session_state.result , re.DOTALL)
        #        output="".join(file).strip()
        #        print(output)
        #        st.text(output)
        #        with st.expander("output"):
        #            st.text_area("output file",output,height=500)
        #        st.download_button(
        #        label="Download CSV",
        #        data=output,
        #        file_name="movie_data.csv",
        #        mime="text/csv"
        #        )"""

elif choice == "Upload URL":
    # Store the entered URL in session_state
    url = st.text_input("Enter the URL you want to scrape", key="url_input")

    # Submit button to trigger scrape
    if st.button("SUBMIT"):
        if url:
            try:
                link = scrape_website_undetect(url)
                body_content = extract_body_content(link)
                cleaned_body_content = clean_body_content(body_content)

                # Store cleaned content in session state
                st.session_state.cleaned_body_content = cleaned_body_content
                st.session_state.url_submitted = True
            except Exception as e:
                st.error(f"Error during scraping: {e}")
        else:
            st.error("Please enter a valid URL.")

    # Only show the rest if scraping has been triggered and content is stored
    if st.session_state.get("url_submitted", False):
        with st.expander("Content"):
            st.text_area("Body content", st.session_state.cleaned_body_content, height=400)

        # Input for data extraction description
        parse_description = st.text_input("Enter the description of the data you want to scrape", key="parse_description")

        # Option radio
        choice2 = st.radio("Select an option", ["Get Data", "Parse Data"], key="url_mode")

        # Scrape button
        if st.button("Scrape Data"):
            st.session_state.url_scrape_triggered = True

        # Run scraping based on user's option after button click
        if st.session_state.get("url_scrape_triggered", False):
            st.write("Scraping data...")

            if st.session_state.url_mode == "Get Data":
                result = parse_with_gemini(
                    st.session_state.cleaned_body_content,
                    parse_description=parse_description
                )
                with open("./files/copy.csv", "w") as file:
                        file.write(result)
                df=pd.read_csv("./files/copy.csv")
                st.dataframe(df)
                st.download_button(
                label="Download CSV",
                data=result,
                file_name="data.csv",
                mime="text/csv"
            )
            else:
                print(len(st.session_state.cleaned_body_content))
                print(type(st.session_state.cleaned_body_content))
                chunks=split_dom_content(st.session_state.cleaned_body_content),
                result = call_with_openrouter(
                    chunks=chunks[0],
                    parse_description=parse_description
                )
                st.text_area("Extracted Data", result, height=300)